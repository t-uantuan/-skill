# runs · 运行时产物目录（跨域共用）

每单一个文件夹 `runs/<id>/`，id 命名建议 `REQ-YYYYMMDD-〈主题〉`。约定：

```
runs/<id>/
├─ intent.md            # meta-requirement 产出
├─ spec.md
├─ acceptance.md
├─ failure-map.md       # 轻量单可内嵌 acceptance.md
├─ state.json           # 状态落盘（阶段/状态/重试/证据/下一步），不落聊天记录
├─ run-note.md          # 执行笔记（第 0 步判定含域外警示时同步标注）
├─ friction.md          # 摩擦记录：每卡一次记一条，归因 A/B/C/D，每条有回写动作
├─ escalations/         # 升级包 E-YYYYMMDD-NN.md（流程问题用 EP-）
└─ terms/               # 术语表落盘（术语表-第N单-〈主题〉.md，跨单累积）
```

## 归因口径（friction.md 用）

- **A 类**：标准缺口——没有对应失败模式/形态卡覆盖 → 修标准（先入 failure-modes.md 再回写 skill）
- **B 类**：执行错误——标准有但没执行到位 → 修执行
- **C 类**：环境/工具问题 → 修环境或绕行
- **D 类**：需求本身变化 → 走修订轮，验收合同同步修订

## 纪律

1. 状态只落 state.json，不落聊天记录。
2. 升级包预算每单 ≤3 包；超预算 = 标准缺口信号（A 类），修标准不是加问。
3. 交付前复盘没做，G3 不放行。
4. **本目录内容严禁纳入版本管理**（含真实环境取证材料）；发布/外发前必须整体剔除本目录。
