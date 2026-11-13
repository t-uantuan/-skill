---
name: dqc-recon
description: 对账与数据质量——多源证据机械验证
when: 链路 s3 验证子段；任何交付前
inputs: [本单产出物路径, 源库连接, golden case]
outputs: [recon-report.md：逐项 pass/fail + 证据路径]
checks: [〈对账脚本〉 / 〈机械Gate脚本〉 / evals/score.py]
escalate: diff≠0 重试 2 次不平 / golden 回归失败
version: 0.1
---

# 对账与质量验证

## 多源证据规则（杀 FM-B06"只查内部勾稽"）

1. **对源重算**：源库 vs 落盘 vs ODS 三方行数（不只查产出物内部自洽）
2. **对历史**：与 golden case 冻结断言比对
3. **跨项交叉**：行数平之外抽 1 列做内容校验（行数对但内容错是真实风险）

## 断言清单（采集域）

- 行数 diff=0（append 表 0 行≠异常）
- 幂等：同分区重跑 count 不变
- 控制表断点值单调
- 分区日期 = 业务日期（杀 FM-A13，实时链路同理）
- 验收查询限时 30s

## 修订记录

| 日期 | 归因 | 改了什么 |
|---|---|---|
| — | 初版 | — |
