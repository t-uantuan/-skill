---
name: delivery-check
description: 交付前检查——回归 + 文档同步 + 复盘强制
when: 链路 s4；G3 放行之前
inputs: [本单全部产出, specs/ 文档集, runs/<id>/friction.md]
outputs: [交付单, 复盘记录, 文档更新完成]
checks: [evals/score.py 全绿, 文档 diff 检查]
escalate: score.py 回归失败 / 复盘未完成
version: 0.1
---

# 交付检查

## 步骤

1. **回归**：`python evals/score.py` 必须全绿（杀 FM-B03：修复引入回归）。
2. **文档同步**：流程文档 FR 表加行；若踩了新坑 → 问题与解决方案文档追加条目（格式对齐 P-xx：现象/根因/解决/验证/经验）。
3. **失败模式回填**：新错法先入 specs/failure-modes.md（模式级）或 skill checks（具体级）。
4. **复盘归因**：friction.md 每条标 A/B/C/D，每条有回写动作——**没有复盘，G3 不放行**（retro_required）。
5. **交付单**：断言结果表 + 证据路径 + 遗留 TBD 清单。

## 修订记录

| 日期 | 归因 | 改了什么 |
|---|---|---|
| — | 初版 | — |
