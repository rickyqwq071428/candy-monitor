#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 统一模型路由层
所有模型用 OpenAI SDK 兼容格式封装，只需切换 base_url + api_key
失败自动降级：主模型不可用时自动尝试备用模型
"""

import os
import json
import uuid
import random
import logging
import base64 as b64
import urllib.parse
from openai import OpenAI
import httpx

logger = logging.getLogger(__name__)

# =============================================================================
# 一、文案模型配置（6个，全部 OpenAI SDK 兼容）
# =============================================================================

TEXT_MODELS = {
    'deepseek': {
        'name': 'DeepSeek V3',
        'model_id': 'deepseek-chat',
        'base_url': os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1'),
        'api_key': os.getenv('DEEPSEEK_API_KEY'),
        'free_quota': '注册送500万token',
        'context': '64K',
        'emoji': '🔵',
        'recommended': True,
    },
    'doubao': {
        'name': '豆包 Pro',
        'model_id': 'doubao-pro-32k',
        'base_url': os.getenv('DOUBAO_BASE_URL', 'https://ark.cn-beijing.volces.com/api/v3'),
        'api_key': os.getenv('DOUBAO_API_KEY'),
        'free_quota': '免费额度充足',
        'context': '32K',
        'emoji': '🟣',
        'recommended': False,
    },
    'qwen': {
        'name': '通义千问 Qwen3',
        'model_id': 'qwen-plus',
        'base_url': os.getenv('QWEN_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1'),
        'api_key': os.getenv('QWEN_API_KEY'),
        'free_quota': '百万token免费',
        'context': '128K',
        'emoji': '🔷',
        'recommended': False,
    },
    'kimi': {
        'name': 'Kimi',
        'model_id': 'moonshot-v1-8k',
        'base_url': os.getenv('KIMI_BASE_URL', 'https://api.moonshot.cn/v1'),
        'api_key': os.getenv('KIMI_API_KEY'),
        'free_quota': '注册送额度',
        'context': '128K',
        'emoji': '🟢',
        'recommended': False,
    },
    'gemini': {
        'name': 'Gemini 2.0 Flash',
        'model_id': 'gemini-2.0-flash',
        'base_url': os.getenv('GEMINI_BASE_URL', 'https://generativelanguage.googleapis.com/v1beta/openai'),
        'api_key': os.getenv('GEMINI_API_KEY'),
        'free_quota': '1500次/天',
        'context': '128K',
        'emoji': '🟡',
        'recommended': False,
    },
    'gpt4o_mini': {
        'name': 'GPT-4o-mini',
        'model_id': 'gpt-4o-mini',
        'base_url': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
        'api_key': os.getenv('OPENAI_API_KEY'),
        'free_quota': '注册送$5',
        'context': '128K',
        'emoji': '🟩',
        'recommended': False,
    },
}

# 默认降级顺序
TEXT_FALLBACK = ['deepseek', 'doubao', 'qwen', 'kimi', 'gemini', 'gpt4o_mini']


# =============================================================================
# 二、图片模型配置（3个）
# =============================================================================

IMAGE_MODELS = {
    'flux_schnell': {
        'name': 'Cloudflare Flux.1 Schnell',
        'model_id': '@cf/black-forest-labs/flux-schnell',
        'type': 'cloudflare',
        'api_key': os.getenv('CLOUDFLARE_API_KEY'),
        'account_id': os.getenv('CLOUDFLARE_ACCOUNT_ID'),
        'free_quota': '300次/天',
        'emoji': '☁️',
        'recommended': True,
    },
    'janus': {
        'name': 'DeepSeek Janus',
        'model_id': 'deepseek-ai/Janus-1.3B',
        'type': 'huggingface',
        'api_key': os.getenv('HF_API_KEY'),
        'free_quota': '免费tier',
        'emoji': '🤖',
        'recommended': False,
    },
    'sdxl': {
        'name': 'Stable Diffusion XL',
        'model_id': 'stabilityai/stable-diffusion-xl-base-1.0',
        'type': 'huggingface',
        'api_key': os.getenv('HF_API_KEY'),
        'free_quota': '免费tier',
        'emoji': '🎨',
        'recommended': False,
    },
}

IMAGE_FALLBACK = ['flux_schnell', 'janus', 'sdxl']


# =============================================================================
# 三、视频模型配置（2个）
# =============================================================================

VIDEO_MODELS = {
    'cogvideo': {
        'name': 'CogVideoX-2B',
        'model_id': 'THUDM/CogVideoX-2b',
        'type': 'huggingface',
        'api_key': os.getenv('HF_API_KEY'),
        'free_quota': '免费tier',
        'emoji': '🎬',
        'recommended': True,
    },
    'svd': {
        'name': 'Stable Video Diffusion',
        'model_id': 'stabilityai/stable-video-diffusion-img2vid',
        'type': 'huggingface',
        'api_key': os.getenv('HF_API_KEY'),
        'free_quota': '免费tier',
        'emoji': '📹',
        'recommended': False,
    },
}

VIDEO_FALLBACK = ['cogvideo', 'svd']


# =============================================================================
# 四、风格 Prompt 映射
# =============================================================================

IMAGE_STYLE_PROMPTS = {
    '写实': 'photorealistic, 8k, highly detailed, professional photography',
    '插画': 'beautiful illustration, digital art, vibrant colors, trending on artstation',
    '国风': 'traditional Chinese art style, ink painting, elegant, cultural elegance',
    'ins风': 'instagram aesthetic, minimalist, warm tones, lifestyle photography',
    '产品图': 'product photography, studio lighting, white background, commercial',
}

VIDEO_STYLE_PROMPTS = {
    '实拍风': 'cinematic, photorealistic, natural lighting, 24fps film look',
    '动漫风': 'anime style, vibrant colors, smooth animation, 2D cel-shaded',
    '产品展示': 'product showcase, clean background, smooth camera movement, commercial',
    '抽象艺术': 'abstract art, flowing colors, experimental, artistic visuals',
}

XHS_STYLES = {
    '种草测评': '以真实用户的语气分享使用体验，突出产品优点，让人想立刻购买',
    '好物分享': '像闺蜜推荐好物的语气，轻松自然，分享为什么觉得这个产品值得',
    '避坑指南': '以过来人身份揭露行业套路，告诉读者怎么选、怎么避坑',
    '教程攻略': '干货导向，步骤清晰，教读者怎么用、怎么搭配、怎么选',
    'Vlog脚本': '生活化叙事，带场景感，像在看一段生活短片',
}

DY_STYLES = {
    '开箱测评': '开箱第一视角，制造悬念，逐层揭晓产品细节',
    '教程干货': '步骤清晰的教学，Quick Tip 风格，信息密度高',
    '剧情反转': '设计一个小情节，先设悬念再反转，让观众会心一笑',
    '对比挑战': '对比展示效果差异，用反差制造冲击力',
    '情感共鸣': '用真实故事打动观众，引发情绪共鸣和分享欲',
}

DY_DURATION_MAP = {
    '15秒': {'total': '15', 'shots': 3, 'shot_duration': '3-5秒'},
    '30秒': {'total': '30', 'shots': 5, 'shot_duration': '3-6秒'},
    '60秒': {'total': '60', 'shots': 8, 'shot_duration': '3-10秒'},
}


# =============================================================================
# 五、核心调用函数
# =============================================================================

def get_available_models_info():
    """返回所有已配置 / 未配置 API Key 的模型信息"""
    available = {}
    for mid, cfg in TEXT_MODELS.items():
        available[mid] = {
            'id': mid, 'name': cfg['name'], 'emoji': cfg['emoji'],
            'free_quota': cfg['free_quota'], 'context': cfg['context'],
            'configured': bool(cfg['api_key']), 'recommended': cfg['recommended'],
            'type': 'text',
        }
    for mid, cfg in IMAGE_MODELS.items():
        available[mid] = {
            'id': mid, 'name': cfg['name'], 'emoji': cfg['emoji'],
            'free_quota': cfg['free_quota'], 'configured': bool(cfg.get('api_key')),
            'recommended': cfg.get('recommended', False), 'type': 'image',
        }
    for mid, cfg in VIDEO_MODELS.items():
        available[mid] = {
            'id': mid, 'name': cfg['name'], 'emoji': cfg['emoji'],
            'free_quota': cfg['free_quota'], 'configured': bool(cfg.get('api_key')),
            'recommended': cfg.get('recommended', False), 'type': 'video',
        }
    return available


def call_text_model(model_name, messages, temperature=0.8, max_tokens=2048):
    """
    调用文案模型，自动降级
    返回 (success, content, model_used, tokens)
    """
    order = [model_name] if model_name in TEXT_MODELS else []
    order += [m for m in TEXT_FALLBACK if m not in order]

    last_error = None
    for m in order:
        cfg = TEXT_MODELS.get(m)
        if not cfg or not cfg['api_key']:
            continue
        try:
            client = OpenAI(api_key=cfg['api_key'], base_url=cfg['base_url'])
            resp = client.chat.completions.create(
                model=cfg['model_id'], messages=messages,
                temperature=temperature, max_tokens=max_tokens,
            )
            content = resp.choices[0].message.content
            tokens = {
                'input': resp.usage.prompt_tokens if resp.usage else 0,
                'output': resp.usage.completion_tokens if resp.usage else 0,
                'total': resp.usage.total_tokens if resp.usage else 0,
            }
            return True, content, cfg['name'], tokens
        except Exception as e:
            last_error = str(e)
            logger.warning(f"{cfg['name']} 失败: {e}")
            continue

    return False, f"所有模型均失败。最后错误: {last_error}", None, None


def call_image_model(model_name, prompt, size='1024x1024'):
    """
    调用图片模型，引擎降级链
    返回 {"success", "image_url"/"error", "engine"}
    """
    order = [model_name] if model_name in IMAGE_MODELS else []
    order += [m for m in IMAGE_FALLBACK if m not in order]

    w, h = size.split('x')

    for m in order:
        cfg = IMAGE_MODELS.get(m)
        if not cfg:
            continue

        try:
            if cfg['type'] == 'cloudflare':
                result = _generate_cloudflare(cfg, prompt, w, h)
            else:
                result = _generate_huggingface(cfg, prompt)

            if result and result.get('success'):
                return result
        except Exception as e:
            logger.warning(f"图片模型 {cfg['name']} 失败: {e}")
            continue

    # 最终降级：Pollinations.ai 免费
    try:
        encoded = urllib.parse.quote(prompt[:200])
        url = f"https://image.pollinations.ai/prompt/{encoded}?width={w}&height={h}&nologo=true&seed={random.randint(1, 99999)}"
        resp = httpx.get(url, timeout=120, follow_redirects=True)
        if resp.status_code == 200:
            ct = resp.headers.get('content-type', 'image/jpeg')
            return {'success': True, 'image_url': f"data:{ct};base64,{b64.b64encode(resp.content).decode()}", 'engine': 'Pollinations.ai (免费)'}
    except:
        pass

    return {'success': False, 'error': '所有图片引擎均不可用'}


def _generate_cloudflare(cfg, prompt, w, h):
    """Cloudflare Workers AI 图片生成"""
    if not cfg['api_key'] or not cfg['account_id']:
        return None
    resp = httpx.post(
        f"https://api.cloudflare.com/client/v4/accounts/{cfg['account_id']}/ai/run/{cfg['model_id']}",
        headers={'Authorization': f'Bearer {cfg['api_key']}', 'Content-Type': 'application/json'},
        json={'prompt': prompt},
        timeout=60,
    )
    if resp.status_code == 200:
        data = resp.json()
        image_b64 = data.get('result', {}).get('image', '')
        if image_b64:
            return {'success': True, 'image_url': f"data:image/png;base64,{image_b64}", 'engine': cfg['name']}
    logger.warning(f"Cloudflare 返回 {resp.status_code}: {resp.text[:200]}")
    return None


def _generate_huggingface(cfg, prompt):
    """HuggingFace Inference API 图片生成"""
    if not cfg['api_key']:
        return None
    resp = httpx.post(
        f"https://api-inference.huggingface.co/models/{cfg['model_id']}",
        headers={'Authorization': f'Bearer {cfg["api_key"]}', 'Content-Type': 'application/json'},
        json={'inputs': prompt},
        timeout=180,
    )
    if resp.status_code == 200 and resp.headers.get('content-type', '').startswith('image/'):
        ct = resp.headers.get('content-type', 'image/jpeg')
        return {'success': True, 'image_url': f"data:{ct};base64,{b64.b64encode(resp.content).decode()}", 'engine': cfg['name']}
    logger.warning(f"HuggingFace 图片返回 {resp.status_code}")
    return None


# ---- 视频任务存储（内存） ----
_video_tasks = {}


def call_video_model(model_name, prompt, duration='5秒', style='写实'):
    """
    视频生成 — 异步任务模式
    返回 {"success", "task_id", "status", "engine"/"error"}
    """
    task_id = str(uuid.uuid4())[:12]
    order = [model_name] if model_name in VIDEO_MODELS else []
    order += [m for m in VIDEO_FALLBACK if m not in order]

    style_prompt = VIDEO_STYLE_PROMPTS.get(style, '')
    full_prompt = f"{prompt}, {style_prompt}" if style_prompt else prompt

    for m in order:
        cfg = VIDEO_MODELS.get(m)
        if not cfg or not cfg['api_key']:
            continue

        try:
            if cfg['type'] == 'huggingface':
                _video_tasks[task_id] = {
                    'status': 'processing',
                    'engine': cfg['name'],
                    'prompt': full_prompt,
                    'config': cfg,
                    'duration': duration,
                    'started_at': __import__('time').time(),
                }
                return {'success': True, 'task_id': task_id, 'status': 'processing', 'engine': cfg['name']}
        except Exception as e:
            logger.warning(f"视频模型 {cfg['name']} 失败: {e}")
            continue

    return {'success': False, 'error': '没有可用的视频引擎。请在 Railway Variables 中添加 HF_API_KEY'}


def check_video_task(task_id):
    """主动查询视频生成进度（HF Inference API 模式下轮询）"""
    task = _video_tasks.get(task_id)
    if not task:
        return {'status': 'not_found', 'error': '任务不存在'}

    if task['status'] == 'completed':
        return {'status': 'completed', 'video_url': task.get('video_url'), 'engine': task['engine']}
    if task['status'] == 'failed':
        return {'status': 'failed', 'error': task.get('error', '生成失败')}

    # 正在处理中，尝试拉取结果
    cfg = task.get('config')
    if cfg:
        try:
            resp = httpx.post(
                f"https://api-inference.huggingface.co/models/{cfg['model_id']}",
                headers={'Authorization': f'Bearer {cfg["api_key"]}', 'Content-Type': 'application/json'},
                json={'inputs': task['prompt']},
                timeout=300,
            )
            if resp.status_code == 200:
                ct = resp.headers.get('content-type', '')
                if ct.startswith('video/') or ct.startswith('application/octet-stream'):
                    video_b64 = b64.b64encode(resp.content).decode()
                    video_url = f"data:{ct};base64,{video_b64}"
                    _video_tasks[task_id]['status'] = 'completed'
                    _video_tasks[task_id]['video_url'] = video_url
                    return {'status': 'completed', 'video_url': video_url, 'engine': task['engine']}
        except Exception as e:
            logger.warning(f"视频轮询失败: {e}")

    return {'status': 'processing', 'message': 'AI 正在生成视频，请耐心等待约1-3分钟...', 'engine': task['engine']}


# =============================================================================
# 六、小红书文案生成
# =============================================================================

XHS_SYSTEM = """你是一个小红书爆款文案写手。请为产品撰写一篇小红书笔记。

