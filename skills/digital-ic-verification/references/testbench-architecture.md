# Testbench 与 UVM 架构

## 选择复杂度

小型纯组合/短时序模块优先自检查 procedural bench；接口复用、多 agent、长回归或覆盖驱动项目再采用 class/UVM。架构层数应由复用和并发需求证明，而不是默认套模板。

## 职责分离

- sequence/generator：产生意图与 transaction，不碰 DUT pin。
- driver/BFM：把 transaction 映射为协议时序，处理 ready/backpressure。
- monitor：无副作用地采样并重建实际 transaction。
- reference model/predictor：从输入和配置计算期望行为。
- scoreboard：按规则匹配 actual/expected，处理乱序、超时、reset/flush。
- assertion：检查周期级协议和局部不变量。
- coverage collector：记录已观察到的需求场景，不制造 stimulus。

## 接口与竞态

使用 interface 封装相关 pin；项目支持时用 clocking block 定义驱动/采样偏移，避免 TB 与 DUT 在同一时间槽竞态。不要混淆 program/block、clocking region 与简单 `@(posedge clk)` 的行为，具体以工具和 IEEE 语义为准。

## 生命周期

测试启动需确定配置、reset、agent 连接和 checker 清空顺序；结束条件以 transaction/objection/显式 drain 为准，不靠任意等待。结束前确认队列为空、无 outstanding、无被抑制的 assertion 和无 `randomize()` 失败。

## 可调试性

transaction 需稳定 ID、时间、源、配置和简洁打印。日志分级；默认只打印关键路径，失败时能提升局部 verbosity。比较器报告首个差异及足够上下文，避免输出整块海量数据。
