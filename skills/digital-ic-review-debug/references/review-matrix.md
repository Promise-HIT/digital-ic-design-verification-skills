# 评审矩阵

| 类别 | 高价值问题 | 所需证据 |
| --- | --- | --- |
| 契约 | 延迟/吞吐/顺序/错误/reset 与规格不符 | 需求段落、调用点、波形或反例 |
| 状态 | enable/优先级遗漏、越界、非法状态、死锁 | 状态转移与触发序列 |
| 握手 | stall 下变化、丢失/重复、组合死环 | 周期序列、SVA 或最小测试 |
| 宽度 | 截断、符号扩展、移位、unsized literal | 表达式宽度推导、lint/仿真 |
| 组合 | latch、环、多驱动、不完整 case | 赋值路径、展开/lint 报告 |
| 时序 | blocking/NBA 竞态、跨块顺序依赖 | IEEE 调度语义、最小复现 |
| reset | 极性/值错误、异步释放、域间顺序 | reset tree、RDC/波形 |
| CDC | 单 bit 误用、多 bit 不相干、脉冲丢失 | crossing 结构、源/目的频率、CDC |
| FIFO | full/empty、回绕、同时读写、非 2 次幂 | 指针/计数不变量、边界测试 |
| TB | driver/monitor race、oracle 复制 DUT、结束过早 | time-slot、checker 路径、失败测试 |
| SVA | 错误 clock/reset、蕴含符号、vacuity | property 语义、cover/反例 |
| coverage | 无 checker 的命中、cross 爆炸、错误 waiver | requirement mapping、coverage DB |
| STA/DFT | generated clock/false path/test mode 缺失 | 约束、报告、结构说明 |

审查时优先追踪“输入如何成为错误输出或遗漏检查”的完整链条。无法解释影响的风格问题不应挤占 findings。
