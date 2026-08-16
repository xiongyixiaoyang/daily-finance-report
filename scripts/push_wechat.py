#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
push_wechat.py - 推送日报到微信（Server酱）

用法:
  python3 push_wechat.py <日报文件路径> [标题]
  python3 push_wechat.py --test   # 发送测试消息

依赖: SENDKEY 环境变量或本文件内配置
"""
import urllib.request
import json
import sys
import os

# Server酱 SendKey（必须通过环境变量 SCT_SENDKEY 配置，不硬编码）
SENDKEY = os.environ.get('SCT_SENDKEY')
if not SENDKEY:
    print('错误: 未设置 SCT_SENDKEY 环境变量。')
    print('请先执行: export SCT_SENDKEY="你的SendKey"')
    sys.exit(1)
API_URL = f'https://sctapi.ftqq.com/{SENDKEY}.send'


def push(title, content):
    """推送到 Server酱，返回响应 JSON"""
    payload = {'title': title, 'content': content}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data,
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=15) as f:
        return json.loads(f.read().decode('utf-8'))


def main():
    if '--test' in sys.argv:
        result = push('📰 测试消息', 'Server酱推送链路测试 ✅')
        print(f'测试推送: {result}')
        return

    if len(sys.argv) < 2:
        print('用法: python3 push_wechat.py <日报文件路径> [标题]')
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 标题：第二个参数或默认从文件名生成
    if len(sys.argv) >= 3:
        title = sys.argv[2]
    else:
        import os.path
        fname = os.path.basename(filepath)
        title = f'📰 全球财经日报 | {fname[:10]}'

    result = push(title, content)
    print(f'推送结果: code={result.get("code")} message={result.get("message", "")}')
    if result.get('data'):
        print(f'推送ID: {result["data"].get("pushid")}')
    if result.get('code') != 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
