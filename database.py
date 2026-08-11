#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库层 - SQLite 存储
表结构:
  ranking_products: 排行产品
  viral_content: 爆款内容
  age_distribution: 消费者年龄分布
  merchants: 跟踪商家
  share_links: 分享链接
"""

import sqlite3
import os
import uuid
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'candy_monitor.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS ranking_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        keyword TEXT NOT NULL,
        rank INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        shop_name TEXT,
        price REAL,
        sales INTEGER,
        cover_url TEXT,
        product_link TEXT,
        source TEXT DEFAULT 'imported',
        imported_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS viral_content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        content_type TEXT DEFAULT 'post',
        title TEXT NOT NULL,
        author TEXT,
        author_avatar TEXT,
        cover_url TEXT,
        summary TEXT,
        likes INTEGER DEFAULT 0,
        comments INTEGER DEFAULT 0,
        shares INTEGER DEFAULT 0,
        favorites INTEGER DEFAULT 0,
        plays INTEGER DEFAULT 0,
        content_link TEXT,
        keyword TEXT,
        source TEXT DEFAULT 'imported',
        published_date TEXT,
        imported_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS age_distribution (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        source_detail TEXT,
        age_group TEXT NOT NULL,
        percentage REAL NOT NULL,
        gender TEXT,
        sample_size INTEGER,
        platform TEXT,
        imported_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS merchants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        name TEXT NOT NULL,
        shop_type TEXT,
        followers TEXT,
        product_count INTEGER,
        avg_price REAL,
        shop_link TEXT,
        notes TEXT,
        imported_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS share_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL DEFAULT '竞品数据分享',
        permission TEXT NOT NULL DEFAULT 'readonly',
        expiry_type TEXT NOT NULL DEFAULT '7d',
        expiry_at DATETIME,
        revoked INTEGER DEFAULT 0,
        visit_count INTEGER DEFAULT 0,
        last_visit DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


# ===== 排行产品 CRUD =====

def get_rankings(platform=None, keyword=None, limit=100):
    conn = get_db()
    query = "SELECT * FROM ranking_products WHERE 1=1"
    params = []
    if platform:
        query += " AND platform = ?"
        params.append(platform)
    if keyword:
        query += " AND keyword LIKE ?"
        params.append(f'%{keyword}%')
    query += " ORDER BY platform, rank LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_ranking(data):
    conn = get_db()
    conn.execute("""
        INSERT INTO ranking_products (platform, keyword, rank, product_name, shop_name, price, sales, cover_url, product_link, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (data['platform'], data['keyword'], data['rank'], data['product_name'],
          data.get('shop_name'), data.get('price'), data.get('sales'),
          data.get('cover_url'), data.get('product_link'), data.get('source', 'manual')))
    conn.commit()
    conn.close()


def clear_rankings():
    conn = get_db()
    conn.execute("DELETE FROM ranking_products")
    conn.commit()
    conn.close()


# ===== 爆款内容 CRUD =====

def get_viral_content(platform=None, limit=100):
    conn = get_db()
    query = "SELECT * FROM viral_content WHERE 1=1"
    params = []
    if platform:
        query += " AND platform = ?"
        params.append(platform)
    query += " ORDER BY likes DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_viral(data):
    conn = get_db()
    conn.execute("""
        INSERT INTO viral_content (platform, content_type, title, author, author_avatar, cover_url,
            summary, likes, comments, shares, favorites, plays, content_link, keyword, source, published_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (data['platform'], data.get('content_type', 'post'), data['title'],
          data.get('author'), data.get('author_avatar'), data.get('cover_url'),
          data.get('summary'), data.get('likes', 0), data.get('comments', 0),
          data.get('shares', 0), data.get('favorites', 0), data.get('plays', 0),
          data.get('content_link'), data.get('keyword'), data.get('source', 'imported'),
          data.get('published_date')))
    conn.commit()
    conn.close()


def clear_viral():
    conn = get_db()
    conn.execute("DELETE FROM viral_content")
    conn.commit()
    conn.close()


# ===== 年龄分布 CRUD =====

def get_age_distribution():
    conn = get_db()
    rows = conn.execute("SELECT * FROM age_distribution ORDER BY source, age_group").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_age_distribution(data):
    conn = get_db()
    conn.execute("""
        INSERT INTO age_distribution (source, source_detail, age_group, percentage, gender, sample_size, platform)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (data['source'], data.get('source_detail'), data['age_group'],
          data['percentage'], data.get('gender'), data.get('sample_size'), data.get('platform')))
    conn.commit()
    conn.close()


def clear_age():
    conn = get_db()
    conn.execute("DELETE FROM age_distribution")
    conn.commit()
    conn.close()


# ===== 商家 CRUD =====