创作原则：
1. 标题：吸睛且有爆款潜质，emoji开头，不超过20字
2. 正文：分段清晰，每段不超过3行，适当使用emoji
3. 语气：口语化、亲切自然，像真实用户分享，不要官方宣传感
4. 结尾：3-5个热门话题标签，用#开头
5. 整体要有"真人体感"，让人以为是真实用户写的"""


def generate_xiaohongshu(product, style='种草测评', length='标准', keywords='', model='deepseek'):
    """小红书爆款笔记生成"""
    word_map = {'短文案': '约150字', '标准': '约300字', '长文案': '约500字'}
    style_desc = XHS_STYLES.get(style, XHS_STYLES['种草测评'])

    prompt = f"""请为产品「{product}」撰写一篇小红书笔记。

产品：{product}
风格：{style_desc}
字数：{word_map.get(length, '约300字')}
{f"补充关键词：{keywords}" if keywords else ""}

输出格式（严格按以下结构）：
【标题】
（emoji开头的爆款标题）

【正文】
（分段清晰的笔记正文）

【标签】
（话题标签）"""

    messages = [
        {'role': 'system', 'content': XHS_SYSTEM},
        {'role': 'user', 'content': prompt},
    ]
    success, content, model_used, tokens = call_text_model(model, messages, 0.85, 2048)

    if success:
        # 尝试解析标题/正文/标签
        parts = _parse_xhs_output(content)
        parts['model_used'] = model_used
        parts['tokens'] = tokens
        parts['success'] = True
        return parts

    # 回退
    return {
        'success': True,
        'title': f'✨ 这款{product}真的太惊艳了',
        'body': f'最近发现了这款{product}，用了一次就爱不释手！\n\n颜值高、品质好、性价比也OK，推荐给所有需要的朋友～',
        'tags': '#好物推荐 #好物分享 #种草 #必买清单 #今日推荐',
        'full': f'✨ 这款{product}真的太惊艳了\n\n最近发现了这款{product}，用了一次就爱不释手！\n\n颜值高、品质好、性价比也OK，推荐给所有需要的朋友～\n\n#好物推荐 #好物分享 #种草',
        'model_used': '模板回退（无API Key）',
        'tokens': None,
    }


def _parse_xhs_output(content):
    """解析 AI 输出为标题/正文/标签"""
    result = {'title': '', 'body': '', 'tags': '', 'full': content}
    content = content.strip()

    # 按【标题】/【正文】/【标签】分段
    for marker, key in [('【标题】', 'title'), ('##', 'title'), ('###', 'body')]:
        if marker in content:
            parts = content.split(marker, 1)
            if len(parts) > 1:
                after = parts[1].strip()
                result[key] = after.split('\n')[0].strip() if key == 'title' else after
    if not result.get('title'):
        first_line = content.split('\n')[0].strip().lstrip('#').strip()
        result['title'] = first_line[:30]
    if not result.get('body'):
        result['body'] = '\n'.join(content.split('\n')[1:]).strip()

    # 提取标签
    for line in content.split('\n'):
        if line.strip().startswith('#') or '【标签】' in line:
            tags_line = line.replace('【标签】', '').strip()
            result['tags'] = tags_line
            break
    if not result['tags']:
        import re
        tags = re.findall(r'#[^\s#]+', content)
        result['tags'] = ' '.join(tags[:8]) if tags else '#好物推荐 #种草 #必买清单'

    return result


# =============================================================================
# 七、抖音脚本生成
# =============================================================================

DOUYIN_SYSTEM = """你是一个抖音爆款短视频策划。请为产品生成拍摄脚本。

