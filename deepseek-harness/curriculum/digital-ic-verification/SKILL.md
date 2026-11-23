---
name: digital-ic-verification
description: 依据 SystemVerilog 验证和 UVM 教材制定 testplan，编写 driver、monitor、scoreboard、SVA 和覆盖驱动测试。
---

# 把接口要求写成能判断对错的测试

## 定计划

《SystemVerilog 验证：测试平台编写指南》第三版正文第 11–12 页（PDF 第 29–30 页）把覆盖反馈和测试平台分层联系起来。将每条需求写成“初始状态、施加的事务、实际采样点、预期响应、失败条件、覆盖目标”。先构造一个可重复的定向序列，再放宽时序和数据随机化。覆盖停滞时区分场景未激发、monitor 未采到以及约束排除了该状态，按原因更改激励或采样点。

以下是把方法用于带背压接口的示例。假设规格要求 valid 等待 ready 时保持 payload，复位取消未完成事务。

| 需求 | 施加场景 | 判定与覆盖 |
| --- | --- | --- |
| 等待期间保持数据 | ready 拉低两拍后恢复 | 逐拍比较 valid 和 payload；记录经历 stall 后的实际握手 |
| 数据保序 | 连续发送 A、B，仅在 A 后施加背压 | 输出依次匹配独立队列中的 A、B；分别记录输入、输出接受数 |
| 复位取消 | A 等待输出时复位，恢复后发送 B | 模型在复位点清空，检查恢复后的第一个输出是 B |

## 写 bench

《UVM 实战》PDF 第 65、76、94–100 页。transaction 保存协议字段；driver 消费请求并在引脚上生成时序，输入与输出 monitor 各自根据接口采样结果重建事务。输入 monitor 的输出送参考模型，输出 monitor 的输出与参考模型预测值在 scoreboard 汇合。用 analysis port 发布，每个事务分配独立对象，避免下一个采样覆写上一次的内容。需要跨进程缓冲时在 env 中连接对应事务类型的 analysis FIFO。项目所用 UVM 库决定实际类型和 API 签名。

对上述保序接口，可用如下 SV 方法处理**已经采样**的同一拍事件。本例假设没有空队列直通，复位分支由调用者处理，DATA_W 为测试配置。调用前先从独立参考模型得到预测数据。

```systemverilog
typedef logic [DATA_W-1:0] word_t;
word_t expected[$];
int unsigned comparisons;

function void check_cycle(bit push, word_t predicted, bit pop, word_t observed);
    word_t oldest;
    if (pop) begin
        if (expected.size() == 0)
            $fatal(1, "Unexpected output");
        oldest = expected.pop_front();
        if (observed !== oldest)
            $fatal(1, "Expected %h, got %h", oldest, observed);
        comparisons++;
    end
    if (push)
        expected.push_back(predicted);
endfunction
```

## 验证 checker

《数字 IC 工作学习资料整理》PDF 第 82–83 页讨论 SVA 的采样及重叠、非重叠蕴含。结合上述保持契约，可写出下式，具体复位屏蔽与项目契约一致：

```systemverilog
assert property (@(posedge clk) disable iff (!rst_n)
    valid && !ready |=> valid && $stable(payload));
```

手填一个 stall 周期和下一采样周期的真值，分别检查保持、错误变化和复位。为 scoreboard 准备正确和错误两个输入，要求正确样例比较次数大于零，故意翻转一位的样例报告首个差异。将覆盖命中、比较结果和残余未测场景回填计划。
