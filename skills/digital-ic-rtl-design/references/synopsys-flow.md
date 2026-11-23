# Synopsys 工程入口与报告

《静态时序分析与逻辑设计》PDF 第 12 页将 setup 和 hold 分别定位在采样边沿前后。在 PrimeTime 中为同一接收寄存器分别取 max 和 min 报告，圈出数据到达、数据要求与捕获边沿。手算一条示例：setup 的到达为 0.93 ns、要求为 0.90 ns，slack 为 −0.03 ns；hold 的到达为 0.12 ns、要求为 0.08 ns，slack 为 +0.04 ns。把两种检查各自的符号、单位和实际报告对齐，再决定是缩短组合路径，还是把最短路径问题交给实现阶段。

从仓库 Makefile、filelist、Tcl、SDC 和已完成 run 的命令记录还原版本、top、宏、include、库映射与参数。复用匹配版本的项目入口，在新的运行目录保存日志。需要额外许可证或缺少目标库时，列出下一步所需输入。

| 任务 | 工具和输入 | 操作与判据 |
| --- | --- | --- |
| 编译与仿真 | VCS，匹配语言模式的 filelist、TB top、UVM 库 | 单独记录编译/展开和 simv 的退出码。固定 seed 和 test，核对 banner、首错、UVM_ERROR/FATAL、实际比较次数、未完成事务。 |
| 定位错拍 | Verdi，匹配本次编译的调试数据库和波形 | 从首个失败事务的接受拍回溯 valid、ready、payload、reset 和 scoreboard 采样点。确认波形与配置及 seed 一致。 |
| 静态检查 | VC SpyGlass，RTL、时钟/复位定义、同步器识别配置 | 按 crossing 检查电平、脉冲、多位数据和重汇合；逐项给 waiver 的同步结构、数据保持时间和复位假设。 |
| 综合 | Design Compiler，目标和链接库、RTL、SDC、顶层 | 在项目 dc_shell 流程中核对 analyze/elaborate/link、check_design、时钟与路径组。审查寄存器、锁存器、RAM 推断、未解析引用、面积与关键路径。 |
| 等价 | Formality，匹配的 RTL、综合网表、库和映射信息 | 分开记录 matched、unmatched、failing 和 aborted points。回溯第一个有差异的锥，检查参数、黑盒与复位建模。 |
| 时序 | PrimeTime，网表、库、SDC、工作模式/角和相应寄生 | 先 check_timing，再看 report_timing 中 max/min 路径的起终点、launch/capture 边沿、例外和 slack。列出未约束端点以及报告覆盖的角。 |

若现有 VCS 工程已经用 `-f rtl.f` 编译，先检查相对路径基准、包顺序、语言模式和库，再给出适合它的完整命令。例如单时钟纯 SV smoke 可从 `vcs -sverilog -f rtl.f -top tb_top -o simv` 和 `./simv -l smoke.log` 起步，前提是 filelist 已含 TB 且当前目录允许生成编译产物。UVM 工程应沿用其库选项和 test plusargs。新增 SDC 例外需从协议或时钟关系解释被排除的路径，并检查例外前后的路径集合。
