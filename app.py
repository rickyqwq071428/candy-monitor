#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可予礼品有限公司 - 喜糖/伴手礼竞品监控平台
Flask 主应用
"""

import os
import json
import random
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import (
    init_db, get_rankings, add_ranking, clear_rankings,
    get_viral_content, add_viral, clear_viral,
    get_age_distribution, add_age_distribution, clear_age,
    get_merchants, add_merchant, clear_merchants,
    create_share_link, get_share_links, verify_share_token,
    revoke_share_link, regenerate_share_link, delete_share_link,
    get_dashboard_stats, get_trends_data
)
from taobao import collector
from backend.ai_router import (
    call_text_model, call_image_model, call_video_model, check_video_task,
    generate_xiaohongshu, generate_douyin,
    get_available_models_info,
    IMAGE_STYLE_PROMPTS, VIDEO_STYLE_PROMPTS,
)

app = Flask(__name__)
app.config['BRAND_NAME'] = '可予礼品有限公司'
app.config['BRAND_COLOR'] = '#8B2942'
app.config['GOLD_COLOR'] = '#C9A961'

# 初始化数据库
init_db()


# ==========================================
# 页面路由
# ==========================================

@app.route('/')
def dashboard():
    """Dashboard 首页概览"""
    stats = get_dashboard_stats()
    rankings = get_rankings(limit=10)
    viral = get_viral_content(limit=6)
    return render_template('dashboard.html', stats=stats, rankings=rankings, viral=viral)


@app.route('/rankings')
def rankings():
    """销量排行页面"""
    platform = request.args.get('platform', '')
    keyword = request.args.get('keyword', '')
    data = get_rankings(platform=platform or None, keyword=keyword or None)
    platforms = ['淘宝', '抖音', '小红书', '大众点评']
    return render_template('rankings.html', rankings=data, platforms=platforms,
                           current_platform=platform, current_keyword=keyword)


@app.route('/viral')
def viral():
    """爆款内容页面"""
    platform = request.args.get('platform', '')
    data = get_viral_content(platform=platform or None)
    platforms = ['抖音', '小红书', '大众点评']
    return render_template('viral.html', viral=data, platforms=platforms,
                           current_platform=platform)


@app.route('/age')
def age():
    """消费者年龄分布"""
    data = get_age_distribution()
    return render_template('age.html', age_data=data)


@app.route('/trends')
def trends():
    """行业趋势"""
    data = get_trends_data()
    return render_template('trends.html', trends=data)


@app.route('/merchants')
def merchants():
    """跟踪商家"""
    platform = request.args.get('platform', '')
    data = get_merchants(platform=platform or None)
    platforms = ['淘宝', '抖音', '小红书', '大众点评']
    return render_template('merchants.html', merchants=data, platforms=platforms,
                           current_platform=platform)


@app.route('/excel')
def excel_import():
    """Excel 数据导入"""
    return render_template('excel.html')


@app.route('/quick-collect')
def quick_collect():
    """快速采集页面"""
    links = collector.get_alternative_links('喜糖')
    mode_info = collector.get_mode_info()
    return render_template('quick_collect.html', links=links, mode_info=mode_info)


@app.route('/guide')
def guide():
    """新手引导页面"""
    stats = get_dashboard_stats()
    return render_template('guide.html', stats=stats)


@app.route('/create')
def create():
    """AI 创作模块"""
    return render_template('create.html')


@app.route('/share')
def share():
    """分享管理"""
    links = get_share_links()
    return render_template('share.html', share_links=links)


@app.route('/s/<token>')
def shared_view(token):
    """受邀用户查看页面"""
    link = verify_share_token(token)
    if not link:
        return render_template('shared_expired.html'), 404
    if link.get('expired'):
        return render_template('shared_expired.html'), 410

    stats = get_dashboard_stats()
    rankings = get_rankings(limit=10)
    viral = get_viral_content(limit=6)
    return render_template('shared_view.html', stats=stats, rankings=rankings,
                           viral=viral, permission=link['permission'])


# ==========================================
# 分享 API
# ==========================================

@app.route('/api/share/create', methods=['POST'])
def api_share_create():
    data = request.json or {}
    title = data.get('title', '竞品数据分享')
    permission = data.get('permission', 'readonly')
    expiry_type = data.get('expiry_type', '7d')
    token = create_share_link(title, permission, expiry_type)
    return jsonify({'success': True, 'token': token, 'url': f'/s/{token}'})


@app.route('/api/share/list')
def api_share_list():
    links = get_share_links()
    return jsonify({'success': True, 'links': links})


@app.route('/api/share/revoke', methods=['POST'])
def api_share_revoke():
    token = (request.json or {}).get('token', '')
    revoke_share_link(token)
    return jsonify({'success': True})


@app.route('/api/share/regenerate', methods=['POST'])
def api_share_regenerate():
    token = (request.json or {}).get('token', '')
    new_token = regenerate_share_link(token)
    if new_token:
        return jsonify({'success': True, 'token': new_token, 'url': f'/s/{new_token}'})
    return jsonify({'success': False, 'error': '链接不存在'}), 404


@app.route('/api/share/delete', methods=['POST'])
def api_share_delete():
    token = (request.json or {}).get('token', '')
    delete_share_link(token)
    return jsonify({'success': True})


# ==========================================
# Excel 导入 API
# ==========================================

@app.route('/api/excel/upload', methods=['POST'])
def api_excel_upload():
    """上传 Excel 并导入数据"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': '请选择文件'}), 400

    file = request.files['file']
    import_type = request.form.get('type', 'rankings')

    try:
        import openpyxl
        wb = openpyxl.load_workbook(file)
        ws = wb.active

        count = 0
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]:
                continue

            if import_type == 'rankings':
                if len(row) >= 6:
                    platform_map = {'淘宝': '淘宝', 'taobao': '淘宝', 'tb': '淘宝',
                                    '抖音': '抖音', 'douyin': '抖音', 'dy': '抖音',
                                    '小红书': '小红书', 'xhs': '小红书',
                                    '大众点评': '大众点评', 'dianping': '大众点评', 'dp': '大众点评'}
                    platform = platform_map.get(str(row[0]).strip().lower(), str(row[0]).strip())
                    add_ranking({
                        'platform': platform,
                        'keyword': str(row[1]) if row[1] else '',
                        'rank': int(row[2]) if row[2] else 0,
                        'product_name': str(row[3]) if row[3] else '',
                        'shop_name': str(row[4]) if row[4] else '',
                        'price': float(row[5]) if row[5] else 0,
                        'sales': int(row[6]) if len(row) > 6 and row[6] else 0,
                        'product_link': str(row[7]) if len(row) > 7 and row[7] else '',
                        'source': 'excel_import'
                    })
                    count += 1

            elif import_type == 'viral':
                if len(row) >= 4:
                    add_viral({
                        'platform': str(row[0]).strip(),
                        'title': str(row[1]) if row[1] else '',
                        'author': str(row[2]) if row[2] else '',
                        'likes': int(row[3]) if row[3] else 0,
                        'comments': int(row[4]) if len(row) > 4 and row[4] else 0,
                        'shares': int(row[5]) if len(row) > 5 and row[5] else 0,
                        'content_link': str(row[6]) if len(row) > 6 and row[6] else '',
                        'keyword': str(row[7]) if len(row) > 7 and row[7] else '',
                        'source': 'excel_import'
                    })
                    count += 1

            elif import_type == 'age':
                if len(row) >= 3:
                    add_age_distribution({
                        'source': str(row[0]).strip(),
                        'age_group': str(row[1]).strip(),
                        'percentage': float(row[2]) if row[2] else 0,
                        'gender': str(row[3]) if len(row) > 3 and row[3] else None,
                        'sample_size': int(row[4]) if len(row) > 4 and row[4] else None,
                        'platform': str(row[5]) if len(row) > 5 and row[5] else None
                    })
                    count += 1

        return jsonify({'success': True, 'count': count, 'message': f'成功导入 {count} 条数据'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/excel/template/<template_type>')
def api_excel_template(template_type):
    """下载 Excel 模板"""
    import openpyxl
    from flask import send_file
    import io

    wb = openpyxl.Workbook()
    ws = wb.active

    if template_type == 'rankings':
        ws.title = '销量排行'
        ws.append(['平台(淘宝/抖音/小红书/大众点评)', '搜索关键词', '排名', '商品名称', '店铺名称', '价格(元)', '销量', '链接'])
    elif template_type == 'viral':
        ws.title = '爆款内容'
        ws.append(['平台(抖音/小红书/大众点评)', '标题', '作者', '点赞数', '评论数', '分享数', '链接', '关键词'])
    elif template_type == 'age':
        ws.title = '年龄分布'
        ws.append(['数据来源', '年龄段', '占比(%)', '性别', '样本量', '平台'])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name=f'candy_monitor_{template_type}_template.xlsx')


# ==========================================
# AI 创作 API — 统一模型路由
# ==========================================

@app.route('/api/ai/models')
def api_ai_models():
    """获取所有模型信息"""
    return jsonify({'success': True, 'models': get_available_models_info()})


@app.route('/api/ai/image', methods=['POST'])
def api_ai_image():
    """AI 图片生成"""
    data = request.json or {}
    prompt = data.get('prompt', '')
    style = data.get('style', '写实')
    size = data.get('size', '1024x1024')
    model = data.get('model', 'flux_schnell')

    if not prompt:
        return jsonify({'success': False, 'error': '请输入提示词'}), 400

    style_en = IMAGE_STYLE_PROMPTS.get(style, IMAGE_STYLE_PROMPTS['写实'])
    full_prompt = f"{prompt}, {style_en}"

    result = call_image_model(model, full_prompt, size)
    if result.get('success'):
        return jsonify({
            'success': True,
            'image_url': result['image_url'],
            'engine': result.get('engine', ''),
            'prompt': prompt, 'style': style,
        })
    return jsonify(result), 500


@app.route('/api/ai/video', methods=['POST'])
def api_ai_video():
    """AI 视频生成 — 异步任务"""
    data = request.json or {}
    prompt = data.get('prompt', '')
    duration = data.get('duration', '5秒')
    style = data.get('style', '实拍风')
    model = data.get('model', 'cogvideo')

    if not prompt:
        return jsonify({'success': False, 'error': '请输入视频描述'}), 400

    result = call_video_model(model, prompt, duration, style)
    return jsonify(result)


@app.route('/api/ai/video_status/<task_id>')
def api_ai_video_status(task_id):
    """查询视频生成进度"""
    result = check_video_task(task_id)
    return jsonify(result)


@app.route('/api/ai/xiaohongshu', methods=['POST'])
def api_ai_xiaohongshu():
    """小红书爆款笔记生成"""
    data = request.json or {}
    product = data.get('product', '')
    style = data.get('style', '种草测评')
    length = data.get('length', '标准')
    keywords = data.get('keywords', '')
    model = data.get('model', 'deepseek')

    if not product:
        return jsonify({'success': False, 'error': '请输入产品名称'}), 400

    result = generate_xiaohongshu(product, style, length, keywords, model)
    if result.get('success'):
        return jsonify(result)
    return jsonify({'success': False, 'error': '生成失败'}), 500


@app.route('/api/ai/douyin', methods=['POST'])
def api_ai_douyin():
    """抖音爆款脚本生成"""
    data = request.json or {}
    product = data.get('product', '')
    script_style = data.get('style', '开箱测评')
    duration = data.get('duration', '30秒')
    model = data.get('model', 'deepseek')

    if not product:
        return jsonify({'success': False, 'error': '请输入产品名称'}), 400

    result = generate_douyin(product, script_style, duration, model)
    if result.get('success'):
        return jsonify(result)
    return jsonify({'success': False, 'error': '生成失败'}), 500


# ==========================================
# 系统重置 API
# ==========================================

@app.route('/api/reset', methods=['POST'])
def api_reset():
    """清空所有数据"""
    clear_rankings()
    clear_viral()
    clear_age()
    clear_merchants()
    return jsonify({'success': True, 'message': '所有数据已清空'})


# ==========================================
# 健康检查（云部署用）
# ==========================================

@app.route('/health')
def health():
    """健康检查端点"""
    stats = get_dashboard_stats()
    return jsonify({
        'status': 'ok',
        'service': '可予礼品竞品监控平台',
        'version': '2.1',
        'database': 'connected' if stats else 'empty',
        'total_products': stats.get('total_products', 0),
        'total_viral': stats.get('total_viral', 0)
    })


if __name__ == '__main__':
    import os
    host = os.environ.get('CANDY_HOST', '0.0.0.0')
    port = int(os.environ.get('CANDY_PORT', '5000'))
    app.run(host=host, port=port, debug=True)
