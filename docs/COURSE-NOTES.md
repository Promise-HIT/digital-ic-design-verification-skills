# 课程资料如何进入 v1.1.0

本次盘点 98 份课程文件。55 份 PDF 建立了全文本或目录索引，扫描教材和文字层编码异常的文档按相关图页核读；31 份 HTML 包括目录和 30 章正文；10 份 Verilog 涵盖两套 APB 示例和一套 FIFO 示例；另有一份 CDC 的 Word 文档以及一份 APB ZIP。ZIP 中 11 个文件的 SHA-256 均能与已展开文件对应。隐藏下载缓存单独排除。以下页码标为“物理页”时，从 PDF 第一页算起。

| 来源及定位 | 转化成的工程任务 |
| --- | --- |
| 《Proverilog 编码规范（草案）》物理第 5 页、《Verilog HDL 电路设计指导书》物理第 16 页、IEEE 1364-2005 与 IEEE 1800-2023 | 明确组合/时序职责、译码覆盖、可综合子集和位宽。历史企业命名与代码组织习惯以项目约定为准。 |
| 《10_同步FIFO》、配套 sync_fifo.v 与 tb_sync_fifo.v、《CDC相关知识点》、《11_亚稳态的产生与恢复》及同步电路设计资料 | 从实际接受事件推导占用量；识别 pointer、RAM 写入、counter 使用不同条件的失配；按信号语义选择跨域结构。课程 FIFO 源文件注明只支持特定二次幂深度。 |
| Arm IHI 0024E 第 2–4 章、IHI 0033C 的传输与响应章节、IHI 0022B、IHI 0022L 修订记录及配套 APB 示例 | 以协议规定完成条件编写 monitor 和断言，分别处理 APB 等待、AHB 相位重叠、AXI 独立通道。AXI4-Lite 另核对官方 H 版 B1。 |
| 《SystemVerilog 验证：测试平台编写指南》第三版物理第 30 页、IEEE 1800-2023 的调度、clocking block、SVA、随机化和覆盖章节、HTML 第 9、13 章 | 分开驱动、观测和预测；用独立模型、命中计数和反例检查 scoreboard 与断言。UVM API 随工程所用库核对。 |
| 《AI处理器硬件架构设计》第 5 章、DNN 高效处理综述、HTML 第 3–5、8、20 和 25 章、IEEE 754-2019 第 4–5 章 | 作为数据通路与工作负载背景，辅助确定功耗活动窗口和验证输入。 |
| IEEE 1801-2018、Power Compiler、Design Compiler、HDL Compiler、VCS 指南、《静态时序分析与逻辑设计》物理第 12 页、STA 教材及工具实例 | 核查电源状态、目标宏、综合推断、仿真入口、时钟约束和 slack 的分析条件。工具参数依安装版本与项目脚本确定。 |
| RISC-V 非特权 ISA、GPGPU 教材、IPD/Linux/Tcl 培训、硬件基础、流片和物理实现章节、面试汇编 | 用于辨别体系结构、工具语言、前端和后端任务的边界。ISA 可选扩展、历史流程或面试答案均需对应项目规格才能用于验收。 |

**采信中的两个取舍**。本地 IHI 0022L 的修订史把 AXI4 等早期接口内容的移除定位在 J 版。AXI4-Lite 的判断使用覆盖该接口的 H 版。课程目录中的 VERDI 2.2 User Manual 第 1.1 节介绍环境建模数据的可视化，它与 VCS/FSDB 调试无关。旧技能所列 UVM 官方归档保留原有出处与版本记录。[Arm IHI 0022H](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)

工具手册的产品、适用版次与厂商入口见 [EDA 手册索引](../skills/digital-ic-eda/references/manuals.md)。
