#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 服务模块 - 统一模型路由 + 真实 API 调用
所有 API Key 从环境变量读取，前端不暴露
支持 7 种免费模型 + 自动降级
"""
import os
import json
import random
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

# =============================================================================
# 模型配置 — 统一 OpenAI SDK 兼容格式
# =============================================================================

MODEL_CONFIGS = {
    'deepseek': {
        'name': 'DeepSeek V3.1',
        'model_id': 'deepseek-chat',
        'base_url': 'https://api.deepseek.com/v1',
        'api_key_env': 'DEEPSEEK_API_KEY',
        'free_quota': '注册送500万token',
        'context': '64K',
        'emoji': '🔵',
    },
    'doubao': {
        'name': '豆包 Pro',
        'model_id': 'doubao-pro-32k',
        'base_url': 'https://ark.cn-beijing.volces.com/api/v3',
        'api_key_env': 'DOUBAO_API_KEY',
        'free_quota': '免费额度充足',
        'context': '32K',
        'emoji': '🟣',
    },
    'qwen': {
        'name': '通义千问 Qwen3-Plus',
        'model_id': 'qwen-plus',
        'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'api_key_env': 'QWEN_API_KEY',
        'free_quota': '百万token免费',
        'context': '128K',
        'emoji': '🔷',
    },
    'kimi': {
        'name': 'Kimi (Moonshot)',
        'model_id': 'moonshot-v1-8k',
        'base_url': 'https://api.moonshot.cn/v1',
        'api_key_env': 'KIMI_API_KEY',
        'free_quota': '128K上下文',
        'context': '128K',
        'emoji': '🟢',
    },
    'gemini': {
        'name': 'Gemini 2.0 Flash',
        'model_id': 'gemini-2.0-flash',
        'base_url': 'https://generativelanguage.googleapis.com/v1beta/openai',
        'api_key_env': 'GEMINI_API_KEY',
        'free_quota': '1500次/天',
        'context': '128K',
        'emoji': '🟡',
    },
    'openai': {
        'name': 'GPT-4o-mini',
        'model_id': 'gpt-4o-mini',
        'base_url': 'https://api.openai.com/v1',
        'api_key_env': 'OPENAI_API_KEY',
        'free_quota': '注册送$5',
        'context': '128K',
        'emoji': '🟩',
    },
    'yi': {
        'name': 'Yi-Large',
        'model_id': 'yi-large',
        'base_url': 'https://api.lingyiwanwu.com/v1',
        'api_key_env': 'YI_API_KEY',
        'free_quota': '免费额度',
        'context': '32K',
        'emoji': '💗',
    },
}

# 默认降级顺序
FALLBACK_ORDER = ['deepseek', 'doubao', 'qwen', 'kimi', 'gemini', 'openai', 'yi']


def get_available_models():
    """返回已配置 API Key 的模型列表"""
    available = []
    order = os.environ.get('MODEL_FALLBACK_ORDER', '').split(',')
    if not order or order == ['']:
        order = FALLBACK_ORDER

    for model_id in order:
        model_id = model_id.strip()
        if model_id in MODEL_CONFIGS:
            cfg = MODEL_CONFIGS[model_id]
            has_key = bool(os.environ.get(cfg['api_key_env']))
            available.append({
                'id': model_id,
                'name': cfg['name'],
                'emoji': cfg['emoji'],
                'free_quota': cfg['free_quota'],
                'context': cfg['context'],
                'configured': has_key,
            })
    return available


def get_client(model):
    """根据模型 ID 获取 OpenAI 客户端"""
    if model not in MODEL_CONFIGS:
        model = FALLBACK_ORDER[0]

    cfg = MODEL_CONFIGS[model]
    api_key = os.environ.get(cfg['api_key_env'])

    if not api_key:
        raise ValueError(f"模型 {cfg['name']} 未配置 API Key，请设置环境变量 {cfg['api_key_env']}")

    return OpenAI(
        api_key=api_key,
        base_url=cfg['base_url'],
    ), cfg['model_id']


def call_ai(model, messages, temperature=0.8, max_tokens=2048):
    """
    调用 AI 模型，自动降级
    返回 (success, content, model_used, tokens)
    """
    # 确定调用顺序
    order = os.environ.get('MODEL_FALLBACK_ORDER', '').split(',')
    if not order or order == ['']:
        order = FALLBACK_ORDER

    # 如果指定了具体模型，优先尝试
    if model and model in MODEL_CONFIGS:
        order = [model] + [m for m in order if m != model]

    last_error = None

    for try_model in order:
        try_model = try_model.strip()
        if try_model not in MODEL_CONFIGS:
            continue

        cfg = MODEL_CONFIGS[try_model]
        api_key = os.environ.get(cfg['api_key_env'])
        if not api_key:
            continue

        try:
            client = OpenAI(api_key=api_key, base_url=cfg['base_url'])
            response = client.chat.completions.create(
                model=cfg['model_id'],
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content
            tokens = {
                'input': response.usage.prompt_tokens if response.usage else 0,
                'output': response.usage.completion_tokens if response.usage else 0,
                'total': response.usage.total_tokens if response.usage else 0,
            }

            return True, content, cfg['name'], tokens

        except Exception as e:
            last_error = str(e)
            logger.warning(f"模型 {cfg['name']} 调用失败: {e}，尝试下一个...")
            continue

    return False, f"所有模型调用均失败。最后错误: {last_error}", None, None


# =============================================================================
# 图片生成 — 多引擎降级
# =============================================================================

STYLE_PROMPTS = {
    '写实': 'photorealistic, 8k, highly detailed, professional photography, studio lighting',
    '插画': 'beautiful illustration, digital art, vibrant colors, trending on artstation',
    '国风': 'traditional Chinese art style, ink wash painting, elegant, cultural, red and gold',
    'ins风': 'instagram aesthetic, minimalist, warm tones, lifestyle photography',
    '产品图': 'product photography, studio lighting, white background, commercial photography',
}


def generate_image(prompt, style='写实', size='1024x1024'):
    """
    图片生成，引擎降级链：
    Stability AI → Pollinations (免费) → Cloudflare
    """
    style_prefix = STYLE_PROMPTS.get(style, STYLE_PROMPTS['写实'])
    full_prompt = f"{prompt}, {style_prefix}"

    w, h = size.split('x')

    # 方案1: Stability AI
    api_key = os.environ.get('STABILITY_API_KEY')
    if api_key:
        try:
            import httpx
            resp = httpx.post(
                'https://api.stability.ai/v2beta/stable-image/generate/core',
                headers={'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'},
                files={'none': ''},
                data={'prompt': full_prompt, 'output_format': 'png'},
                timeout=120,
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get('image'):
                    return {'success': True, 'image_url': f"data:image/png;base64,{data['image']}", 'engine': 'Stability AI'}
        except Exception as e:
            logger.warning(f"Stability AI 失败: {e}")

    # 方案2: Pollinations.ai (免费，不限量)
    try:
        import urllib.parse
        encoded = urllib.parse.quote(full_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width={w}&height={h}&nologo=true&seed={random.randint(1, 99999)}"
        return {'success': True, 'image_url': url, 'engine': 'Pollinations.ai (免费)'}
    except Exception as e:
        logger.warning(f"Pollinations 失败: {e}")

    return {'success': False, 'error': '所有图片引擎均不可用'}


# =============================================================================
# 小红书文案 Prompt
# =============================================================================

XHS_SYSTEM_PROMPT = """你是一位小红书爆款文案专家，擅长撰写高互动率的种草内容。
创作原则：
1. 标题用 emoji 开头，15-25字，有冲击力
2. 开篇用个人体验引入，像朋友分享
3. 正文分点列出亮点，每点配上使用感受
4. 语气亲切自然，避免官方宣传感
5. 文末加 5-8 个热门话题标签
6. 结尾加互动引导"""


def generate_xiaohongshu(product, style='种草', word_count='medium', model='deepseek'):
    """生成小红书文案（真 AI 调用）"""
    word_map = {'short': '150字', 'medium': '300字', 'long': '500字'}

    prompt = f"""请为产品「{product}」撰写一篇小红书{style}类文案。

