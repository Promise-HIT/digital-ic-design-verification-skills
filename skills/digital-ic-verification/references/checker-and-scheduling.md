# Checker、调度与随机化

## 最小自检查环境

统一 `timeunit/timeprecision`，定义 DUT 边沿、TB 驱动时刻和 monitor 采样时刻。clocking block 的默认 input `#1step` 采边沿前值，input `#0` 的语义不同；选择要与契约一致。不要用任意 `#1` 掩盖 race；简易单时钟 bench 可在相反边沿驱动，在约定边沿采样，但不泛化到多域或双边沿协议。

monitor 根据采样到的接受事件建事务，不能从 generator 的意图直接记 coverage。input/output 同周期发生时明确模型更新顺序；零延迟 bypass 和寄存延迟是不同契约。

比较器输出 ID、输入、期望、实际、配置和周期。对有效数据使用四态检查；对 don't-care/byte enable 做字段级屏蔽，禁止无依据忽略差异。设有界 watchdog，并在正常结束检查 outstanding、queue、错误计数；“等待 N 拍后 finish”不构成通过条件。

## Checker 自检

至少对新 checker 注入一种应当拒绝的错误，例如 payload 单 bit 错、漏响应、重复响应、乱序或 stall 时改变数据。确认测试真的失败，随后撤掉注入恢复通过。若注入无法影响比较路径，说明观察点或 checker 有缺口。规模依风险选取，无需给所有小修改都建完整 mutation 框架。

reference model 按规格使用简单队列/数学模型，不复制 RTL 微架构。对复杂算法用独立实现或可信 golden vector，并说明精度、舍入及来源。

## 约束随机与覆盖

先用 directed 固定语义，再增加随机交互。合法空间和专门 negative test 分开；不要用约束排除 DUT 应支持的边界。检查 `dist`、`solve before`、约束继承/覆盖、动态数组大小、randc 使用限制及约束可解性。

同 seed 只有在代码、工具、配置和随机调用顺序固定时才有可复现意义。随机化对象生命周期、fork 时序和日志对象创建都可能影响随机序列；保存完整配置后再最小化。

covergroup 在真实接受/完成事件采样。分别覆盖 input accepted、output completed 和必要的错误恢复；burst×backpressure×reset 等 cross 根据风险裁剪。只有 stimulus 命中而无正确性检查的场景，不能标记为验证关闭。

## SVA 精确语义

确认 `|->` 从当前采样拍开始，`|=>` 从下一拍开始；每条属性用 3–5 拍手算真/假波形检验 off-by-one。`disable iff` 的异步取消与采样 reset 条件不同，需要匹配 reset 语义。

stall 保持属性需规定 reset/flush 例外，检查整组 payload；`$past` 用 history-valid 防首拍无定义。断言前件的 cover 能揭示永不触发的 vacuity；cover 命中不等于断言已证明。bounded proof 只说明已探索边界，不能写成无界证明。

formal assume 仅表达真实环境契约；约束 DUT 输出或内部结果可能把 bug 假设掉。检查是否能从 reset 到达有效事务、满/空和响应状态；fairness 和最终响应的假设单独列出。
