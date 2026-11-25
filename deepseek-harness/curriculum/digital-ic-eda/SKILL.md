---
name: digital-ic-eda
description: 数字 IC 与 FPGA 工程的 EDA 工具使用、日志判读和 Tcl、Python、Shell 流程脚本。按实际工具与版本处理编译仿真、lint、CDC/RDC、形式、综合、DFT、布局布线、STA、功耗、物理签核及 ECO。
---

# EDA 工具、报告与流程脚本

先确定用户需要的工程结论，例如“这次 RTL 修改是否改变了综合网表的行为”或“布线后哪组 hold 路径失败”。从已有 Makefile、filelist、Tcl、runset 或 CI 作业定位产生该证据的阶段。记下设计版本、top、工具版本、目标工艺或器件、模式与角、输入产物和本次运行目录。


按项目使用的工具选择对应说明。查命令时确认所在 shell、对象类型、设计加载状态、单位和命令帮助。对一次失败保留首条因果错误、原始行号、上游产物和可区分原因的下一项检查。交付脚本或报告时列出实际命令、运行结果、报告路径、关键数值及其覆盖范围。

# 前端工具与逻辑实现

## 编译、仿真与波形

把构建拆为源文件编译、顶层展开和仿真执行。核对语言模式、文件顺序、include 路径、宏、库映射和选定的 top。包或模块未解析时，从第一次声明不可见的位置查起。仿真运行才会用到的 test plusarg 和 seed 应记录在执行命令。门级仿真另查网表、单元模型、SDF 实例映射、时标、注回覆盖与 timing-check 选项。

| 工具链 | 项目入口与证据 |
| --- | --- |
| VCS、Verdi、URG | 沿用项目的 VCS 编译或分步脚本，确认生成的 simv 与此次运行相同。检查运行日志的用例名、seed、断言、scoreboard 及结束原因。Verdi 打开匹配构建的源码和波形；FSDB 的生成取决于项目的 dump/PLI 设置。用 URG 汇总时核对覆盖数据库对应的设计、覆盖模型和排除项。 |
| Questa/ModelSim | 常见顺序为 vlib、vmap（需要映射时）、vlog/vcom 和 vsim。将工作库放在本次运行目录。排查仿真 time 0 时，先区分顶层加载失败、初始化 fatal 和零时间循环。批处理显式返回成功或失败，并另查断言和 TB 终止原因。 |
| Xcelium、SimVision | 从工程 xrun 或分步入口取得快照、库与运行参数。确认加载的 snapshot、UVM test 及波形数据库属于同一次构建。检查覆盖配置和数据库后再用项目覆盖工具合并。 |
| Verilator | 用本版支持的 --lint-only 检查可解析的 RTL。仿真模型、时序选项、断言、四态和覆盖支持须按版本及所用构造判断。将命令行的宽度告警追到赋值两侧的位宽与符号。 |

**调度示例**。UVM summary 中 error/fatal 为零但输出比较次数为零时，沿 driver、输入接受、输出接受、monitor、scoreboard 找到第一个缺失事件。在首个分歧拍同时观察 clock/reset、有效位和数据。先定位该拍，再决定是否扩大波形层次。

## 静态、形式、综合与 DFT

