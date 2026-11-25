# 选择对应产品和版次的依据

**课程库已核对的用户手册**。以下是资料封面所列版次。工程使用其他版次时，用本机 help/man、随安装提供的文档和项目已有命令核对语法。

| 用户手册 | 建议查找的主题 | 决策示例 |
| --- | --- | --- |
| Synopsys VCS User Guide，S-2021.09 | Compilation/Elaboration、Runtime Options、Timing Back-annotation、Coverage | 当前开关属于构建还是运行；SDF 用了哪份网表和层次。 |
| Synopsys HDL Compiler for Verilog User Guide，O-2018.06 | Register Inference Guidelines、存储器、可综合语言构造 | 由 RTL 与目标库判断推断的结构，再查实际综合报告。 |
| Synopsys Design Compiler User Guide，P-2019.03 | design libraries、link、check_design、constraints、timing/area reports | 核对 top、link/target library 和未解析引用，之后再解释面积与 QoR。 |
| Synopsys Power Compiler User Guide，U-2022.12-SP3 | read_saif、未注回活动、report_power、clock gating | 分清功耗报告中的活动来源，复核实例映射、时间窗和默认估计。 |
| Mentor Graphics ModelSim SE Reference Manual，10.1c（工具安装随附） | vlib、vmap、vlog、vsim、do、quit | 核对库、顶层及 batch 退出状态；其他版本按随附参考复核。 |

本地《Static Timing Analysis for Nanometer Designs: A Practical Approach》可用于时序概念。课程文件 VERDIUserManual.pdf 的正文是环境数据可视化软件 VERDI 2.2。需要 Synopsys Verdi、PrimeTime、StarRC 等产品的精确选项时，从相应版本的 Documentation on the Web 或安装手册查询。[Synopsys 官方文档入口](https://www.synopsys.com/support/licensing-installation-computeplatforms/synopsys-documentation.html)

**公开资料与受控手册**。公开命令参考适合作为可复制示例的依据。商业产品页用于确认产品职责；需要客户账号的详细命令应先查已许可版本。

| 缺少本地手册的方向 | 官方查询入口 |
| --- | --- |
| Cadence 仿真、形式、综合、实现与签核 | 在 Cadence Online Support 按产品和 release 查 Xcelium、Jasper、Genus、Conformal、Innovus、Tempus、Quantus、Voltus、Modus 等的 User Guide / Command Reference。[Cadence Support](https://www.cadence.com/en_US/home/support.html) |
| Siemens 验证、DFT、物理验证 | 在 Customer Center 按 Questa、Tessent 或 Calibre 的安装版次选择文档。公开产品资料可核对 ATPG 与 LVS 的用途。[Siemens 支持入口](https://support.sw.siemens.com/) · [Calibre 电路验证](https://www.siemens.com/en-us/products/ic/calibre-design/circuit-verification/) |
| 开源前端与形式 | [Verilator 用户指南](https://verilator.org/guide/latest/exe_verilator.html) · [Yosys 0.50 命令参考](https://yosyshq.readthedocs.io/projects/yosys/en/v0.50/cmd/check.html) · [SBY 配置参考](https://yosyshq.readthedocs.io/projects/sby/en/latest/reference.html) · [EQY 手册](https://yosyshq.readthedocs.io/projects/eqy/en/latest/) |
| 数字后端、寄生与物理验证 | [OpenROAD Flow Scripts 教程](https://openroad-flow-scripts.readthedocs.io/en/latest/tutorials/FlowTutorial.html) · [OpenROAD 官方源码与模块文档](https://github.com/The-OpenROAD-Project/OpenROAD)（src/rcx、src/psm、src/dft） · [OpenSTA](https://github.com/The-OpenROAD-Project/OpenSTA) · [KLayout LVS](https://www.klayout.de/doc/manual/lvs_intro.html) |
| FPGA 实现、分析与 Tcl | [Vivado UG894](https://docs.amd.com/r/en-US/ug894-vivado-tcl-scripting/Redirecting-Output) · [Vivado UG835](https://docs.amd.com/r/en-US/ug835-vivado-tcl-commands/report_timing_summary) · [Quartus Prime Pro Scripting](https://cdrdv2-public.intel.com/721822/ug-qpp-scripting-683432-721822.pdf) · [Quartus Prime Pro Timing Analyzer](https://cdrdv2-public.intel.com/774741/ug-683243-774741.pdf) |
