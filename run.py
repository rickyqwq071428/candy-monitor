#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可予礼品有限公司 - 喜糖/伴手礼竞品监控平台
生产级启动入口（waitress WSGI）
"""

import os
import sys
from waitress import serve
from app import app

# 环境变量配置，支持多平台云部署
# Render: 自动注入 PORT，PythonAnywhere: 无特殊变量
HOST = os.environ.get('CANDY_HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT') or os.environ.get('CANDY_PORT', 5000))
THREADS = int(os.environ.get('CANDY_THREADS', '4'))
DEBUG = os.environ.get('CANDY_DEBUG', 'false').lower() == 'true'

BANNER = """
╔══════════════════════════════════════════════════╗
║     可予礼品有限公司 · 竞品监控平台               ║
║     喜糖 · 伴手礼 · 行业数据                     ║
╚══════════════════════════════════════════════════╝
"""

if __name__ == '__main__':
    print(BANNER)
    print(f"  🚀 生产模式 (waitress {THREADS}线程)")
    print(f"  🌐 监听地址: http://{HOST}:{PORT}")
    print(f"  📋 新手引导: http://{HOST}:{PORT}/guide")
    print(f"  ❤️  健康检查: http://{HOST}:{PORT}/health")
    print()

    if DEBUG:
        print("  ⚠️  DEBUG 模式已开启")
        app.run(host=HOST, port=PORT, debug=True)
    else:
        print("  ✅ 服务已启动，按 Ctrl+C 停止")
        serve(app, host=HOST, port=PORT, threads=THREADS)
