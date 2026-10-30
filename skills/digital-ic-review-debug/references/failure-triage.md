# 失败分诊

## 先确认层级

1. 语法/预处理：宏、include、语言模式、编译顺序。
2. 展开/连接：参数、top、端口、package/library、multiple drivers。
3. 时间 0/reset：X、初始化、reset sequence、clock 未运行。
4. 首个协议/断言失败：抓失败前后最短波形窗口。
5. scoreboard mismatch：核对 transaction 边界、顺序、延迟、flush 和参考模型输入。
6. timeout：找更早的请求、响应、objection 或死锁，不把 timeout 当根因。
7. coverage/形式：检查不可达、约束过强、vacuity、黑盒和深度。

## 假设模板

`在 <配置/序列> 下，由于 <具体机制>，<信号/状态> 在 <时间> 违反 <契约>；若假设正确，观察 <最小信号/断言> 将出现 <可判定结果>。`

每次实验只改变一个因素。修复后先跑原失败，再跑邻近边界和最小回归。若改变 seed、timeout 或关闭 checker 才“通过”，问题通常尚未关闭。

## 常见伪修复

- 增大 timeout 掩盖死锁；
- 添加初始化掩盖 reset/X；
- 扩大 `disable iff` 屏蔽真实断言；
- 放松 scoreboard 比较掩盖顺序/数据错误；
- 给 CDC 信号加单个寄存器但未建立完整协议；
- 全局关闭 lint warning；
- 仅更换 seed。
