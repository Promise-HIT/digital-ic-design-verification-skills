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
