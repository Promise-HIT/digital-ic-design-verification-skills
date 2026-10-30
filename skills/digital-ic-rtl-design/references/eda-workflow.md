# EDA 工具使用与流程脚本开发

目的：让工具回答一个明确工程问题，并留下可复现证据。先读项目脚本和已安装版本帮助；以下工具名仅作能力映射，不是购买建议或可直接执行的命令配方。

## 阶段与问题映射

|环节|要回答的问题|关键输入|重点输出/复核|
|---|---|---|---|
|解析/展开|当前配置实际形成什么设计？|top、filelist、语言模式、include、宏、参数、package 顺序|未解析模块/包、端口/层次、generate 分支、重复定义|
|lint|有没有高概率 RTL 语义错误？|同一编译配置、设计约束、规则集|latch、多驱动、宽度/符号、不可达/不完整分支；最窄范围 waiver|
|仿真|在所测事务下是否符合契约？|DUT/TB、模型、test、seed、运行选项|首个失败、接受/比较次数、协议/断言、结束条件；退出码和报告一起判断|
|波形调试|错误首先在哪里产生？|同配置 debug 数据库、失败时窗、层次与源码|从第一个错误反推数据/控制来源，追踪 driver；不以最终 timeout 定根因|
|CDC/RDC|跨域结构、相干性和复位协议是否成立？|时钟/复位定义、mode、同步器识别、环境假设|全部 crossing 分类、reconvergence、同步结构、约束和 waiver|
|属性形式|特定不变量在已建模环境下是否成立？|DUT、assert/assume/cover、reset/clock、抽象|反例、可达性、vacuity、深度、证明/未决分类|
|综合|RTL 映射成什么结构，代价如何？|RTL、目标库/宏、SDC、工况/模式、映射选项|未链接/black box、latch、RAM/ICG、面积、关键路径与高扇出|
|等价检查|RTL 与网表/优化前后是否等价？|reference/implementation、映射、库、宏、参数、reset 假设|匹配点、unmatched/aborted/failing；不能把 aborted 当通过|
|STA|在真实时序约束下是否满足 setup/hold 等要求？|网表、库、SDC、寄生、mode/corner|未约束路径、异常约束、起终点/边沿、slack、recovery/removal|

项目可能使用 VCS/Verdi/VC SpyGlass、Design Compiler/PrimeTime/Formality，或其他厂商的等价工具。开放工具可承担适合其版本能力的环节；不可默认它们支持完整 UVM/class/SVA、工艺库或商业签核模型。

官方定位入口（沿用原包链接，使用时核对）：[VCS](https://www.synopsys.com/verification/simulation/vcs.html)、[静态/形式验证](https://www.synopsys.com/verification/static-and-formal-verification.html)、[CDC](https://www.synopsys.com/verification/static-and-formal-verification/vc-spyglass/vc-spyglass-cdc.html)。产品页面只说明能力；精确命令仍查本地版本手册与工程模板。

## 使用工具的操作顺序

1. 明确本次问题和范围：新模块编译、某次 mismatch、某条 CDC crossing 或某条 timing path。
2. 找到并固定配置：源文件/库、top、参数、宏、约束、工具版本。不要在几个工具里维护互不一致的 filelist。
3. 先跑最小高信号入口：展开/编译和相关 smoke；再根据风险扩大。日志首因未解决时，不重复提交大回归。
4. 看报告上下文：定位源代码和真实配置，区分设计 bug、缺约束、模型、工具限制或环境错误。
5. 修改原因对应的对象，再跑原失败和相邻边界；性能/面积比较固定库、约束和模式。

## 开发 Tcl/Python/Shell 流程时

- 配置与动作分离：配置记录 top、filelist、include/defines、参数、库/宏、SDC、test/seed 和工具适配；脚本执行这些配置，不在多个脚本硬编码同一事实。
- 复用已有 Make/runner/Tcl 入口。没有入口时，先实现一个真实可跑的 compile→smoke 纵向流程，再扩展 lint、回归或报告；不要先造庞大框架。
- Tcl 使用 list 组织命令参数，路径正确引用；Python 优先 `subprocess` argv，明确 cwd/环境；Shell 保持平台一致。不要把日志、PDF 或源码中的字符串直接当命令执行。
- 输出按 run-id 隔离：配置快照、完整命令、版本、日志、退出码、seed、报告路径。避免旧覆盖数据库或上一轮网表混入当前结果。
- 编译缓存/增量构建的 key 包含源码、宏、参数、库和工具版本；改变这些因素时检查是否应重新编译。不得因缓存存在而跳过必要展开。
- 返回码要真实传递；日志解析作为补充，保留原始日志。timeout、license failure、tool missing、aborted、not run 都与 pass 区分。
- 检查 license/队列/资源限制，按授权范围运行；并行任务不得共用可写 work library、临时文件名或覆盖输出目录。
- 修改脚本后，用受控的成功、失败、缺工具、超时场景验证返回与证据保存。已有 CI 能覆盖时沿用。

需要轻量记录多条命令时使用 [run_hdl_checks.py 的说明](check-execution.md)；成熟回归环境仍优先使用项目 runner。

## 综合与 STA 的反馈思路

综合面积异常：先查结构/推断与参数，不直接改时序约束。时序失败：先确认约束、clock relationship 和路径类别，再判断逻辑深度/扇出/存储读路径/物理实现。流水化会改变接口延迟和取消语义，必须重新跑功能测试。详见 [timing-synthesis.md](timing-synthesis.md)。

不把 LEC 当属性证明，不把 lint clean 当功能正确，不把 CDC 结构通过当跨域协议活性成立，也不把综合估计时序当最终寄生/角覆盖的 STA 签核。
