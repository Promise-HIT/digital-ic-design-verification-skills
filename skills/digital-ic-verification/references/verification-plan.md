# 验证计划

## 从需求而非 RTL 出发

每个 feature 建立唯一 `REQ/DV` ID，并映射到 stimulus、独立 checker、coverage 与完成证据。RTL 可帮助发现可观察点，但不能替代规格成为唯一 oracle。

计划至少覆盖：基本功能、协议合法序列、边界、非法/错误、reset、背压/并发、资源耗尽、恢复、配置组合、CDC 相关时序和性能要求。对不可直接仿真的要求说明 lint、formal、CDC、STA 或 review 证据。

## 测试空间

| 类型 | 目的 | 示例 |
| --- | --- | --- |
| smoke | 快速验证环境和主路径 | 单 transaction、基本 reset |
| directed | 锁定语义与 bug 回归 | 满后 push、stall 时 payload 稳定 |
| constrained-random | 探索交互与顺序 | burst、backpressure、并发错误 |
| negative | 验证拒绝/报错/恢复 | 非法 opcode、underflow |
| stress | 长时间与资源边界 | 最大 outstanding、连续流 |
| formal/static | 穷举局部状态或结构风险 | FIFO 不越界、CDC 结构 |

## 完成标准

计划项只有在 checker 已实现、测试可复现、目标覆盖命中且失败为零时才能标记 covered。代码覆盖缺口逐项归因：不可达、未刺激、未观察、死代码或工具限制。waiver 写明需求依据、风险、证据、适用配置与复审条件。
