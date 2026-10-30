# 书籍核心内容与出处

原始材料清单记录了 16 份去重 PDF；UVM 1.1d 教材仅作历史版本背景。公开仓库不包含原书、企业手册、源码包或个人资料目录，也不要求这些文件存在。

skill 保存提炼后的工程方法、适用条件和检查判据，不保存整书转录。具体来源见 [核心内容与取舍](book-source-notes.md)，文件名、ID、页数和哈希见 [source-catalog.json](source-catalog.json)。需要核对公式、图或示例代码时，使用自己合法持有的资料，按文件名与 ID 定位相关页；不默认全文加载或逐页 OCR。

## 阅读路由

|需要解决的问题|skill 中的归纳|优先原始来源|
|---|---|---|
|从规格到交付的开发闭环|[development-flow.md](development-flow.md)|ASIC 工程师手册、SystemVerilog 数字系统设计、需求/调试记录类资料|
|常用模块的选择、契约与验证边界|[common-modules.md](common-modules.md)、[protocol-boundaries.md](protocol-boundaries.md)|Verilog 编程艺术、高级数字系统设计、ASIC 手册、HDL 设计指导书|
|位宽/符号、调度、可综合语义|[language-semantics.md](language-semantics.md)|SystemVerilog 数字系统设计、Verilog 编程艺术|
|时钟/复位/跨域|[clock-reset-cdc.md](clock-reset-cdc.md)|同步电路规范、ASIC 手册|
|EDA 使用与流程脚本|[eda-workflow.md](eda-workflow.md)、[timing-synthesis.md](timing-synthesis.md)|数字 IC 工作学习资料、ASIC 手册、静态时序资料；具体选项查本地版本帮助|
|testplan、随机、checker、覆盖|配套验证 skill 的 verification-plan、checker-and-scheduling 等参考|SystemVerilog 验证指南第二/第三版|
|UVM 架构与 API|配套验证 skill 的 official-uvm、uvm-practical、uvm-sequences-ral|Accellera 官方手册与匹配版库；本地 1.1d 教材仅作辅助案例|
|并行架构/系统背景|仅在任务相关时阅读对应原书章节|GPGPU 设计、硬件工程师、IPD、Linux 教材|

## 采用原则

优先级为项目规格/约束 → 匹配版标准与官方文档 → 经过推导的工程建议 → 书中案例。旧资料的企业命名、审批、特定工艺和过时工具命令不自动成为当前项目要求。遇到有争议的技术表述，核对原图与具体机制后再采用。

读取到资料不代表已验证其中示例代码。只有实际执行且范围明确的编译、仿真、静态或实现结果，才能作为该项验证证据。