要求：
- 字数控制：约{word_map.get(word_count, '300字')}
- 风格：{style}
- 标题格式：emoji开头 + 吸引眼球（15-25字）
- 正文分点列出产品亮点
- 添加5-8个热门话题标签
- 语气轻松自然，像闺蜜分享

输出格式：
【标题】
（标题内容）

【正文】
（正文内容）

【标签】
（话题标签）"""

    messages = [
        {'role': 'system', 'content': XHS_SYSTEM_PROMPT},
        {'role': 'user', 'content': prompt},
    ]

    success, content, model_used, tokens = call_ai(model, messages, temperature=0.85, max_tokens=2048)

    if success:
        return {'success': True, 'full': content, 'model_used': model_used, 'tokens': tokens}

    # AI 调用失败，回退到模板
    return _generate_xhs_fallback(product, style, word_count)


def _generate_xhs_fallback(product, style, word_count):
    """小红书文案模板回退"""
    titles = {
        '种草': f'备婚必看！{product}这样选宾客都夸爆了',
        '测评': f'花了3000实测12款{product}，结果出乎意料',
        '攻略': f'备婚干货｜{product}避雷指南建议收藏',
        '分享': f'被问爆的{product}链接今天终于整理好了',
        '探店': f'跑遍5家{product}店终于找到心仪的',
    }
    body = f'分享一款超好看的{product}🔥\n\n颜值高、性价比好，宾客反馈超棒！\n\n备婚的姐妹闭眼入～'
    tags = '#备婚 #备婚日记 #喜糖 #好物推荐 #婚礼筹备 #备婚好物'
    return {
        'success': True,
        'full': f"{titles.get(style, titles['种草'])}\n\n{body}\n\n{tags}",
        'model_used': '模板回退（无API Key）',
        'tokens': None,
    }


# =============================================================================
# 抖音脚本 Prompt
# =============================================================================

DOUYIN_SYSTEM_PROMPT = """你是一位抖音短视频爆款编导，精通短视频脚本创作。
要求：
1. 黄金3秒 Hook 必须抓人
2. 分镜脚本用表格格式输出
3. 节奏紧凑，适合短视频
4. 给出 BGM 建议
5. 添加热门话题标签"""


def generate_douyin(product, content_type='展示', duration='medium', model='deepseek'):
    """生成抖音脚本（真 AI 调用）"""
    duration_map = {'short': '30秒', 'medium': '60秒', 'long': '90秒'}

    prompt = f"""请为产品「{product}」创作一份抖音短视频脚本。

