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

**读取 UVM 计数**。对单次仿真日志运行 `python <技能目录>/scripts/read_uvm_summary.py sim.log`。[读取器](../scripts/read_uvm_summary.py)查找标准 UVM Report Summary，接受常见的 ModelSim transcript 行前缀。返回 0 表示该摘要的 ERROR、FATAL 计数均为零，1 表示至少一项非零，2 表示缺行、重复或格式不匹配。输出含原始行号。若项目重写 report server，应针对其真实输出编写解析器。合并回归先拆分到每个 run，再与结束标记、仿真器状态、比较次数合并判断。

**Vivado Tcl**。已取得项目生成的 DCP 时，在工程选定的 Vivado 版本中运行以下命令，把两个报告写入新目录。报告对应输入 DCP 所处阶段。脚本打印版本与时钟数，报告内包含未约束路径信息。检查输入或报告生成失败会返回非零退出码。[Tcl 脚本](../assets/vivado-checkpoint-reports.tcl) · [UG835 命令参考](https://docs.amd.com/r/en-US/ug835-vivado-tcl-commands/report_timing_summary) · [UG894 报告输出](https://docs.amd.com/r/en-US/ug894-vivado-tcl-scripting/Redirecting-Output)

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