要求：
1. 第1个分镜必须是"黄金3秒Hook"，快速抓住注意力
2. 台词要口语化、有网感，拒绝书面语
3. 备注列标注画面建议（景别/运镜/特效）
4. 节奏紧凑，适合短视频传播
5. 结尾给出BGM推荐和话题标签"""


def generate_douyin(product, script_style='开箱测评', duration='30秒', model='deepseek'):
    """抖音爆款脚本生成"""
    duration_info = DY_DURATION_MAP.get(duration, DY_DURATION_MAP['30秒'])
    style_desc = DY_STYLES.get(script_style, DY_STYLES['开箱测评'])

    prompt = f"""请为产品「{product}」创作一份抖音短视频拍摄脚本。

产品：{product}
风格：{style_desc}
总时长：约{duration_info['total']}秒
建议分镜数：{duration_info['shots']}个
每个分镜时长：{duration_info['shot_duration']}

输出格式（严格用表格形式）：
| 镜号 | 时长 | 画面描述 | 台词/旁白 | 备注 |
|------|------|---------|----------|------|
| 1    | 3s   | xxx     | xxx      | 黄金3秒Hook |
| 2    | ...  | ...     | ...      | ... |

结尾请注明：🎵 BGM建议：xxx / 🏷️ 话题标签：xxx"""

    messages = [
        {'role': 'system', 'content': DOUYIN_SYSTEM},
        {'role': 'user', 'content': prompt},
    ]
    success, content, model_used, tokens = call_text_model(model, messages, 0.9, 2048)

    if success:
        # 提取 BGM 和标签
        bgm = ''
        tags = ''
        for line in content.split('\n'):
            if 'BGM' in line:
                bgm = line.strip()
            if '话题标签' in line or (line.strip().startswith('#') and not tags):
                tags = line.strip()

        return {
            'success': True,
            'full': content,
            'bgm': bgm or '轻快节奏 / 热门卡点BGM',
            'tags': tags or '#抖音好物 #好物推荐 #短视频',
            'model_used': model_used,
            'tokens': tokens,
        }

    # 回退
    fallback = f"""| 镜号 | 时长 | 画面描述 | 台词/旁白 | 备注 |
|------|------|---------|----------|------|
| 1 | 3s | {product}特写 | 你敢信这个{product}？ | 黄金3秒Hook·特写 |
| 2 | 5s | 产品展示全景 | 用了就回不去了 | 中景·慢推 |
| 3 | 5s | 使用场景演示 | 真的太惊喜了 | 近景·自然光 |
| 4 | 4s | 细节特写 | 每一处都用心 | 微距·灯光 |
| 5 | 3s | 结尾CTA | 快去试试！ | 引导关注 |

🎵 BGM建议：轻快鼓点 / Deep House
🏷️ 话题标签：#抖音好物 #好物推荐 #必买清单"""

    return {
        'success': True,
        'full': fallback,
        'bgm': '轻快鼓点 / Deep House',
        'tags': '#抖音好物 #好物推荐 #必买清单',
        'model_used': '模板回退（无API Key）',
        'tokens': None,
    }