| 分析及常用工具 | 最低输入 | 如何读结果 |
| --- | --- | --- |
| Lint、CDC/RDC（VC SpyGlass、Questa、Jasper CDC 等） | 一致展开的 RTL、主/生成时钟、复位域、模式、黑盒和同步结构定义 | 先查未识别时钟、未分析域和约束匹配数，再按 crossing 看源/目的域、首级扇出、多位重汇合及复位释放。waiver 定位到具体结构与成立条件。 |
| 属性验证（VC Formal、Jasper、Questa Formal、SBY） | harness、时钟/初始状态、assume/assert/cover、引擎、深度或时限 | 区分反例、已证明、深度内通过、未知/超时。排查不可达前件或互相矛盾的假设；读反例时记录第一个违反契约的采样，不直接把最后一拍当根因。 |
| 综合（DC/Design Compiler、Fusion Compiler、Genus、Yosys） | top、参数、技术/链接库、约束、预期存储资源和目标网表 | DC 的 analyze/elaborate 或本工程读取入口后核对 link 与 check_design。检查未解析引用、推断的寄存器/RAM/latch，再比面积和时序。同工艺、库角、约束下比较。Yosys 的 check -assert 可将其识别的结构问题作为脚本失败条件。 |
| 等价性（Formality、Conformal、EQY） | 指明 golden 与 revised、库、参数、黑盒、映射线索、scan/test 模式 | 分开记录未配对点、已证明点、失败点和中止点。单看“零失败”会漏掉未比较的逻辑。沿第一个失败点回查约束与两侧逻辑锥。重定时、时钟门控与存储抽象需相应流程支持。 |
| Scan、ATPG、MBIST（TestMAX、Modus、Tessent） | test clock/reset、scan enable、单元及链配置、测试模式约束、目标故障模型；存储器测试还需 macro 描述 | 先查 DFT DRC、链连通、shift/capture 时钟与 X 源。ATPG 报告注明故障模型、分母与 detected、untestable、aborted 等分类。记录 pattern 数/覆盖、模式仿真及 chain reorder 后的对应关系。MBIST 单列所测存储器和算法。 |

