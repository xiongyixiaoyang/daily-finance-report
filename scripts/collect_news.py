#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collect_news.py - 全球财经新闻采集
从 CNBC / MarketWatch RSS + 财新网 + 第一财经 + 官方公告 提取今日头条。

用法: python3 collect_news.py [--limit N]
输出: JSON 数组 [{source, title, desc, date, url}]
"""
import urllib.request
import re
import html
import json
import sys

def fetch_rss(url, source, timeout=10):
    """抓取 RSS 并解析 title/description/pubDate"""
    results = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as f:
            content = f.read().decode('utf-8', errors='ignore')
        items = re.findall(
            r'<item>.*?<title>(.*?)</title>.*?<description>(.*?)</description>.*?<pubDate>(.*?)</pubDate>',
            content, re.DOTALL
        )
        for title, desc, date in items:
            results.append({
                'source': source,
                'title': html.unescape(re.sub(r'<[^>]+>', '', title)).strip(),
                'desc': html.unescape(re.sub(r'<[^>]+>', '', desc)).strip()[:200],
                'date': date.strip()
            })
    except Exception as e:
        results.append({'source': source, 'title': f'[ERROR] {e}', 'desc': '', 'date': ''})
    return results

def fetch_headlines(url, source, timeout=10):
    """抓取普通页面中的新闻标题（财新/一财/官网等）"""
    results = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as f:
            content = f.read().decode('utf-8', errors='ignore')
        # 提取 a 标签中的标题（10-100字符）
        links = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>([^<]{10,100})</a>', content)
        seen = set()
        for href, text in links:
            text = text.strip()
            if text and text not in seen and not href.startswith('javascript'):
                seen.add(text)
                results.append({'source': source, 'title': text, 'desc': '', 'date': '', 'url': href})
    except Exception as e:
        results.append({'source': source, 'title': f'[ERROR] {e}', 'desc': '', 'date': ''})
    return results

def main():
    limit = 8
    if '--limit' in sys.argv:
        idx = sys.argv.index('--limit')
        limit = int(sys.argv[idx + 1])

    all_news = []
    # 核心 RSS 源（已验证可用）
    all_news += fetch_rss('https://www.cnbc.com/id/100003114/device/rss/rss.html', 'CNBC')
    all_news += fetch_rss('https://www.marketwatch.com/rss/topstories', 'MarketWatch')
    # 辅助源（可能被墙/403，失败自动跳过）
    all_news += fetch_headlines('https://www.caixin.com/', '财新网')
    all_news += fetch_headlines('https://www.yicai.com/news/', '第一财经')

    # 过滤错误条目
    valid = [n for n in all_news if not n['title'].startswith('[ERROR]')]
    # 按日期排序（有日期的在前）
    valid.sort(key=lambda x: x['date'], reverse=True)

    print(json.dumps(valid[:limit * 4], ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
