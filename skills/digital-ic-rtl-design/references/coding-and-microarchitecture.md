# 编码与微架构要点

## 组合与时序

组合块开头设置默认值，分支只覆盖差异。时序块表达“状态在时钟边沿如何更新”，不要把同一 next-state 计算散落在多个块。对优先级使用显式 `if/else`；对并行译码使用项目认可的 `unique case`，同时提供安全 default。

位宽计算应能人工复核。加减、比较、移位前统一 signedness；对会增长的算术明确扩展位。切片、拼接、unsized literal 与参数表达式是高风险点。

## FSM

建议两进程 FSM：时序块只保存 state，组合块计算 next-state 和输出。Moore/Mealy 选择以接口时序和关键路径为准。说明非法状态策略；安全敏感模块不能只依赖仿真中的 X。

Moore 输出由状态决定，Mealy 输出还依赖当前输入；二者的 next-state 都可以依赖状态和输入。不要把旧资料中“Moore 的状态转变只依赖当前状态”的表述直接转成 RTL。两进程只是常用形式，不能为了套模板破坏工程既有且正确的单/三进程实现。

## CRC、编码和位操作

先锁定多项式表示、初始值、input/output reflection、字节/bit 顺序、final XOR、合法 payload 长度及有效 byte lane。串行算法展开为并行 XOR 网络时，应和一个独立、按 bit 迭代的模型对照，不能将“单周期处理多个 bit”误写成多个时钟周期。

检查已知 golden vector、全 0/全 1、单 bit、不同消息长度、非整 beat 尾部、连续包以及 reset/seed reload 与 transfer 同拍。需要匹配外部协议时从协议规定获取这些常量，不直接套书中 CRC-16 的参数。

## FIFO

同步 FIFO 至少检查：深度合法、指针宽度、full/empty 判定、同时 push/pop、underflow/overflow 策略、first-word-fall-through 语义、占用计数范围。非 2 的幂深度不能照搬二进制指针回绕。

异步 FIFO 不是同步 FIFO 加两级寄存器。通常需要 Gray 指针、跨域同步、域内 full/empty 比较及复位后的保守状态；具体公式需与深度和实现约束一致，并交给 CDC/形式工具验证。

## ready/valid 与流水线

一次传输只在 `valid && ready` 发生。发送端在未接受时保持 valid 与 payload；接收端可通过 ready 背压。若打断组合路径，使用 skid/elastic buffer，并验证连续流、单周期 stall、长期 stall、同时入出和 reset/flush。

流水线寄存 data 时必须同步寄存 valid、tag、错误和 sideband。任何 bypass 或 replay 都要保持 transaction 身份与顺序。

## 仲裁

明确 fixed-priority、round-robin 或其他策略及公平性目标。检查同周期请求、grant onehot/onehot0、被接受前请求保持约定、锁定事务、空闲恢复和指针更新条件。不要把“轮转”误当成已证明无饥饿。

## 参数化

参数只暴露有真实需求的维度；给出合法范围和组合。特别测试宽度 1、深度 1/2、最大计数、非 2 的幂，以及 feature disabled。生成块命名稳定，避免层级路径随工具变化。
