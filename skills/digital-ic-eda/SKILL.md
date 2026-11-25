---
name: digital-ic-eda
description: 数字 IC 与 FPGA 工程的 EDA 工具使用、日志判读和 Tcl、Python、Shell 流程脚本。按实际工具与版本处理编译仿真、lint、CDC/RDC、形式、综合、DFT、布局布线、STA、功耗、物理签核及 ECO。
---

# EDA 工具、报告与流程脚本

先确定用户需要的工程结论，例如“这次 RTL 修改是否改变了综合网表的行为”或“布线后哪组 hold 路径失败”。从已有 Makefile、filelist、Tcl、runset 或 CI 作业定位产生该证据的阶段。记下设计版本、top、工具版本、目标工艺或器件、模式与角、输入产物和本次运行目录。

- [前端、综合与可测性](references/frontend.md) 用于编译仿真、波形与覆盖、lint、CDC/RDC、形式、综合、等价和 DFT。
- [实现、提取与签核](references/implementation.md) 用于 floorplan 到 GDS、寄生提取、STA、功耗、IR/EM、DRC/LVS、ECO，以及 FPGA 实现。
- [日志判读与流程脚本](references/automation.md) 用于从原始报告定位失败、编写 Tcl/Python/Shell 和构造可重跑的检查。
- [手册与版本](references/manuals.md) 用于核对本地 User Guide、公开命令参考以及需要客户账号的产品文档入口。

按项目使用的工具选择对应说明。查命令时确认所在 shell、对象类型、设计加载状态、单位和命令帮助。对一次失败保留首条因果错误、原始行号、上游产物和可区分原因的下一项检查。交付脚本或报告时列出实际命令、运行结果、报告路径、关键数值及其覆盖范围。
