# 纯净版 skill · Agent 工作流实施框架（通用模板）

> 体系：大白话 → meta-requirement（规格+三层验收）→ 四段带内循环 → 机械 Gate + 独立复核
> → 3 个人拍板点（G1 口径 / G2 方案 / G3 豁免）→ 强制复盘回写资产。
>
> 本目录为**脱敏通用版**：只含可复用的方法论骨架与领域包模板，不含任何真实运行数据、
> 环境信息、凭据或项目信息。领域包内所有具体名称均以占位符表示（如〈集群A〉〈业务库〉〈表X〉），
> 落地时替换为实际值即可。

## 两层结构（骨架与血肉分离）

```
纯净版skill\
├─ README.md                  # 本文件：入口
├─ 使用说明.md                # 用法总览：五种用法、可复制提示词、常见坑
├─ skeleton\                  # 通用骨架（跨行业不变）：元 skill + 4 角色文件
├─ domains\                   # 领域包（血肉），一域一文件夹
│  └─ dw-collect\             # 数仓采集·通用示例领域包（模板+占位示例）
└─ runs\                      # 运行时产物目录（跨域共用；<id>/state.json + friction.md）
```

**换领域 = 建新领域包，骨架零改动。** 新建包的检查清单见 `domains\README.md`。

## 各目录说明

| 目录 | 内容 |
|---|---|
| `使用说明.md` | 用法总览：散用/流水线/回归/建包/复盘五种用法 + 可复制提示词 + 常见坑 |
| `skeleton\skills\meta-requirement\` | 唯一元 skill：大白话 → 六件产出（意图卡/规格/三层验收/失败模式映射/升级包/术语表）。任何需求必经 |
| `skeleton\agents\` | planner / builder / reviewer / verifier 四角色上下文隔离文件 |
| `domains\<域>\specs\` | 术语库 glossary.yaml + 失败模式清单 + 验收断言形态卡 + 试点决策记录 |
| `domains\<域>\skills\` | 行业 skill（由失败模式逐条推导） |
| `domains\<域>\workflow\` | 状态机实例（段/链路/Gate 映射） |
| `domains\<域>\evals\` | golden case 模板（input/context/decisions/expected/check.py）+ score.py 评分器 |
| `domains\<域>\escalations\` | 升级包样例（脱敏模板；实际单的升级包落 `runs\<id>\escalations\`） |
| `domains\<域>\baselines\` | 人工基线计时落这里 |
| `runs\<id>\` | 每单状态 state.json + 摩擦记录 friction.md + 升级包 escalations\ + 术语表 terms\ |

## 第一次跑（操作顺序）

1. 选定（或新建）领域包，把 `domains\dw-collect\specs\` 中的占位符替换为实际术语与环境事实。
2. 用一个已知可复现的历史小任务，参照 `domains\dw-collect\evals\cases\example-table-sync\`
   冻结一个自己的 golden case（五件：input/context/decisions/expected/check.py）。
3. `cd domains\<域> && python evals/score.py` —— 确认评分器环境（环境不可用时 SKIPPED，正常）。
4. 来一个真实需求 → 交给 `skeleton\skills\meta-requirement` 产六件
   （inputs 四件套 = 大白话原文＋本包 specs 的 glossary / failure-modes / 验收断言形态卡；
   第 6 件术语表落盘项目术语目录 `terms\`，跨单累积）
   → 按 `domains\<域>\workflow\` 状态机走。
5. 每卡一次记 `runs\<id>\friction.md`（归因 A/B/C/D）。
6. 交付前：复盘没做，G3 不放行。

## 纪律（三条红线）

1. 状态落 state.json（`runs/<id>/`），不落聊天记录。
2. Reviewer 只见 acceptance.md + 原始需求 + 产出物三样。
3. 改任何 skill 前后各跑一次 score.py（杀回归）。

## 使用注意

- `runs\` 目录只放运行时产物，**严禁**将含真实环境信息（主机/IP/账号/凭据）的取证材料
  纳入版本管理；凭据一律走工具原生文件机制并物理隔离（见 .gitignore）。
- 本模板文件本身不应出现任何真实环境值；发现占位符被真实值替换后仍留在模板层的，按泄漏处理。
- 文中出现的通用技术栈名（如 Hive / StreamLoad / 常见默认端口）仅作示例说明，不构成环境信息；
  落地时按本域实际技术栈替换。

## 修订记录

| 日期 | 归因 | 改动 |
|---|---|---|
| — | 初版 | 元 skill + 4 角色文件 + 领域包结构 + 评分器（初版为 21 文件骨架） |
| — | 结构重构（骨架/血肉分离） | 新增 skeleton\ 与 domains\ 两层；领域内容入包 |
| 2026-11-11 | 脱敏整理 | 由实战框架整理为通用模板：移除全部运行数据/环境信息/真实名称，领域包改占位符示例 |
| 2026-11-11 | 审核修复 | 补升级包样例（domains\dw-collect\escalations\）；修 verifier.md 排版与 score.py 退出码判定；目录说明与修订记录对齐实际文件数 |
