# 从症状追踪首因

|症状|优先区分|最小证据|
|---|---|---|
|小数值通过，最高位为 1 失败|signed/unsigned、截断、比较扩展|逐级表达式宽度和边界向量|
|深度为 1 或非 2 次幂失败|零宽索引、回绕、同地址读写|实际参数展开、空满同时操作|
|首个包错误|reset 释放、无效数据误采样、模型未清空|reset 到首个 fire 的波形|
|满速正常，背压后丢包|ready 延迟无缓冲、payload 未保持|每拍 fire、occupancy 和唯一序号|
|仅多时钟/特定频比失败|脉冲丢失、CDC 相干性、局部 reset|源/目的事件数、同步级与协议|
|UVM 时间 0 结束|无 objection、test 未创建、phase 不一致|topology、test 名与 phase trace|
|UVM 永不结束|objection 未 drop、sequencer 死锁、队列漏 drain|objection owner、item 握手、outstanding|
|所有 actual 最终都相同|analysis 对象重复使用、浅拷贝|对象身份和发布/缓存时内容|
|同一 seed 偶发失败|DUT/TB race、fork/共享状态、配置漂移|采样区、工具/代码/随机调用链|
|coverage 100% 仍错|无独立 checker、错误采样/分母、字段漏比|注错测试、需求映射、实际有效事务|
|formal 很快全通过|前件不触发、reset 卡住、assume 过强|cover reachability、假设依赖、深度|
|STA 变好但 RTL 未改|新增 false path/clock group、角/模式漂移|约束 diff 和路径集合/分母|

以上是候选机制，不是已确认 findings。每项仍需触发条件、可观察影响、源代码位置和反例；文档命名或旧版规范本身不是严重度依据。
