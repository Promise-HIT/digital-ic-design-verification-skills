---
name: digital-ic-verification
description: 数字 IC 验证规划与实现：建立需求可追踪 testplan、SystemVerilog/UVM testbench、SVA、约束随机、scoreboard、功能覆盖率和回归闭环。用于验证方案、环境开发或 coverage closure；不从 RTL 单方面猜测未定义规格。
---

# Agent 编写自检查验证代码

**先写判据**。把一个需求写成“在哪个边沿采什么、什么条件下计入、哪一次比较能推翻它”。给 driver、monitor 和 scoreboard 各指定输入。monitor 从实际引脚重建成交事务，scoreboard 从输入事务和外部规格维护期望状态。若预测器用 DUT 的 full 或内部指针决定队列能否出入，它会跟着错误状态一起停住。

| 容易漏错的位置 | 写法与验收 |
| --- | --- |
| driver 与监视器同沿运行 | 在 interface 约定 clocking block 的驱动和采样偏移。单时钟简易 bench 也可在另一边沿驱动。区分沿前接受的请求和 NBA 更新后才有效的数据，用不同的采样位置匹配规定延迟。 |
| 数据在 UVM 组件之间传递 | driver 的 item 完成点按协议定义。monitor 每次发布新对象，或生成包含可变子对象的独立快照。analysis port 传递句柄，复用同一对象会改变队列里先前的记录。用地址相同、数据相异的连续事务验证这一点。 |
| 四态值与 byte enable | 在有效拍先检查握手、索引和有效数据位是否含未知值。保留四态值到检查点，避免提前转成 bit。先按规格选中有效 lane，再对选中位作四态比较。两个相同的 X 经 case equality 可以判相等，需要显式检查已知性。 |
| 随机与覆盖 | 检查 randomize() 的返回值。覆盖在 monitor 的实际事件上采样，将 stall 长度或 FIFO 的边沿前占用量作为属性。区分“没有打到场景”“前件未触发”和“场景触发但数据未比较”。保存 seed、参数和工具版本。 |
| 测试结束 | 停止产生新请求，继续 drain，按协议核对已接受、完成、取消与遗留的事务。对要求有流量的 smoke 检查比较数大于零。watchdog 报告最老 outstanding 的标识与最后进展拍；有界延迟只有在响应方提供相应保证时才是接口要求。 |

**从课程 FIFO 建立独立模型**。以“空无直通、满时拒写”为例，用边沿前软件队列长度分别决定能否读、写。同拍双请求且仅读被接受时只取旧队首。注册读口按约定延迟比较该旧值。覆盖深度 1、3、正常深度的空/满双请求，并测试绕回后地址重用。若规格允许满时替换，模型在满且双接受时先取旧队首，再附加新值。

**一个可判定的自检**。先写入两个不同字，再施加背压后放行。正例要看到两次有序比较、队列清空。仅在 checker 输入侧把第二个有效字翻转一位，保持握手、seed 和其他配置，负例应在第二次比较报告期望、实测和事务标识。移除注错后复跑。APB 等有写副作用的接口还应核对提交次数，重复写同一个普通 RAM 值可能让最终内容比较仍然通过。

依据包括 IEEE 1800-2023 第 4、14、16、18、19 章，《SystemVerilog验证：测试平台编写指南》第三版第 1 章，以及课程 APB 和同步 FIFO 的激励代码。

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

对上述保序接口，可用如下 SV 方法处理**已经采样**的同一拍事件。本例假设没有空队列直通，复位分支由调用者处理，DATA_W 为测试配置。调用前先确认有效握手为已知值，再转为 bit；检查有效数据位已知，并从独立参考模型得到预测数据。

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
