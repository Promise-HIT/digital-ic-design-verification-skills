# 握手、FIFO、仲裁的边界推导

## 先写接受事件

`in_fire = in_valid && in_ready`，`out_fire = out_valid && out_ready`。复位/flush 是否屏蔽接受需由契约给定。状态仅在对应接受事件更新，不能因为出现 request 或 grant 就无条件消耗资源。

|场景|必须判定|
|---|---|
|空 + push/pop 同时请求|是否允许 bypass；同步读 RAM 能否同周期输出|
|满 + push/pop 同时请求|是否允许出队腾位后接受入队；ready 是否形成长组合路径|
|stall|valid 与完整 payload/sideband 保持；释放 stall 后只消费一次|
|reset/flush + transfer|哪一个优先；已接受事务取消、完成还是报错|
|空闲/复位后首拍|输出 valid、地址及状态是否有定义|

## 同步 FIFO

令 `push`/`pop` 为已经接受的事件，`occ_next=occ+push-pop`，并证明 `0<=occ<=DEPTH`。同周期加减要作为一个更新处理，避免两个 NBA 导致后一个覆盖前一个。checker 自己按接受事件维护队列，不复制 DUT 指针公式。

分别写清输出为 FWFT、寄存读还是有旁路；RAM 同地址读写是 old-data/new-data/no-change 中哪种。容量、延迟、吞吐和 full/empty 信号可见延迟均是接口契约。

最小矩阵：深度 1/2/非 2 次幂/典型深度，fill→full→drain→empty，连续环绕，同时入出，单拍/长背压，满/空附近 reset/flush。对非法请求按规格检查拒绝/告警，不默认为合法接受。

## 异步 FIFO

常见 Gray 指针结构要求 2 次幂深度；非 2 次幂实现需要专门证明。二进制指针用于本地地址，Gray 编码为 `g=b^(b>>1)`，只跨域同步 Gray 指针。标准 full 判定的高两位翻转公式依赖指针宽度；极小深度不得照抄产生负切片。

full/empty 使用本域约定的当前/下一指针计算，不能混用。同步延迟导致保守的 flag 延迟，不能承诺同步 FIFO 的即时反映。同步 Gray 编码仍需实现端 max-delay/bus-skew 等适配约束，结构识别与物理限制分别检查。

覆盖双时钟相位/频率变化、一域停钟、一侧复位和重新加入。独立局部复位可能破坏历史数据对应关系；若只支持共同 reset，就明确禁止并验证这一前提，不能私自承诺任意一侧 reset 安全。

## Elastic/skid buffer

单寄存 elastic stage 常用 `in_ready = !out_valid || out_ready`，仅适用于允许该组合 ready 路径、无额外 flush/模式的结构。寄存 ready 时，要为反馈延迟期间已经接受的 beat 预留存储；简单打一拍 ready 可能丢数据。

检查数据守恒：已接受输入数减已接受输出数等于缓冲中的有效事务数（扣除按规格取消的事务）；用唯一序号和 sideband 一起比较，检查连续流吞吐和气泡。

## 仲裁与性能

区分 request、grant 与真正接受。round-robin 更新点通常在获胜事务接受/完成时，必须服从 burst/锁定规格。检查 onehot0、无请求不 grant、stall 期间 winner 稳定、复位初始优先级。

无饥饿证明需要持续请求以及下游进展/最大锁定时间的环境条件。没有公平性前提，不写固定等待上限。性能测试说明有效测量窗口、时钟、输入负载、背压和 warm-up，不把设计峰值当成实测吞吐。
