#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_quotes.py - 行情数据采集
从腾讯行情 API + 免费汇率/黄金 API 获取核心市场数据。

用法: python3 fetch_quotes.py
输出: JSON 对象 {指标名: {price, change_pct, time}}
"""
import urllib.request
import json
import re

# 腾讯行情代码映射
TENCENT_CODES = {
    '沪深300': 'sh000300',
    '中证500': 'sz399005',
    '创业板指': 'sz399006',
    '上证50': 'sh000016',
    '科创50': 'sh000688',
    '恒生指数': 'hkHSI',
    '恒生科技': 'hkHSTECH',
    '标普500': 'usINX',
    '纳斯达克': 'usIXIC',
    '道琼斯': 'usDJI',
}

def fetch_tencent():
    """从腾讯行情 API 获取指数数据"""
    codes = ','.join(TENCENT_CODES.values())
    url = f'https://qt.gtimg.cn/q={codes}'
    result = {}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as f:
            data = f.read().decode('gbk', errors='ignore')

        for line in data.strip().split(';'):
            if '~' not in line:
                continue
            parts = line.split('~')
            if len(parts) < 33:
                continue
            # 找到对应的指标名
            name = None
            for label, code in TENCENT_CODES.items():
                if code in line:
                    name = label
                    break
            if not name:
                continue
            price = parts[3]
            change_pct = parts[32]
            raw_time = parts[30]  # YYYYMMDDHHMMSS
            # 格式化时间 MM-DD HH:MM（鲁棒解析：提取连续数字）
            digits = re.sub(r'\D', '', raw_time)
            if len(digits) >= 12:
                time_str = f'{digits[4:6]}-{digits[6:8]} {digits[8:10]}:{digits[10:12]}'
            else:
                time_str = ''
            # A股指数收盘时间处理：HH > 15 显示为 15:00(收盘)
            if name in ('沪深300', '中证500', '创业板指', '上证50', '科创50') and len(digits) >= 10:
                hh = int(digits[8:10])
                if hh > 15:
                    time_str = f'{digits[4:6]}-{digits[6:8]} 15:00(收盘)'
            result[name] = {'price': price, 'change_pct': change_pct, 'time': time_str}
    except Exception as e:
        result['_error'] = f'腾讯行情: {e}'
    return result

def fetch_forex():
    """汇率：美元兑人民币"""
    try:
        req = urllib.request.Request('https://open.er-api.com/v6/latest/USD',
                                     headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as f:
            data = json.loads(f.read().decode())
        return {'离岸人民币/美元': {'price': str(data['rates']['CNY']), 'change_pct': '', 'time': ''}}
    except Exception as e:
        return {'_error': f'汇率: {e}'}

def fetch_gold():
    """现货黄金"""
    try:
        req = urllib.request.Request('https://api.gold-api.com/price/XAU',
                                     headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as f:
            data = json.loads(f.read().decode())
        return {'现货黄金': {'price': str(data.get('price', '')), 'change_pct': str(data.get('chg', '')),
                              'time': ''}}
    except Exception as e:
        return {'_error': f'黄金: {e}'}

def main():
    result = {}
    result.update(fetch_tencent())
    result.update(fetch_forex())
    result.update(fetch_gold())
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
