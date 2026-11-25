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
