# 综合、SDC 与实现反馈

用于 RTL 改动影响关键路径、RAM/ICG 映射，或需要解释综合/STA 时。流程和约束以项目为准；历史教材中的工具命令不是当前版本保证。

## 约束审查

逐项核对 primary/generated clocks、period/waveform、clock relationship、I/O delay 的 min/max、input transition/output load、clock uncertainty、工作模式/角。若需求未给频率和 I/O 时序，记录缺口，不编造目标后宣称收敛。

区分 setup、hold、recovery/removal、clock gating checks；定位起点/终点、launch/capture edge、数据/时钟路径以及 exception。修 setup 的流水化会改变延迟/flush/sideband，修 hold 通常依赖实现端，不用随意增加 RTL `#delay`。

false path、多周期、异步 clock group 都需要结构和协议理由。multicycle 的 setup/hold 配对依赖具体边沿语义；不机械给所有路径加 N/N-1。宽泛 `set_clock_groups` 或 false path 可能遮盖本来要约束的 Gray 总线物理时序，检查约束优先级。

## 综合后反馈

核对 latch、多驱动、未连接/常量输出、未约束路径、被裁掉的状态、RAM/DSP/ICG 实际推断及高扇出。面积/时序比较使用同一库、约束、模式和工具选项。等价检查要说明 reset/初始化、black box、参数和映射假设。

clock enable 优先于组合造钟；必须门控时使用已批准 ICG/厂商原语与 test-enable 策略，并检查 scan/test mode。低功耗模块额外定义 isolation、retention、power-up/down 顺序，缺少 UPF/电源意图时不宣称低功耗签核。

## 闭环

关键路径报告 → 判断逻辑深度/扇出/存储结构/约束问题 → 最小改动 → 功能回归 → 重新综合/STA。只改变约束就通过时，必须解释为什么新约束真实反映环境。