def get_merchants(platform=None):
    conn = get_db()
    query = "SELECT * FROM merchants"
    params = []
    if platform:
        query += " WHERE platform = ?"
        params.append(platform)
    query += " ORDER BY platform, name"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_merchant(data):
    conn = get_db()
    conn.execute("""
        INSERT INTO merchants (platform, name, shop_type, followers, product_count, avg_price, shop_link, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (data['platform'], data['name'], data.get('shop_type'), data.get('followers'),
          data.get('product_count'), data.get('avg_price'), data.get('shop_link'), data.get('notes')))
    conn.commit()
    conn.close()


def clear_merchants():
    conn = get_db()
    conn.execute("DELETE FROM merchants")
    conn.commit()
    conn.close()


# ===== 分享链接 CRUD =====

def create_share_link(title, permission='readonly', expiry_type='7d'):
    token = uuid.uuid4().hex[:12]
    now = datetime.now()

    expiry_map = {
        '24h': now + timedelta(hours=24),
        '7d': now + timedelta(days=7),
        '30d': now + timedelta(days=30),
        'forever': None
    }
    expiry_at = expiry_map.get(expiry_type)

    conn = get_db()
    conn.execute("""
        INSERT INTO share_links (token, title, permission, expiry_type, expiry_at)
        VALUES (?, ?, ?, ?, ?)
    """, (token, title, permission, expiry_type, expiry_at))
    conn.commit()
    conn.close()
    return token


def get_share_links():
    conn = get_db()
    rows = conn.execute("SELECT * FROM share_links ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def verify_share_token(token):
    conn = get_db()
    row = conn.execute("SELECT * FROM share_links WHERE token = ? AND revoked = 0", (token,)).fetchone()
    if not row:
        conn.close()
        return None

    link = dict(row)
    if link['expiry_at']:
        expiry = datetime.fromisoformat(link['expiry_at'])
        if datetime.now() > expiry:
            conn.close()
            return {'expired': True}

    conn.execute("UPDATE share_links SET visit_count = visit_count + 1, last_visit = ? WHERE token = ?",
                 (datetime.now().isoformat(), token))
    conn.commit()
    conn.close()
    link['expired'] = False
    return link


def revoke_share_link(token):
    conn = get_db()
    conn.execute("UPDATE share_links SET revoked = 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()


def regenerate_share_link(token):
    conn = get_db()
    old = conn.execute("SELECT * FROM share_links WHERE token = ?", (token,)).fetchone()
    if not old:
        conn.close()
        return None
    new_token = uuid.uuid4().hex[:12]
    conn.execute("UPDATE share_links SET token = ? WHERE token = ?", (new_token, token))
    conn.commit()
    conn.close()
    return new_token


def delete_share_link(token):
    conn = get_db()
    conn.execute("DELETE FROM share_links WHERE token = ?", (token,))
    conn.commit()
    conn.close()


# ===== Dashboard 统计 =====

def get_dashboard_stats():
    conn = get_db()
    stats = {}
    stats['total_rankings'] = conn.execute("SELECT COUNT(*) FROM ranking_products").fetchone()[0]
    stats['total_viral'] = conn.execute("SELECT COUNT(*) FROM viral_content").fetchone()[0]
    stats['total_merchants'] = conn.execute("SELECT COUNT(*) FROM merchants").fetchone()[0]

    # 各平台排行数量
    platforms = conn.execute("SELECT platform, COUNT(*) as cnt FROM ranking_products GROUP BY platform").fetchall()
    stats['platform_counts'] = {r['platform']: r['cnt'] for r in platforms}

    # 总互动量
    engagement = conn.execute("""
        SELECT SUM(likes) as total_likes, SUM(comments) as total_comments,
               SUM(shares) as total_shares, SUM(plays) as total_plays
        FROM viral_content
    """).fetchone()
    stats['total_likes'] = engagement['total_likes'] or 0
    stats['total_comments'] = engagement['total_comments'] or 0
    stats['total_plays'] = engagement['total_plays'] or 0

    # 平均价格
    avg = conn.execute("SELECT AVG(price) as avg_price FROM ranking_products WHERE price > 0").fetchone()
    stats['avg_price'] = round(avg['avg_price'], 1) if avg['avg_price'] else 0

    conn.close()
    return stats


def get_trends_data():
    """获取趋势数据 - 按平台和关键词聚合"""
    conn = get_db()
    rows = conn.execute("""
        SELECT platform, keyword, COUNT(*) as cnt, AVG(price) as avg_price, SUM(sales) as total_sales
        FROM ranking_products
        GROUP BY platform, keyword
        ORDER BY cnt DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


if __name__ == '__main__':
    init_db()
    print("数据库初始化完成:", DB_PATH)
