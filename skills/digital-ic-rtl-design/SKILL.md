---
name: digital-ic-rtl-design
description: 数字 IC RTL 设计与实现：把接口规格转化为微架构和可综合 SystemVerilog，并验证 FSM、FIFO、仲裁、流水线、复位及 CDC/RDC。用于新模块、功能修改或 RTL 重构；仅做验证规划或已有失败分诊时使用对应专项 Skill。
---

# 数字 IC RTL 设计

交付与规格一致、可综合、可验证的最小 RTL 变更，并用项目工具给出证据。

## 开发与模块入口

- 从规格到交付、选择当前阶段与裁剪门禁：[development-flow.md](references/development-flow.md)。
- 计数器、FSM、FIFO、仲裁、流水、CSR/RAM、算术/CRC、协议适配：[common-modules.md](references/common-modules.md)。
- 仿真/lint/CDC/综合/等价/STA 的使用思路和 Tcl/Python 流程：[eda-workflow.md](references/eda-workflow.md)。

先选当前任务分支，再按需阅读相关参考；不把完整开发流程强加给小修改。

## 权限与判断

- 解释、规划或审查请求：检查相关材料并报告，不修改代码。
- 实现、修改或修复请求：完成范围内的本地编辑和非破坏性验证，无需为正常读取、编辑或测试反复询问。
- 在用户已授权范围内完成必要检查；破坏性操作、外部发布或显著新增计算/许可证成本，先核对现有授权，只对缺少的授权提问。
- 只在歧义会改变接口、架构或验收结果时提问；否则写明可撤销假设并继续。

## 执行流程

1. 读取适用的仓库说明、构建入口、filelist、相邻模块和测试。保持现有接口、命名、复位及断言风格。
2. 建立契约：端口宽度/符号、时钟域、复位、接受条件、延迟、吞吐、背压、顺序、错误和参数边界。区分规格事实、仓库事实、工具证据和推断。
3. 选择最小微架构，列出状态、数据/控制路径、缓冲、优先级、CDC/RDC 边界、不变量及主要失败场景。
4. 小步实现；避免无关格式化。对高价值局部不变量加入与项目风格一致的断言。
5. 发现并使用仓库已有命令，先跑最便宜的高信号检查：解析/展开、相关 lint、最小 directed test；风险需要时再做综合、形式、CDC/RDC 或 STA。
6. 失败时修复首个根因并重跑最小复现；不要通过关闭 checker、warning 或改变 seed 掩盖问题。

仓库较大且入口不清楚时，可直接执行 `python3 scripts/scan_hdl_project.py <repo>`；无需先读取脚本源码，其输出只提供候选线索。

## 设计不变量

- 组合逻辑完整赋值；时序状态单一驱动。组合优先阻塞赋值，寄存器优先非阻塞赋值。
- 显式处理位宽、signedness、扩展、截断、移位和 `$clog2` 边界；禁止无意 latch、组合环、多驱动与 RTL `#delay`。
- FSM 有明确 default/非法状态策略；不用 `casex` 掩盖 X/Z。
- ready/valid 在 stall 下保持 payload，数据与 valid/metadata 同步推进，无丢失、重复或组合死环。
- 复位说明断言与释放语义；跨域控制、多 bit 数据和复位采用适合各自语义的结构。
- 未运行的综合、时序、CDC 或形式检查只能标为缺口。

## 按需读取

- 新模块、微架构或完成门禁：[references/rtl-workflow.md](references/rtl-workflow.md)
- FSM/FIFO/握手/仲裁/参数化：[references/coding-and-microarchitecture.md](references/coding-and-microarchitecture.md)
- 出现多个时钟、异步输入或局部复位：[references/clock-reset-cdc.md](references/clock-reset-cdc.md)
- 需要选择工具、解释 warning 或组织证据：[references/tool-and-evidence.md](references/tool-and-evidence.md)

通常只读取一到两个相关 reference。

## 实现前的决策记录

新模块先写一张简明表：需求/接受事件、状态量、更新优先级、延迟/吞吐、边界、checker 和验收命令。已有模块只补变更涉及的条目。没有明确定义的协议语义不能从教材例子擅自补为规格。

需要记录时可裁剪 [设计契约模板](assets/design-contract-template.md)，不必为小改动生成完整文档。

优先交付可运行的主路径，再完善边界；第一次仿真先用固定配置/seed，检查 checker 确实观察了数据。修改 FIFO/握手/算术时至少验证一个会触发对应错误的边界；修 bug 先保留原失败复现。不要为了“更完整”无条件重写架构或引入 UVM。

## 深入参考与本地资料

- 算术、signedness、参数、NBA/X、RAM 推断：[language-semantics.md](references/language-semantics.md)。
- FIFO、skid buffer、同时入出、仲裁公平性：[protocol-boundaries.md](references/protocol-boundaries.md)。
- 综合/SDC/STA、ICG、DFT/低功耗：[timing-synthesis.md](references/timing-synthesis.md)。
- 需要解释原理或核对书中规则：[书籍核心内容与出处](references/local-library.md)。按问题回查相关章节，不做整书转录。
- 需要保存多条项目检查证据：[check-execution.md](references/check-execution.md)，使用 `scripts/run_hdl_checks.py`。已有 runner 能满足时沿用项目入口。

规格、仓库事实、书籍建议与实际工具证据分别标识；用提炼后的流程和判据辅助实现，书中示例仍需验证。

## 完成输出

直接给出：结果摘要；关键契约与假设；修改文件；实际命令、版本、退出码和结果；未验证项及残余风险。保留这些内容，压缩背景和重复解释。
