# SVA、形式验证与覆盖率

## SVA

优先写最小、命名清楚的 property：请求/响应时序、stall 稳定、onehot、队列范围、禁止 underflow/overflow、状态合法、数据保持。明确采样时钟与 reset 屏蔽；需要历史值时用 `$past` 并保护初始周期。

区分假设与断言。环境协议约束可作为 formal assume，但在 simulation 中不能把 DUT 错误假设掉。对最终响应一类活性属性，说明公平性和最大延迟；无界属性是否受工具支持需要确认。

## 形式验证

适合局部但难随机穷尽的状态空间：FIFO 指针、仲裁互斥、计数器范围、协议安全性。先做 bounded proof/cover 检查可达性，再处理 induction。所有通过结论需包含 top、参数、时钟/reset 建模、assumptions、depth/engine 和未证明属性。

## 功能覆盖率

coverpoint 对齐需求等价类和边界；cross 只表达风险交互，如 opcode × error、burst × backpressure。transition bins 用于状态序列；assertion cover 用于关键协议序列。自动 bins 不能替代人工可解释目标。

## 代码覆盖率

statement/branch/toggle/FSM 用于发现未执行结构，但不能证明输出正确。低覆盖可能是 stimulus、配置、不可达逻辑或死代码；高覆盖也可能缺少 checker。功能与代码覆盖率必须联合解读。
