# 从未命中场景到可执行的测试

《SystemVerilog 验证：测试平台编写指南》第三版正文第 11–12 页（PDF 第 29–30 页）讨论了覆盖反馈与分层测试平台。在下面的 FIFO 练习中，generator 选择“填满后同时读写”这个场景，driver 负责输入引脚时序，monitor 在采样沿独立生成实际接受的事务。将激励、观察和判定分开，背压导致 driver 请求未被接受时，参考队列应保持原值。

先问三个问题：事务可以发生吗？monitor 能看见吗？若结果错了，checker 会失败吗？把三者绑定到同一条需求，再选择定向或约束随机激励。

以同步 FIFO 的满时同时入出为例。规格若允许满时用一次出队腾出空间，先用唯一递增数据填满，再在同一拍提出读写。monitor 分别以真实的输入、输出握手判定 push 和 pop。scoreboard 保存该拍之前的队首，在 pop 时与实际输出对比，再记录已接受的输入。这个次序适用于本例的旧队首输出契约；空时旁路需独立建模。

```systemverilog
// 在 monitor 已经采样引脚并建立同一拍的快照后执行
if (pop) begin
    if (expected.size() == 0)
        $fatal(1, "Unexpected output");
    oldest = expected.pop_front();
    if (out_data !== oldest)
        $fatal(1, "FIFO order mismatch");
end
if (push)
    expected.push_back(in_data);
```

TB 中用与 payload 等宽的四态类型声明 oldest 和队列元素。覆盖点采样握手之前模型的满状态以及本拍 push/pop。将输出的一个有效位翻转一次，确认 checker 报错；撤销注错，复跑相同 seed。结束时清空队列并核对比较次数。

若覆盖长期停在满时入出这个 bin，先复核采样点和分母，再用定向序列填满 FIFO 并对齐请求。若规格规定满时必须拒收，在同样激励下检查拒绝行为，并记录原覆盖目标为何不可达。此流程参考《SystemVerilog 验证：测试平台编写指南》第三版第 1 章关于覆盖反馈的讨论。
