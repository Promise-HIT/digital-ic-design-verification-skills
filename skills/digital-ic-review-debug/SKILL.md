---
name: digital-ic-review-debug
description: 数字 IC RTL 与验证评审、故障调试和签核缺口分析：检查 SystemVerilog、lint/编译/仿真/CDC/RDC/综合/STA/形式日志，定位协议、位宽、复位、X、竞态及 coverage 问题。用于审查或诊断；仅在用户明确要求修复时编辑代码。
---

# 数字 IC 评审与调试

交付可定位、可复现、说明实际影响的 findings 或首因结论，避免风格噪声。

整体任务需要衔接设计、验证和实现阶段时，读取配套 RTL skill 的 [开发流程](../digital-ic-rtl-design/references/development-flow.md)；工具流程问题读取 [EDA 使用与脚本开发](../digital-ic-rtl-design/references/eda-workflow.md)。小任务只取相关阶段。

## 权限与判断

- 审查、诊断或解释请求：只读检查并报告，不修改代码。
- 明确要求修复：完成范围内的本地修改和非破坏性验证。
- 扩展范围、破坏性操作或新增大量资源成本时先核对现有授权；正常只读诊断与已授权修复持续完成。
- 证据不足时标记“待确认”，不把猜测写成缺陷；无可确认问题时明确检查范围和残余风险。

## 执行流程

1. 读取 diff、相关规格/接口、相邻模块、调用点、filelist、约束与测试入口。保护用户未提交改动。
2. 固定 commit、top/config、seed、工具版本和命令；找到最早错误时间或首条因果诊断，而不是最后的 timeout。
3. 按功能/协议、可综合语义、clock/reset/CDC/RDC、timing/DFT、验证充分性排序检查。
4. 写一个可证伪假设，用最小观察或实验区分 DUT、TB、约束和工具/环境问题；一次改变一个因素。
5. 若获授权修复，先保留能复现原问题的测试或断言，再做最小修复并运行邻近回归。

长日志可直接执行 `python3 scripts/summarize_diagnostics.py <log>`；无需先读取脚本源码，分类结果必须回到原始上下文核实。

## Findings 标准

- `P0`：可能造成硅失效、安全/数据破坏或大范围签核错误。
- `P1`：明确功能错误、死锁、CDC/RDC/综合风险，或验证会漏掉严重问题。
- `P2`：配置/边界问题、重要验证缺口，或很可能诱发错误的设计缺陷。
- `P3`：有证据的低风险改进；纯格式偏好通常不报告。

每项使用 `[严重度] 标题 — file:line`，随后说明触发条件、影响、证据和最小修复方向。先给 findings，再给整体说明。

## 审查不变量

- 不从 warning 数量、lint clean、当前无 X 或已有测试通过推断设计正确。
- 不全局关闭 warning，不用增大 timeout、更换 seed、扩大 `disable iff` 或放松 scoreboard 比较掩盖失败。
- 必查协议边界、宽度/signedness、阻塞/NBA 调度、组合完整性、复位释放、多 bit CDC、TB race 和 checker 独立性。
- 用户只要求审查或诊断时不得编辑文件。

## 按需读取

- 系统性代码/diff 审查：[references/review-matrix.md](references/review-matrix.md)
- 仿真、断言、scoreboard 或 timeout 分诊：[references/failure-triage.md](references/failure-triage.md)
- tapeout/milestone 或完整 closure 评估：[references/signoff-checklist.md](references/signoff-checklist.md)

## 深入分诊

- 边界/背压、UVM 早退或 hang、对象别名、形式空证明等症状：[failure-patterns.md](references/failure-patterns.md)。
- 书籍来源与版本限制：[local-library.md](references/local-library.md)。
- UVM API 争议：优先核对配套验证 skill 的 [官方依据](../digital-ic-verification/references/official-uvm.md) 和工程实际库。

引用源码、书中案例或工具警告时，仍需建立“合法触发 → 错误机制 → 可观察影响”的证据链。未证明的怀疑不写成已确认 bug；缺少仿真/CDC/STA 证据时明确范围。

## 完成输出

按严重度给 findings；再给重现命令与结果、待确认项、未运行检查和残余风险。没有 findings 时不要虚构问题。