类型：{content_type}
时长：{duration_map.get(duration, '60秒')}

输出格式（表格）：
| 镜号 | 时长 | 画面描述 | 台词/旁白 | 备注 |

要求：
1. 黄金3秒Hook必须抓人（前3秒决定完播率）
2. 每个镜头不超过5秒
3. 节奏紧凑，不要拖沓
4. 最后加 BGM 推荐和热门话题标签"""

    messages = [
        {'role': 'system', 'content': DOUYIN_SYSTEM_PROMPT},
        {'role': 'user', 'content': prompt},
    ]

    success, content, model_used, tokens = call_ai(model, messages, temperature=0.9, max_tokens=2048)

    if success:
        return {'success': True, 'full': content, 'model_used': model_used, 'tokens': tokens}

    return _generate_dy_fallback(product, content_type, duration)


def _generate_dy_fallback(product, content_type, duration):
    """抖音脚本模板回退"""
    hooks = {
        '展示': f'你敢信？这个{product}让婚礼预算省了一半！',
        '口播': f'备婚的姐妹听我一句劝，{product}千万别乱买！',
        '剧情': f'当我把这个{product}拿给婆婆看...',
        '痛点': f'花了3000买{product}，我后悔了...',
        '开箱': f'快递到了！今天开箱最近超火的{product}',
    }
    script = f"""| 镜号 | 时长 | 画面描述 | 台词 | 备注 |
| 1 | 3秒 | {product}特写 | {hooks.get(content_type, hooks['展示'])} | Hook |
| 2 | 5秒 | 产品展示全景 | 来看这款{product}的细节 | 中景 |
| 3 | 5秒 | 使用场景 | 真的超出预期 | 特写 |
| 4 | 3秒 | 结尾CTA | 闭眼入！ | 引导关注 |"""
    full = f"""🎣 Hook: {hooks.get(content_type, hooks['展示'])}

📜 分镜脚本：
{script}

🎵 BGM建议：轻快鼓点 / 温馨钢琴
🏷️ #备婚 #喜糖 #婚礼好物 #抖音好物推荐"""
    return {
        'success': True,
        'full': full,
        'model_used': '模板回退（无API Key）',
        'tokens': None,
    }
