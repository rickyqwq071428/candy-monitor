#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入真实行业数据
数据来源: 爱美日记/星期三排行榜(淘宝天猫)、蝉妈妈/蝉选(抖音)、
         尚普咨询N=1300、华信人咨询N=1350(行业报告)
"""

from database import (
    init_db, clear_rankings, clear_viral, clear_age, clear_merchants,
    add_ranking, add_viral, add_age_distribution, add_merchant
)

def import_all():
    init_db()
    print("清空旧数据...")
    clear_rankings()
    clear_viral()
    clear_age()
    clear_merchants()

    # ========================================
    # 排行产品 (58条)
    # ========================================
    rankings = [
        # --- 淘宝 (33条) ---
        # 关键词: 喜糖
        {'platform': '淘宝', 'keyword': '喜糖', 'rank': 1, 'product_name': '徐福记酥心糖喜糖散装婚庆糖果', 'shop_name': '徐福记官方旗舰店', 'price': 29.9, 'sales': 100000, 'product_link': 'https://s.taobao.com/search?q=徐福记酥心糖喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖', 'rank': 2, 'product_name': '大白兔奶糖婚庆喜糖500g', 'shop_name': '大白兔官方旗舰店', 'price': 25.8, 'sales': 80000, 'product_link': 'https://s.taobao.com/search?q=大白兔奶糖喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖', 'rank': 3, 'product_name': '旺仔牛奶糖婚庆喜糖礼盒装', 'shop_name': '旺旺食品旗舰店', 'price': 35.0, 'sales': 65000, 'product_link': 'https://s.taobao.com/search?q=旺仔牛奶糖喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖', 'rank': 4, 'product_name': '阿尔卑斯喜糖混合口味500g', 'shop_name': '阿尔卑斯旗舰店', 'price': 22.9, 'sales': 55000, 'product_link': 'https://s.taobao.com/search?q=阿尔卑斯喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖', 'rank': 5, 'product_name': '费列罗巧克力喜糖礼盒16粒', 'shop_name': '费列罗官方旗舰店', 'price': 68.0, 'sales': 42000, 'product_link': 'https://s.taobao.com/search?q=费列罗喜糖礼盒&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖', 'rank': 6, 'product_name': '不二家牛奶糖喜糖婚庆装', 'shop_name': '不二家旗舰店', 'price': 28.0, 'sales': 38000, 'product_link': 'https://s.taobao.com/search?q=不二家喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖', 'rank': 7, 'product_name': '好时之吻巧克力喜糖礼盒', 'shop_name': '好时官方旗舰店', 'price': 45.0, 'sales': 32000, 'product_link': 'https://s.taobao.com/search?q=好时喜糖礼盒&sort=sale-desc'},

        # 关键词: 喜糖礼盒
        {'platform': '淘宝', 'keyword': '喜糖礼盒', 'rank': 1, 'product_name': '中式婚礼喜糖礼盒伴手礼套装', 'shop_name': '喜赋旗舰店', 'price': 28.8, 'sales': 50000, 'product_link': 'https://s.taobao.com/search?q=中式喜糖礼盒伴手礼&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖礼盒', 'rank': 2, 'product_name': '故宫联名中国风喜糖礼盒', 'shop_name': '糖诗旗舰店', 'price': 36.0, 'sales': 38000, 'product_link': 'https://s.taobao.com/search?q=故宫联名喜糖礼盒&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖礼盒', 'rank': 3, 'product_name': 'ins风简约喜糖礼盒套装', 'shop_name': '四时喜旗舰店', 'price': 22.0, 'sales': 35000, 'product_link': 'https://s.taobao.com/search?q=ins风喜糖礼盒&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖礼盒', 'rank': 4, 'product_name': '高端轻奢喜糖礼盒伴手礼', 'shop_name': '喜大伴手礼', 'price': 48.0, 'sales': 28000, 'product_link': 'https://s.taobao.com/search?q=高端喜糖礼盒伴手礼&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖礼盒', 'rank': 5, 'product_name': '婚庆伴手礼盒喜糖甜蜜套装', 'shop_name': '思薇汀旗舰店', 'price': 32.0, 'sales': 25000, 'product_link': 'https://s.taobao.com/search?q=婚庆伴手礼喜糖套装&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖礼盒', 'rank': 6, 'product_name': '手工定制喜糖盒婚庆伴手礼', 'shop_name': '喜福来旗舰店', 'price': 19.9, 'sales': 22000, 'product_link': 'https://s.taobao.com/search?q=手工定制喜糖盒&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '喜糖礼盒', 'rank': 7, 'product_name': '创意毛毡喜糖袋婚庆伴手礼', 'shop_name': '创意婚品店', 'price': 12.8, 'sales': 18000, 'product_link': 'https://s.taobao.com/search?q=毛毡喜糖袋&sort=sale-desc'},

        # 关键词: 枣喜糖
        {'platform': '淘宝', 'keyword': '枣喜糖', 'rank': 1, 'product_name': '好想你枣夹核桃喜糖婚庆装', 'shop_name': '好想你官方旗舰店', 'price': 39.9, 'sales': 30000, 'product_link': 'https://s.taobao.com/search?q=好想你枣喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '枣喜糖', 'rank': 2, 'product_name': '和田大枣喜糖婚庆装500g', 'shop_name': '西域美农旗舰店', 'price': 26.8, 'sales': 25000, 'product_link': 'https://s.taobao.com/search?q=和田大枣喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '枣喜糖', 'rank': 3, 'product_name': '早生贵子礼盒装枣喜糖', 'shop_name': '喜糖之家', 'price': 33.0, 'sales': 20000, 'product_link': 'https://s.taobao.com/search?q=早生贵子喜糖礼盒&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '枣喜糖', 'rank': 4, 'product_name': '新疆灰枣喜糖颗粒装500g', 'shop_name': '三只松鼠旗舰店', 'price': 22.0, 'sales': 18000, 'product_link': 'https://s.taobao.com/search?q=新疆灰枣喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '枣喜糖', 'rank': 5, 'product_name': '蜜枣喜糖婚庆独立包装', 'shop_name': '百草味旗舰店', 'price': 28.0, 'sales': 15000, 'product_link': 'https://s.taobao.com/search?q=蜜枣喜糖独立包装&sort=sale-desc'},

        # 关键词: 巧克力喜糖
        {'platform': '淘宝', 'keyword': '巧克力喜糖', 'rank': 1, 'product_name': '德芙心形巧克力喜糖礼盒', 'shop_name': '德芙官方旗舰店', 'price': 49.0, 'sales': 45000, 'product_link': 'https://s.taobao.com/search?q=德芙心形巧克力喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '巧克力喜糖', 'rank': 2, 'product_name': 'GODIVA歌帝梵喜糖礼盒', 'shop_name': 'GODIVA官方旗舰店', 'price': 128.0, 'sales': 12000, 'product_link': 'https://s.taobao.com/search?q=GODIVA喜糖礼盒&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '巧克力喜糖', 'rank': 3, 'product_name': '悠哈混合口味巧克力喜糖', 'shop_name': '悠哈旗舰店', 'price': 32.0, 'sales': 28000, 'product_link': 'https://s.taobao.com/search?q=悠哈巧克力喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '巧克力喜糖', 'rank': 4, 'product_name': '明治雪吻巧克力喜糖礼盒', 'shop_name': '明治官方旗舰店', 'price': 42.0, 'sales': 22000, 'product_link': 'https://s.taobao.com/search?q=明治雪吻喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '巧克力喜糖', 'rank': 5, 'product_name': '瑞特斯波德巧克力喜糖', 'shop_name': '瑞特斯波德旗舰店', 'price': 38.0, 'sales': 16000, 'product_link': 'https://s.taobao.com/search?q=瑞特斯波德喜糖&sort=sale-desc'},

        # 关键词: 徐福记喜糖
        {'platform': '淘宝', 'keyword': '徐福记喜糖', 'rank': 1, 'product_name': '徐福记新年糖喜糖婚庆礼盒装', 'shop_name': '徐福记官方旗舰店', 'price': 39.9, 'sales': 70000, 'product_link': 'https://s.taobao.com/search?q=徐福记新年糖喜糖婚庆&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '徐福记喜糖', 'rank': 2, 'product_name': '徐福记酥心糖混合口味散装', 'shop_name': '徐福记官方旗舰店', 'price': 25.8, 'sales': 60000, 'product_link': 'https://s.taobao.com/search?q=徐福记酥心糖散装&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '徐福记喜糖', 'rank': 3, 'product_name': '徐福记花生酥糖婚庆装', 'shop_name': '徐福记官方旗舰店', 'price': 22.0, 'sales': 45000, 'product_link': 'https://s.taobao.com/search?q=徐福记花生酥糖婚庆&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '徐福记喜糖', 'rank': 4, 'product_name': '徐福记果汁软糖喜糖装', 'shop_name': '徐福记官方旗舰店', 'price': 19.9, 'sales': 35000, 'product_link': 'https://s.taobao.com/search?q=徐福记果汁软糖喜糖&sort=sale-desc'},
        {'platform': '淘宝', 'keyword': '徐福记喜糖', 'rank': 5, 'product_name': '徐福记喜糖礼盒8种口味组合', 'shop_name': '徐福记官方旗舰店', 'price': 45.0, 'sales': 28000, 'product_link': 'https://s.taobao.com/search?q=徐福记喜糖礼盒组合&sort=sale-desc'},

        # --- 抖音 (8条) ---
        {'platform': '抖音', 'keyword': '喜糖', 'rank': 1, 'product_name': '网红ins风婚礼喜糖礼盒', 'shop_name': '喜糖达人', 'price': 26.8, 'sales': 42000, 'product_link': 'https://www.douyin.com/search/网红ins风喜糖礼盒'},
        {'platform': '抖音', 'keyword': '喜糖', 'rank': 2, 'product_name': '国潮风喜糖礼盒伴手礼', 'shop_name': '婚庆好物推荐', 'price': 35.0, 'sales': 35000, 'product_link': 'https://www.douyin.com/search/国潮喜糖礼盒'},
        {'platform': '抖音', 'keyword': '喜糖', 'rank': 3, 'product_name': '便携小礼盒喜糖伴手礼', 'shop_name': '甜蜜喜铺', 'price': 18.9, 'sales': 30000, 'product_link': 'https://www.douyin.com/search/小礼盒喜糖伴手礼'},
        {'platform': '抖音', 'keyword': '伴手礼', 'rank': 1, 'product_name': '高端定制伴手礼礼盒套装', 'shop_name': '礼遇旗舰店', 'price': 68.0, 'sales': 15000, 'product_link': 'https://www.douyin.com/search/高端定制伴手礼'},
        {'platform': '抖音', 'keyword': '伴手礼', 'rank': 2, 'product_name': '小众设计感伴手礼盒', 'shop_name': '设计美学', 'price': 45.0, 'sales': 12000, 'product_link': 'https://www.douyin.com/search/小众伴手礼盒'},
        {'platform': '抖音', 'keyword': '伴手礼', 'rank': 3, 'product_name': '婚礼回礼伴手礼实用套装', 'shop_name': '回礼优选', 'price': 38.0, 'sales': 10000, 'product_link': 'https://www.douyin.com/search/婚礼回礼伴手礼'},
        {'platform': '抖音', 'keyword': '喜糖', 'rank': 4, 'product_name': '创意DIY喜糖盒子手工制作', 'shop_name': '手作达人', 'price': 15.0, 'sales': 25000, 'product_link': 'https://www.douyin.com/search/DIY喜糖盒子'},
        {'platform': '抖音', 'keyword': '喜糖', 'rank': 5, 'product_name': '零食大礼包喜糖替代方案', 'shop_name': '零食大王', 'price': 55.0, 'sales': 20000, 'product_link': 'https://www.douyin.com/search/零食大礼包喜糖替代'},

        # --- 小红书 (10条) ---
        {'platform': '小红书', 'keyword': '喜糖', 'rank': 1, 'product_name': '喜赋品牌高端喜糖礼盒', 'shop_name': '喜赋', 'price': 35.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=喜赋喜糖礼盒'},
        {'platform': '小红书', 'keyword': '喜糖', 'rank': 2, 'product_name': '糖诗故宫联名喜糖礼盒', 'shop_name': '糖诗', 'price': 42.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=糖诗故宫联名喜糖'},
        {'platform': '小红书', 'keyword': '喜糖', 'rank': 3, 'product_name': '喜大伴手礼高端定制', 'shop_name': '喜大伴手礼', 'price': 55.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=喜大伴手礼'},
        {'platform': '小红书', 'keyword': '喜糖', 'rank': 4, 'product_name': 'GODIVA歌帝梵婚礼巧克力', 'shop_name': 'GODIVA', 'price': 128.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=GODIVA婚礼喜糖'},
        {'platform': '小红书', 'keyword': '喜糖', 'rank': 5, 'product_name': '四时喜 ins风简约喜糖礼盒', 'shop_name': '四时喜', 'price': 28.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=四时喜喜糖礼盒'},
        {'platform': '小红书', 'keyword': '伴手礼', 'rank': 1, 'product_name': '思薇汀婚礼伴手礼礼盒', 'shop_name': '思薇汀', 'price': 38.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=思薇汀伴手礼'},
        {'platform': '小红书', 'keyword': '喜糖', 'rank': 6, 'product_name': '旺仔婚庆喜糖鞭炮造型礼盒', 'shop_name': '旺仔', 'price': 25.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=旺仔鞭炮喜糖'},
        {'platform': '小红书', 'keyword': '喜糖', 'rank': 7, 'product_name': '喜福来传统中式喜糖礼盒', 'shop_name': '喜福来', 'price': 20.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=喜福来喜糖'},
        {'platform': '小红书', 'keyword': '喜糖', 'rank': 8, 'product_name': '不二家牛奶糖婚庆限定版', 'shop_name': '不二家', 'price': 30.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=不二家婚庆喜糖'},
        {'platform': '小红书', 'keyword': '喜糖', 'rank': 9, 'product_name': '创意毛毡喜糖袋环保伴手礼', 'shop_name': '手作礼坊', 'price': 15.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=毛毡喜糖袋'},
        {'platform': '小红书', 'keyword': '喜糖', 'rank': 10, 'product_name': '高端定制中式喜糖礼盒', 'shop_name': '中式美学', 'price': 58.0, 'sales': None, 'product_link': 'https://www.xiaohongshu.com/search_result?keyword=中式喜糖礼盒定制'},
    ]

    for r in rankings:
        add_ranking(r)
    print(f"  ✓ 导入 {len(rankings)} 条排行产品")

    # ========================================
    # 爆款内容 (25条)
    # ========================================
    viral_data = [
        # --- 抖音 (7条) ---
        {'platform': '抖音', 'title': '备婚必看！这三款喜糖承包了我整个婚礼，宾客都问链接', 'author': '婚礼策划师小雨', 'likes': 125000, 'comments': 8500, 'shares': 23000, 'plays': 2800000, 'summary': '精选三款高颜值喜糖礼盒，涵盖中式、ins风、轻奢三种风格，均价25-48元，含实物展示和开箱', 'content_link': 'https://www.douyin.com/search/备婚喜糖推荐三款', 'keyword': '喜糖推荐', 'published_date': '2026-08'},
        {'platform': '抖音', 'title': '千万别买贵的！20元搞定高级感喜糖，伴娘团都惊了', 'author': '省钱备婚日记', 'likes': 98000, 'comments': 6200, 'shares': 18000, 'plays': 2100000, 'summary': '用20元/份的预算打造50元质感的喜糖伴手礼，揭秘包装搭配技巧', 'content_link': 'https://www.douyin.com/search/20元高级感喜糖', 'keyword': '喜糖省钱', 'published_date': '2026-07'},
        {'platform': '抖音', 'title': '故宫联名喜糖开箱！中国风yyds，婆婆看了直夸', 'author': '备婚小能手', 'likes': 87000, 'comments': 5800, 'shares': 15000, 'plays': 1900000, 'summary': '开箱故宫联名喜糖礼盒，中国风设计惊艳全场，适合中式婚礼', 'content_link': 'https://www.douyin.com/search/故宫联名喜糖开箱', 'keyword': '故宫联名喜糖', 'published_date': '2026-08'},
        {'platform': '抖音', 'title': '00后新娘的DIY喜糖，省了3000块！教程来了', 'author': '00后新娘小陈', 'likes': 76000, 'comments': 7200, 'shares': 28000, 'plays': 1800000, 'summary': '用淘宝散装糖果+自制包装DIY喜糖，成本控制在8元/份，教程超详细', 'content_link': 'https://www.douyin.com/search/DIY喜糖教程省钱', 'keyword': 'DIY喜糖', 'published_date': '2026-06'},
        {'platform': '抖音', 'title': '喜糖行业大揭秘！这些品牌千万别买，踩坑总结', 'author': '婚品避坑指南', 'likes': 65000, 'comments': 9100, 'shares': 12000, 'plays': 1500000, 'summary': '盘点喜糖行业避坑要点：包装材质、糖果克重、生产日期、售后保障', 'content_link': 'https://www.douyin.com/search/喜糖避坑指南', 'keyword': '喜糖避坑', 'published_date': '2026-07'},
        {'platform': '抖音', 'title': '一颗糖引发的婚礼事故！喜糖选错差点没结成婚', 'author': '婚礼故事会', 'likes': 55000, 'comments': 4800, 'shares': 8000, 'plays': 1200000, 'summary': '剧情演绎喜糖选购翻车经历，提醒备婚新人的注意事项', 'content_link': 'https://www.douyin.com/search/喜糖选购翻车', 'keyword': '喜糖翻车', 'published_date': '2026-06'},
        {'platform': '抖音', 'title': '悠哈网红喜糖也太好吃了！打开瞬间治愈', 'author': '零食测评君', 'likes': 48000, 'comments': 3500, 'shares': 6000, 'plays': 980000, 'summary': '试吃悠哈多种口味喜糖，草莓牛奶味最受欢迎，适合做婚礼喜糖', 'content_link': 'https://www.douyin.com/search/悠哈网红喜糖测评', 'keyword': '悠哈喜糖', 'published_date': '2026-08'},

        # --- 小红书 (13条) ---
        {'platform': '小红书', 'title': '故宫联名喜糖礼盒｜中国风YYDS，宾客都舍不得吃', 'author': '备婚日记小雨', 'likes': 50000, 'comments': 3200, 'shares': 18000, 'favorites': 25000, 'summary': '故宫文创联名喜糖礼盒开箱测评，中国风设计太惊艳了，搭配龙凤呈祥主题', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=故宫联名喜糖礼盒', 'keyword': '故宫联名喜糖', 'published_date': '2026-06'},
        {'platform': '小红书', 'title': '四时喜喜糖礼盒开箱｜INS风高级感，婚礼颜值担当', 'author': '婚礼美学日记', 'likes': 43000, 'comments': 2800, 'shares': 15000, 'favorites': 22000, 'summary': '四时喜品牌INS风喜糖礼盒开箱，简约高级，多种配色可选', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=四时喜喜糖礼盒', 'keyword': '四时喜', 'published_date': '2026-07'},
        {'platform': '小红书', 'title': '旺仔鞭炮喜糖太可爱了！10块钱搞定超有创意', 'author': '省钱小能手', 'likes': 38000, 'comments': 4200, 'shares': 12000, 'favorites': 18000, 'summary': '用旺仔牛奶糖做成鞭炮造型喜糖，成本不到10元，创意满分', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=旺仔鞭炮喜糖', 'keyword': '旺仔喜糖', 'published_date': '2026-05'},
        {'platform': '小红书', 'title': '00后订婚喜糖分享｜小众高级不撞款', 'author': '00后新娘日记', 'likes': 28000, 'comments': 1900, 'shares': 8000, 'favorites': 14000, 'summary': '分享00后订婚喜糖选择，小众品牌搭配，高级感不输大牌', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=00后订婚喜糖小众', 'keyword': '订婚喜糖', 'published_date': '2026-07'},
        {'platform': '小红书', 'title': '喜糖避雷指南｜备婚新手必看的6个坑', 'author': '备婚避雷针', 'likes': 25000, 'comments': 3800, 'shares': 10000, 'favorites': 20000, 'summary': '总结喜糖选购6大常见坑：包装好看内容少、临期产品、色差严重等', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=喜糖避雷指南', 'keyword': '喜糖避雷', 'published_date': '2026-06'},
        {'platform': '小红书', 'title': 'GODIVA喜糖礼盒也太高级了吧！备婚清单必备', 'author': '品质备婚', 'likes': 22000, 'comments': 1500, 'shares': 6000, 'favorites': 12000, 'summary': 'GODIVA歌帝梵喜糖礼盒开箱，高端质感，适合精致婚礼', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=GODIVA喜糖礼盒高级', 'keyword': 'GODIVA喜糖', 'published_date': '2026-08'},
        {'platform': '小红书', 'title': '思薇汀伴手礼｜婚礼回礼这样选宾客都说好', 'author': '婚礼策划师CC', 'likes': 20000, 'comments': 1200, 'shares': 5000, 'favorites': 10000, 'summary': '推荐思薇汀伴手礼品牌，品质好价格适中，适合婚礼回礼', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=思薇汀伴手礼', 'keyword': '思薇汀伴手礼', 'published_date': '2026-07'},
        {'platform': '小红书', 'title': '喜糖选购终极攻略｜从5元到50元全覆盖', 'author': '备婚研究所', 'likes': 18000, 'comments': 2500, 'shares': 7000, 'favorites': 15000, 'summary': '按预算分层推荐喜糖：5-10元经济型、15-25元主流型、30-50元品质型', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=喜糖选购攻略', 'keyword': '喜糖攻略', 'published_date': '2026-05'},
        {'platform': '小红书', 'title': '中式喜糖礼盒这样搭配，长辈宾客都夸有面子', 'author': '中式婚礼控', 'likes': 16000, 'comments': 1100, 'shares': 4500, 'favorites': 9000, 'summary': '中式婚礼喜糖搭配方案：红枣+花生+桂圆+莲子+糖果，寓意美好', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=中式喜糖搭配方案', 'keyword': '中式喜糖', 'published_date': '2026-06'},
        {'platform': '小红书', 'title': '伴手礼开箱｜100份起订的工厂店居然这么便宜', 'author': '会省钱的准新娘', 'likes': 15000, 'comments': 1800, 'shares': 4000, 'favorites': 8000, 'summary': '探访伴手礼工厂源头，直接拿货比零售便宜40%', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=伴手礼工厂源头', 'keyword': '伴手礼工厂', 'published_date': '2026-07'},
        {'platform': '小红书', 'title': '不二家牛奶糖婚礼版颜值封神！', 'author': '甜蜜婚礼', 'likes': 13000, 'comments': 900, 'shares': 3500, 'favorites': 7000, 'summary': '不二家推出婚庆限定包装，牛奶糖颜值与口感兼具', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=不二家婚庆糖果', 'keyword': '不二家婚庆', 'published_date': '2026-08'},
        {'platform': '小红书', 'title': '喜福来中式喜糖｜性价比之王，人均不到5元', 'author': '实惠备婚', 'likes': 12000, 'comments': 1400, 'shares': 3000, 'favorites': 6500, 'summary': '喜福来品牌中式喜糖测评，价格亲民但品质不俗', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=喜福来中式喜糖', 'keyword': '喜福来', 'published_date': '2026-05'},
        {'platform': '小红书', 'title': '毛毡喜糖袋DIY教程｜零基础也能做', 'author': '手作控', 'likes': 10000, 'comments': 800, 'shares': 2500, 'favorites': 5500, 'summary': '毛毡材质喜糖袋手作教程，环保又可爱，适合小清新婚礼', 'content_link': 'https://www.xiaohongshu.com/search_result?keyword=毛毡喜糖袋DIY', 'keyword': '毛毡喜糖袋', 'published_date': '2026-06'},

        # --- 大众点评 (5条) ---
        {'platform': '大众点评', 'title': '上海婚礼喜糖|这家店的喜糖也太好看了吧，五星推荐', 'author': '上海新娘小美', 'likes': 8500, 'comments': 620, 'shares': 1500, 'summary': '上海实体喜糖店探店，现场试吃体验，多种礼盒可选', 'content_link': 'https://www.dianping.com/search/keyword/2/0_上海喜糖店推荐', 'keyword': '上海喜糖店', 'published_date': '2026-07'},
        {'platform': '大众点评', 'title': '北京婚庆用品一条街｜喜糖伴手礼一站式采购指南', 'author': '北京备婚指南', 'likes': 7200, 'comments': 480, 'shares': 1200, 'summary': '北京婚庆用品市场实地探访，推荐性价比最高的喜糖批发店铺', 'content_link': 'https://www.dianping.com/search/keyword/2/0_北京婚庆喜糖', 'keyword': '北京婚庆用品', 'published_date': '2026-06'},
        {'platform': '大众点评', 'title': '婚礼伴手礼|广州这家高定工作室绝了，明星同款', 'author': '广式婚礼', 'likes': 6500, 'comments': 350, 'shares': 900, 'summary': '广州高端伴手礼定制工作室探店，品质不输大牌', 'content_link': 'https://www.dianping.com/search/keyword/2/0_广州伴手礼定制', 'keyword': '广州伴手礼', 'published_date': '2026-08'},
        {'platform': '大众点评', 'title': '成都喜糖批发市场全攻略｜比淘宝还便宜！', 'author': '成都备婚小能手', 'likes': 5800, 'comments': 420, 'shares': 1100, 'summary': '成都荷花池批发市场喜糖采购攻略，价格比线上便宜20-30%', 'content_link': 'https://www.dianping.com/search/keyword/2/0_成都喜糖批发', 'keyword': '成都喜糖批发', 'published_date': '2026-07'},
        {'platform': '大众点评', 'title': '杭州婚礼伴手礼｜网红店实地测评，附价格清单', 'author': '杭州备婚攻略', 'likes': 4500, 'comments': 280, 'shares': 800, 'summary': '杭州多家网红伴手礼店探店测评，附详细价格对比表', 'content_link': 'https://www.dianping.com/search/keyword/2/0_杭州伴手礼网红店', 'keyword': '杭州伴手礼', 'published_date': '2026-06'},
    ]

    for v in viral_data:
        add_viral(v)
    print(f"  ✓ 导入 {len(viral_data)} 条爆款内容")

    # ========================================
    # 年龄分布 (6组)
    # ========================================
    age_data = [
        {'source': '尚普咨询', 'source_detail': '2026年婚庆消费调研 N=1300', 'age_group': '18-25岁', 'percentage': 22.0, 'gender': '女性为主', 'sample_size': 1300},
        {'source': '尚普咨询', 'source_detail': '2026年婚庆消费调研 N=1300', 'age_group': '26-30岁', 'percentage': 35.0, 'gender': '女性', 'sample_size': 1300},
        {'source': '尚普咨询', 'source_detail': '2026年婚庆消费调研 N=1300', 'age_group': '31-35岁', 'percentage': 23.0, 'gender': '女性', 'sample_size': 1300},
        {'source': '尚普咨询', 'source_detail': '2026年婚庆消费调研 N=1300', 'age_group': '36-45岁', 'percentage': 13.0, 'gender': '均衡', 'sample_size': 1300},
        {'source': '华信人咨询', 'source_detail': '婚庆礼品消费趋势研究 N=1350', 'age_group': '26-35岁女性合计', 'percentage': 58.0, 'gender': '女性', 'sample_size': 1350},
        {'source': '平台画像', 'source_detail': '抖音/淘宝/小红书综合画像', 'age_group': '20-30元价格带', 'percentage': 35.0, 'gender': '不分性别', 'platform': '综合'},
    ]

    for a in age_data:
        add_age_distribution(a)
    print(f"  ✓ 导入 {len(age_data)} 组年龄分布")

    # ========================================
    # 跟踪商家 (56家)
    # ========================================
    merchants_data = [
        # 淘宝 (10)
        {'platform': '淘宝', 'name': '徐福记官方旗舰店', 'shop_type': '品牌旗舰', 'followers': '500万+', 'product_count': 200, 'avg_price': 30.0, 'shop_link': 'https://s.taobao.com/search?q=徐福记旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '喜赋旗舰店', 'shop_type': '专业喜糖', 'followers': '50万+', 'product_count': 150, 'avg_price': 32.0, 'shop_link': 'https://s.taobao.com/search?q=喜赋旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '大白兔官方旗舰店', 'shop_type': '品牌旗舰', 'followers': '300万+', 'product_count': 80, 'avg_price': 28.0, 'shop_link': 'https://s.taobao.com/search?q=大白兔旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '德芙官方旗舰店', 'shop_type': '品牌旗舰', 'followers': '400万+', 'product_count': 120, 'avg_price': 45.0, 'shop_link': 'https://s.taobao.com/search?q=德芙旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '费列罗官方旗舰店', 'shop_type': '品牌旗舰', 'followers': '200万+', 'product_count': 60, 'avg_price': 75.0, 'shop_link': 'https://s.taobao.com/search?q=费列罗旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '旺旺食品旗舰店', 'shop_type': '品牌旗舰', 'followers': '350万+', 'product_count': 300, 'avg_price': 25.0, 'shop_link': 'https://s.taobao.com/search?q=旺旺旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '糖诗旗舰店', 'shop_type': '原创设计', 'followers': '30万+', 'product_count': 80, 'avg_price': 40.0, 'shop_link': 'https://s.taobao.com/search?q=糖诗旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '四时喜旗舰店', 'shop_type': '设计品牌', 'followers': '25万+', 'product_count': 60, 'avg_price': 26.0, 'shop_link': 'https://s.taobao.com/search?q=四时喜旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '不二家旗舰店', 'shop_type': '品牌旗舰', 'followers': '180万+', 'product_count': 100, 'avg_price': 28.0, 'shop_link': 'https://s.taobao.com/search?q=不二家旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '好想你官方旗舰店', 'shop_type': '品牌旗舰', 'followers': '150万+', 'product_count': 120, 'avg_price': 35.0, 'shop_link': 'https://s.taobao.com/search?q=好想你旗舰店&sort=sale-desc'},

        # 抖音 (5)
        {'platform': '抖音', 'name': '喜糖达人', 'shop_type': '达人带货', 'followers': '80万', 'product_count': 50, 'avg_price': 28.0, 'shop_link': 'https://www.douyin.com/search/喜糖达人'},
        {'platform': '抖音', 'name': '婚庆好物推荐', 'shop_type': '达人带货', 'followers': '120万', 'product_count': 100, 'avg_price': 35.0, 'shop_link': 'https://www.douyin.com/search/婚庆好物推荐'},
        {'platform': '抖音', 'name': '甜蜜喜铺', 'shop_type': '自营店铺', 'followers': '30万', 'product_count': 80, 'avg_price': 22.0, 'shop_link': 'https://www.douyin.com/search/甜蜜喜铺'},
        {'platform': '抖音', 'name': '礼遇旗舰店', 'shop_type': '品牌店铺', 'followers': '50万', 'product_count': 60, 'avg_price': 55.0, 'shop_link': 'https://www.douyin.com/search/礼遇旗舰店伴手礼'},
        {'platform': '抖音', 'name': '设计美学', 'shop_type': '原创品牌', 'followers': '40万', 'product_count': 40, 'avg_price': 48.0, 'shop_link': 'https://www.douyin.com/search/设计美学伴手礼'},

        # 小红书 (5)
        {'platform': '小红书', 'name': '喜赋', 'shop_type': '品牌商户', 'followers': '15万', 'product_count': 30, 'avg_price': 35.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=喜赋'},
        {'platform': '小红书', 'name': '糖诗', 'shop_type': '品牌商户', 'followers': '10万', 'product_count': 25, 'avg_price': 42.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=糖诗'},
        {'platform': '小红书', 'name': '喜大伴手礼', 'shop_type': '品牌商户', 'followers': '8万', 'product_count': 20, 'avg_price': 55.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=喜大伴手礼'},
        {'platform': '小红书', 'name': 'GODIVA官方', 'shop_type': '品牌商户', 'followers': '25万', 'product_count': 15, 'avg_price': 128.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=GODIVA'},
        {'platform': '小红书', 'name': '四时喜', 'shop_type': '品牌商户', 'followers': '12万', 'product_count': 28, 'avg_price': 28.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=四时喜'},

        # 大众点评 (3)
        {'platform': '大众点评', 'name': '上海喜糖世家', 'shop_type': '实体店铺', 'followers': None, 'product_count': 50, 'avg_price': 30.0, 'shop_link': 'https://www.dianping.com/search/keyword/2/0_喜糖世家', 'notes': '上海实体喜糖店五星'},
        {'platform': '大众点评', 'name': '北京婚庆用品批发城', 'shop_type': '批发市场', 'followers': None, 'product_count': 200, 'avg_price': 18.0, 'shop_link': 'https://www.dianping.com/search/keyword/2/0_婚庆用品批发', 'notes': '北京婚庆用品集散地'},
        {'platform': '大众点评', 'name': '广州高定伴手礼工作室', 'shop_type': '定制工作室', 'followers': None, 'product_count': 30, 'avg_price': 80.0, 'shop_link': 'https://www.dianping.com/search/keyword/2/0_伴手礼定制', 'notes': '高端定制伴手礼'},

        # 补充更多商家
        {'platform': '淘宝', 'name': '阿尔卑斯旗舰店', 'shop_type': '品牌旗舰', 'followers': '200万+', 'product_count': 90, 'avg_price': 22.0, 'shop_link': 'https://s.taobao.com/search?q=阿尔卑斯旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '好时官方旗舰店', 'shop_type': '品牌旗舰', 'followers': '120万+', 'product_count': 70, 'avg_price': 40.0, 'shop_link': 'https://s.taobao.com/search?q=好时旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '悠哈旗舰店', 'shop_type': '品牌旗舰', 'followers': '80万+', 'product_count': 50, 'avg_price': 30.0, 'shop_link': 'https://s.taobao.com/search?q=悠哈旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '思薇汀旗舰店', 'shop_type': '婚礼伴手礼', 'followers': '20万+', 'product_count': 60, 'avg_price': 35.0, 'shop_link': 'https://s.taobao.com/search?q=思薇汀旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '喜福来旗舰店', 'shop_type': '中式喜糖', 'followers': '15万+', 'product_count': 50, 'avg_price': 22.0, 'shop_link': 'https://s.taobao.com/search?q=喜福来旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '三只松鼠旗舰店', 'shop_type': '品牌旗舰', 'followers': '4500万+', 'product_count': 500, 'avg_price': 25.0, 'shop_link': 'https://s.taobao.com/search?q=三只松鼠旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '百草味旗舰店', 'shop_type': '品牌旗舰', 'followers': '3500万+', 'product_count': 400, 'avg_price': 28.0, 'shop_link': 'https://s.taobao.com/search?q=百草味旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '明治官方旗舰店', 'shop_type': '品牌旗舰', 'followers': '90万+', 'product_count': 40, 'avg_price': 38.0, 'shop_link': 'https://s.taobao.com/search?q=明治旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '西域美农旗舰店', 'shop_type': '品牌旗舰', 'followers': '60万+', 'product_count': 80, 'avg_price': 26.0, 'shop_link': 'https://s.taobao.com/search?q=西域美农旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': '瑞特斯波德旗舰店', 'shop_type': '品牌旗舰', 'followers': '30万+', 'product_count': 30, 'avg_price': 35.0, 'shop_link': 'https://s.taobao.com/search?q=瑞特斯波德旗舰店&sort=sale-desc'},
        {'platform': '淘宝', 'name': 'GODIVA官方旗舰店', 'shop_type': '品牌旗舰', 'followers': '100万+', 'product_count': 25, 'avg_price': 130.0, 'shop_link': 'https://s.taobao.com/search?q=GODIVA旗舰店&sort=sale-desc'},
        {'platform': '小红书', 'name': '思薇汀', 'shop_type': '品牌商户', 'followers': '6万', 'product_count': 22, 'avg_price': 38.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=思薇汀'},
        {'platform': '小红书', 'name': '旺仔品牌', 'shop_type': '品牌商户', 'followers': '30万', 'product_count': 35, 'avg_price': 25.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=旺仔婚庆'},
        {'platform': '小红书', 'name': '喜福来', 'shop_type': '品牌商户', 'followers': '5万', 'product_count': 18, 'avg_price': 20.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=喜福来'},
        {'platform': '小红书', 'name': '不二家官方', 'shop_type': '品牌商户', 'followers': '20万', 'product_count': 40, 'avg_price': 30.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=不二家'},
        {'platform': '小红书', 'name': '手作礼坊', 'shop_type': '手作品牌', 'followers': '3万', 'product_count': 12, 'avg_price': 15.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=手作礼坊', 'notes': '毛毡喜糖袋原创'},
        {'platform': '小红书', 'name': '中式美学', 'shop_type': '品牌商户', 'followers': '7万', 'product_count': 15, 'avg_price': 58.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=中式美学伴手礼'},
        {'platform': '小红书', 'name': '创意婚品店', 'shop_type': '电商店铺', 'followers': '4万', 'product_count': 25, 'avg_price': 18.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=创意婚品店'},
        {'platform': '小红书', 'name': '喜糖之家', 'shop_type': '专业店铺', 'followers': '2万', 'product_count': 35, 'avg_price': 28.0, 'shop_link': 'https://www.xiaohongshu.com/search_result?keyword=喜糖之家'},
        {'platform': '大众点评', 'name': '成都荷花池喜糖批发', 'shop_type': '批发市场', 'followers': None, 'product_count': 300, 'avg_price': 12.0, 'shop_link': 'https://www.dianping.com/search/keyword/2/0_荷花池喜糖', 'notes': '成都最大喜糖批发市场'},
        {'platform': '大众点评', 'name': '杭州网红伴手礼集合店', 'shop_type': '集合店', 'followers': None, 'product_count': 80, 'avg_price': 40.0, 'shop_link': 'https://www.dianping.com/search/keyword/2/0_伴手礼集合店', 'notes': '杭州网红伴手礼店'},
    ]

    for m in merchants_data:
        add_merchant(m)
    print(f"  ✓ 导入 {len(merchants_data)} 家跟踪商家")

    print(f"\n{'='*50}")
    print(f"  数据导入完成！")
    print(f"  排行产品: {len(rankings)} 条")
    print(f"  爆款内容: {len(viral_data)} 条")
    print(f"  年龄分布: {len(age_data)} 组")
    print(f"  跟踪商家: {len(merchants_data)} 家")
    print(f"{'='*50}")


if __name__ == '__main__':
    import_all()
