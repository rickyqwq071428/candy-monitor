#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淘宝开放平台数据采集器
支持三种模式:
  - manual: 手动模式（默认），通过 Excel 模板导入
  - personal: 个人开发者API（仅基础字段：标题、主图、一口价）
  - enterprise: 企业开发者API（全量字段：含销量、SKU、库存）
"""

import configparser
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')


class TaobaoCollector:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_PATH, encoding='utf-8')
        self.mode = self.config.get('taobao', 'api_mode', fallback='manual')
        self.app_key = self.config.get('taobao', 'app_key', fallback='')
        self.app_secret = self.config.get('taobao', 'app_secret', fallback='')

    def get_mode_info(self):
        """返回当前模式信息"""
        modes = {
            'manual': {
                'name': '手动模式',
                'description': '通过 Excel 模板手动导入数据',
                'fields': ['标题', '主图', '价格', '销量', '店铺', '链接'],
                'rate_limit': '无限制',
                'auth_required': '无需认证',
                'guide': '下载Excel模板 → 手动填入数据 → 上传导入 → 自动入库'
            },
            'personal': {
                'name': '个人开发者API',
                'description': '仅需身份证实名认证，获取基础字段',
                'fields': ['标题', '主图', '一口价'],
                'rate_limit': '500次/天',
                'auth_required': '身份证实名认证',
                'guide': '1. 访问 open.taobao.com 注册个人开发者\n2. 完成身份证实名认证\n3. 创建应用获取AppKey/AppSecret\n4. 填入config.ini'
            },
            'enterprise': {
                'name': '企业开发者API',
                'description': '需企业营业执照，获取全量商品数据',
                'fields': ['标题', '主图', '价格', '销量', 'SKU', '库存', '店铺信息'],
                'rate_limit': '5000次/天',
                'auth_required': '企业营业执照认证',
                'guide': '联系淘宝开放平台申请企业资质'
            }
        }
        return modes.get(self.mode, modes['manual'])

    def search_products(self, keyword, page=1, page_size=10):
        """搜索商品（企业模式需要实现淘宝API调用）"""
        if self.mode == 'manual':
            return {
                'mode': 'manual',
                'message': f'请在淘宝搜索"{keyword}"，将结果填入Excel模板后上传',
                'search_link': f'https://s.taobao.com/search?q={keyword}&sort=sale-desc'
            }

        if self.mode == 'personal':
            if not self.app_key or self.app_key == 'your_app_key_here':
                return {
                    'mode': 'personal',
                    'message': '请先配置 AppKey 和 AppSecret',
                    'guide': self.get_mode_info()['guide']
                }
            return {
                'mode': 'personal',
                'message': '个人模式仅能获取标题/主图/一口价，无法获取销量数据',
                'recommendation': '建议使用 manual 模式 + 生意参谋免费版组合方案'
            }

        # enterprise mode - would implement actual API call here
        return {
            'mode': 'enterprise',
            'message': f'搜索关键词: {keyword}',
            'api_ready': bool(self.app_key and self.app_key != 'your_app_key_here')
        }

    def get_alternative_links(self, keyword):
        """获取各平台零成本查询链接"""
        return {
            'taobao': f'https://s.taobao.com/search?q={keyword}&sort=sale-desc',
            'taobao_shop': f'https://s.taobao.com/search?q={keyword}&sort=sale-desc',
            'douyin': f'https://www.douyin.com/search/{keyword}',
            'xiaohongshu': f'https://www.xiaohongshu.com/search_result?keyword={keyword}',
            'dianping': f'https://www.dianping.com/search/keyword/2/0_{keyword}',
            'alibaba_index': f'https://index.1688.com/alizs/search.htm?key={keyword}',
            'sycm': 'https://sycm.taobao.com'
        }


collector = TaobaoCollector()
