# 📰 Daily Finance Report - 全球财经日报生成器

> 猫笔刀风格的全球财经日报自动生成技能。为个人实盘投资提供可执行、可回溯的市场分析与推荐。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 功能特性

- 🗞️ **多源新闻采集**：CNBC / MarketWatch RSS + 财新网 + 第一财经
- 📊 **实时行情数据**：腾讯行情 API（16项核心指标）+ 汇率 + 黄金
- 💡 **猫笔刀风格分析**：核心观点 → 股票推荐 → ETF实操框架 → 深度观察 → 核心数据
- 🚀 **股票推荐规则**：仅限A股/港股、A+H默认选H股、目标价偏离≤30%
- 📊 **ETF实操框架**：核心逻辑、配置权重、目标区间、止盈止损、逻辑依据
- 📋 **推荐跟踪档案**：历史推荐自动归档，逻辑连贯可回溯
- 📱 **微信推送**：Server酱一键推送到个人微信

## 安装

### 方式一：ClawHub
从 ClawHub 搜索 `daily-finance-report` 一键安装。

### 方式二：手动安装
```bash
# 克隆仓库
git clone https://github.com/<your-username>/daily-finance-report.git

# 复制到 OpenClaw skills 目录
cp -r daily-finance-report ~/.openclaw/skills/
```

### 方式三：zip 包
将 `daily-finance-report-skillhub.zip` 解压到 skills 目录：
```bash
unzip daily-finance-report-skillhub.zip -d ~/.openclaw/skills/
```

## 使用

安装后，在对话中直接说：

- 「生成今天的财经日报」
- 「今天推荐什么股票/ETF」
- 「跑一下日报推送到微信」
- 「今日市场怎么看」

技能会自动执行：采集新闻 → 拉取行情 → 生成日报 → 更新跟踪档案 → 推送微信。

## 输出示例

日报包含六个章节：

1. **💡 核心观点** — 3-5句带态度的市场要点
2. **🚀 股票推荐** — ≤2只，含逻辑/跟踪记录/目标价/风险
3. **📊 ETF推荐** — ≤2只，含完整实操框架
4. **🌍 深度观察** — 3-6条猫笔刀风格分析
5. **📊 核心数据** — 16项指标行情表
6. **⚡ 今日关注清单** — 关键事件/逻辑链

## 配置

### Server酱推送（可选）
```bash
export SCT_SENDKEY="你的SendKey"
```
或在 `scripts/push_wechat.py` 中直接配置。

### 推荐跟踪档案
默认保存在 `AI 工作区/成果文件/全球财经日报/推荐跟踪档案.md`，记录每次推荐的标的、价格、目标、逻辑。

## 目录结构

```
daily-finance-report/
├── SKILL.md                    # 主指令
├── scripts/
│   ├── collect_news.py         # 新闻采集
│   ├── fetch_quotes.py         # 行情采集
│   └── push_wechat.py          # Server酱推送
├── references/
│   ├── report_template.md      # 日报模板
│   └── recommendation_rules.md # 推荐规则
└── assets/
    └── track_template.md       # 跟踪档案格式
```

## 免责声明

本技能生成的所有内容基于公开信息，不构成投资建议。投资有风险，入市需谨慎。

## License

[MIT](LICENSE)