选择形式工具模式前核对其具体含义。SBY 的 bmc、prove、cover 有不同目标，EQY 处理两个设计之间的等价。模拟工具的命令选项按当前版本确认。[SBY 文件参考](https://yosyshq.readthedocs.io/projects/sby/en/latest/reference.html) · [EQY 手册](https://yosyshq.readthedocs.io/projects/eqy/en/latest/) · [Verilator 命令参考](https://verilator.org/guide/latest/exe_verilator.html) · [Yosys 0.50 check](https://yosyshq.readthedocs.io/projects/yosys/en/v0.50/cmd/check.html) · [Tessent FastScan 产品说明](https://resources.sw.siemens.com/en-GB/fact-sheet-tessent-fastscan/)

# 实现、寄生提取与签核

| 阶段与代表工具 | 本阶段需要的输入和动作 | 交接前检查的证据 |
| --- | --- | --- |
| Floorplan、供电规划、placement（Innovus、ICC2/Fusion Compiler、OpenROAD） | 匹配网表、工艺与单元 LEF、宏、Liberty、SDC/MMMC 设置；指定核区、IO、宏的朝向、阻挡与 PDN。 | 供电连通、合法放置、利用率与局部拥塞。记录 pre-CTS 的时钟假设以及寄生估算来源。 |
| CTS、global/detailed route | 选中 clock root、允许的 clock cell、模式及 RC 环境；核对时钟传播、布线约束、实际布通及天线修补。 | 比较每个时钟的插入延迟、skew、setup/hold 和转换时间；检查未连线、拥塞与路由违规。分别标明 global route 估计和 detailed route 结果。 |
| RC 提取（StarRC、Quantus、Calibre xACT、OpenRCX） | 匹配布线后的设计、提取规则、RC corner、耦合选项、层映射及名称映射。 | 核实 SPEF 等交接产物的单位、corner、注回覆盖和未匹配网络。网表或金属发生 ECO 后使受影响的寄生结果失效。 |
| STA / SI（PrimeTime、Tempus、OpenSTA） | 对应网表、Liberty、SDC、寄生与分析视图；按项目设置 OCV、串扰、时钟传播及模式。 | 先查缺失时钟、未约束端点、例外命中与禁用 timing arc，再按模式/角及 max/min 读 WNS、TNS、违例端点和一条完整路径。读 launch/capture 边沿、时钟路径与不确定度。setup slack 为 required−arrival，hold 为 arrival−required。 |
| 低功耗与功耗（Power Compiler、PrimePower、Joules 等） | 检查 UPF 域及状态、隔离、level shifter、retention；活动估计还需匹配 workload、时间窗、VCD/SAIF 实例路径、库角和时钟。 | 将结构/电源感知功能检查与功耗估算分别报告。注明活动注回比例、默认活动、internal/switching/leakage 分类和单位。比较两个 mW 数前先对齐输入。 |
| 供电完整性（RedHawk-SC、Voltus、OpenROAD PDNSim 等） | 电网抽取、供电点与电压、功耗/电流分布，动态分析另需随时间变化的激励。 | 记录静态或动态 IR 的模型、最坏电压位置及条件；EM 核对层、线/过孔电流和工艺限值。静态 IR 结果适用于对应的负载假设。 |
| 物理验证与交付（Calibre、IC Validator、Pegasus、KLayout 等） | GDSII/OASIS、工艺层映射、匹配的 foundry runset；LVS 还需原理/源网表、抽取与电源网映射。 | DRC 按规则与几何 marker 归类；LVS 检查顶层、opens/shorts、器件和端口差异；另核对适用的 ERC、antenna、density/fill 及豁免。记录 deck 版本与顶层。 |
| ECO 与重签核 | 给出变更前后网表/版图版本、受影响逻辑锥和物理范围。 | 按更改重跑等价、提取、各视图 setup/hold、DRC/LVS 以及受影响的供电或测试检查。列明仍沿用的报告对应哪个设计版本。 |

**时序日志实例**。某 setup path 的 arrival 为 2.35 ns，required 为 2.20 ns，其 slack 为 −0.15 ns。若改动前的“正 slack”来自综合估计，改动后来自布线后慢角，两数不能直接归因为 RTL 退化。先在相同 netlist、view、寄生与时钟口径下找出数据路径或约束的差异。另查 hold 视图。

**FPGA 分支**。Vivado 读取 XDC、器件与 speed grade，Quartus 读取工程 revision、器件、SDC 等设置。按 synth、place/fit、route、时序/DRC、bitstream 或汇编产物保留日志。查看实现后的时序覆盖、未约束路径、CDC/时钟交互、资源与时钟网络。比较同器件、同阶段、同约束结果。IP 或器件更换后优先检查约束对象仍能匹配。[Vivado 实现报告](https://docs.amd.com/r/2026.1-English/ug904-vivado-implementation/Reporting-in-Non-Project-Mode) · [Quartus Timing Analyzer 手册](https://cdrdv2-public.intel.com/774741/ug-683243-774741.pdf)

公开可复查的实现流程、STA 交接格式与版图结果判读见 [OpenROAD Flow Scripts 教程](https://openroad-flow-scripts.readthedocs.io/en/latest/tutorials/FlowTutorial.html)、[OpenSTA 项目文档](https://github.com/The-OpenROAD-Project/OpenSTA)、[KLayout DRC 手册](https://www.klayout.de/doc/manual/drc_basic.html) 和 [KLayout LVS 手册](https://www.klayout.de/doc/manual/lvs_intro.html)。正式交付采用项目指定的工艺规则与签核配置。

# 工具脚本与日志

**脚本的三个边界**。Shell/Make 管理进程、参数、文件和退出码。EDA 内嵌 Tcl 查询已加载设计的对象、施加约束、显式写出报告。Python 解析日志、关联配置和汇总回归。沿用工程已有入口与相对路径语义，尤其留意不同工具对 filelist 内相对路径的解释。生成新 run 目录，避免读取上次的 summary、checkpoint 或 coverage 数据库。

## 从日志到结论

| 看到的现象 | 先读哪份证据 | 可以作出的判断 |
| --- | --- | --- |
| 包装脚本报 missing netlist | 上一阶段命令、退出状态、首个 error 及实际输出路径 | 若上一阶段 link 就失败，missing netlist 是下游症状。保留第一条未解析引用的文件位置和 library 配置。 |
| 日志里出现许多 ERROR 字样 | 结合工具消息格式、消息编号、前后文、结尾状态与新生成的报告 | 帮助文本、预期负测和“0 errors”也可能命中关键字。长日志先按阶段和实例聚类，再回原始行核对。 |
| 仿真进程返回 0 | 读用例及 seed、设计实际接受数、比较数、UVM summary、SVA 与仿真器级错误、watchdog 和正常结束标记 | 故意翻转一个被比较的有效数据位，验证此配置能在预期位置失败。不同仿真器或 UVM report server 的格式可不同。 |
| STA 看起来全绿 | 同一视图的 check_timing、时钟、例外匹配、约束覆盖、最差路径和 setup/hold 汇总 | 若目标域没有采集到路径，记录缺失覆盖与起终点条件，重新生成该视图。 |
| 工具未运行/超时、许可证或 PDK 无法加载 | 工具启动记录、日志完整性、依赖版本和上游输入 | 将本次状态记为 unavailable、timeout 或 incomplete。修正依赖后从首个受影响的阶段重跑。 |

## 可直接使用的例子

**读取 UVM 计数**。对单次仿真日志运行 `python <技能目录>/scripts/read_uvm_summary.py sim.log`。[读取器](scripts/read_uvm_summary.py)查找标准 UVM Report Summary，接受常见的 ModelSim transcript 行前缀。返回 0 表示该摘要的 ERROR、FATAL 计数均为零，1 表示至少一项非零，2 表示缺行、重复或格式不匹配。输出含原始行号。若项目重写 report server，应针对其真实输出编写解析器。合并回归先拆分到每个 run，再与结束标记、仿真器状态、比较次数合并判断。

**Vivado Tcl**。已取得项目生成的 DCP 时，在工程选定的 Vivado 版本中运行以下命令，把两个报告写入新目录。报告对应输入 DCP 所处阶段。脚本打印版本与时钟数，报告内包含未约束路径信息。检查输入或报告生成失败会返回非零退出码。[Tcl 脚本](assets/vivado-checkpoint-reports.tcl) · [UG835 命令参考](https://docs.amd.com/r/en-US/ug835-vivado-tcl-commands/report_timing_summary) · [UG894 报告输出](https://docs.amd.com/r/en-US/ug894-vivado-tcl-scripting/Redirecting-Output)

```shell
vivado -mode batch -source /path/to/vivado-checkpoint-reports.tcl -tclargs routed.dcp reports/new-run
```

**写通用 Tcl**。用 list/lappend 构造含空格的路径与参数，通过 `{*}$args` 展开一个合法 Tcl 列表。检查选择器的命中数与对象类型；Vivado 的对象列表可用 llength，而 Synopsys collection 应用对应 shell 的 sizeof_collection 等 API。先验证数量，再施加时钟、例外或生成报告。对关键命令用 catch 捕获解释器错误，并核对工具自己报告的失败与结果对象。

**保存外部命令状态**。Bash 需要将输出经 tee 保存时，立即复制管道中两个退出码；使用项目实际的 phase 脚本，并保留具体失败码。PowerShell 使用外部进程的 $LASTEXITCODE，Python 用 subprocess 的参数数组、显式 cwd、timeout 和返回码。将超时和启动失败保存在结果中。

```bash
#!/usr/bin/env bash
# Usage: capture.sh NEW_LOG COMMAND [ARG ...]
log=$1
shift
"$@" 2>&1 | tee "$log"
codes=("${PIPESTATUS[@]}")
if (( codes[0] != 0 )); then exit "${codes[0]}"; fi
exit "${codes[1]}"
```

提取指标时同时保存报告路径、行号、单位、分析视图和工具版本。取不到 TNS、比较数或覆盖分母时写 missing。跨版本修改 parser 前至少用一份成功输出、一份失败输出和一份截断输出验证。

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
