# DOMAIN · dw-collect 领域包说明（这个包是干什么的）

> **一句话**：数仓采集领域的领域知识模板——数据采集（试点）+ 实时数仓（暂缓）。骨架（`..\..\skeleton\`）发动的流程，靠本包提供"什么算做对"的事实标准。
> **本包为通用示例包**：所有环境名、库名、表名、脚本名均为占位符（见 `..\README.md` 占位符约定），落地时替换为实际值；占位符本身即"待填"信号，不得当作可用环境。

## 为什么存在（准入证据摘要——建包时按实际填写，全文见 specs/pilot.md）

| 准入条件 | 证据（示例写法） |
|---|---|
| 会重复出现 | 元数据驱动 N 张表周期采集，新表随业务持续出现；同类任务跨 ≥3 项目重复 |
| 可机械核验 | 行数对账脚本现成；幂等重跑可脚本判定 |
| 有历史答案 | 流程文档 + 历史问题清单已闭环（现象/根因/解决/验证逐项可查） |

## 包含清单

```
dw-collect/
├─ DOMAIN.md               # 本文件
├─ workflow/dw-delivery.yaml   # 状态机实例（链路1采集启用 / 链路2实时暂缓；治理不变量见骨架纪律）
├─ skills/                 # 5 个行业 skill（由失败模式逐条推导）
│  ├─ table-sync/          # 试点链路执行 skill
│  ├─ caliber-spec/  source-profile/  dqc-recon/  delivery-check/
├─ specs/
│  ├─ glossary.yaml        # 术语库模板 + 大白话映射；多集群并存时须写警示条目
│  ├─ failure-modes.md     # 失败模式清单（FM-A 数据链路层 + FM-B Agent 执行层）
│  ├─ acceptance-assertion-cards.md  # 验收断言形态卡
│  └─ pilot.md             # 试点决策记录模板 + 准入证据链
├─ evals/
│  ├─ cases/example-table-sync/      # golden case 模板（input/context/decisions/expected/check.py）
│  └─ score.py             # 评分器（SKIPPED 机制；路径绑定本包 cases/）
├─ escalations/            # 升级包样例（脱敏；E- 任务级 / EP- 流程级）
└─ baselines/              # 第 0 周人工 3 单计时填充
```

## 当前状态（建包时填写）

- [ ] 第 0 周人工基线 3 单（baselines/ 待填，只有本人能做）
- [ ] golden case 实跑全绿（需环境可用；环境不可用即挂起，不得擅自启动——FM-B09）
- [ ] L1 首跑真实新表需求
- 环境警示：多集群并存时在此写明"命令勿混目标"（FM-B10）

## 怎么用（与骨架的对接）

1. 新需求 → `skeleton/skills/meta-requirement/SKILL.md`，inputs 喂本包 `specs/glossary.yaml` + `specs/failure-modes.md`（+ 形态卡）
2. 走本包 `workflow/dw-delivery.yaml` 状态机（G1 口径 → G2 方案 → MG+IR → G3 豁免）
3. 机械验收跑本包 `evals/score.py`；摩擦记根目录 `runs/<id>/friction.md`

## 修订记录

| 日期 | 归因 | 改动 |
|---|---|---|
| — | 初版 | 由实战领域包迁入本结构 |
| 2026-11-11 | 脱敏整理 | 全部环境/库名/表名/脚本名占位符化，运行状态清零为模板 |
| 2026-11-11 | 审核修复 | 包含清单补 escalations\（升级包样例） |
