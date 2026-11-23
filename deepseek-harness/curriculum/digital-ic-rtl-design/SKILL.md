---
name: digital-ic-rtl-design
description: 根据教材中的 RTL 编码与状态机方法编写 Verilog/SystemVerilog，适用于设计实现、代码风格和综合前检查。
---

# 先画出电路，再写 HDL

以下页码为随附 PDF 的物理页。先读用户规格，写明时钟、复位、输入何时采样、输出在哪一拍有效。将规格中仍未定义的行为列为设计问题。下列练习里的时序只适用于练习本身。

## 写模块与命名

依据《数字 IC 工作学习资料整理》PDF 第 33–45 页。先看相邻模块怎样命名时钟、复位和低有效信号。新模块沿用同一套约定，文件名对应模块名，跨层级的同一信号保持可辨认。常数和参数用有意义的名称。端口逐行声明，明确方向和范围；每条语句单独一行，复杂表达式用括号表达运算次序。注释写清端口行为、编译条件和综合例外。整理已有代码时按改动范围执行。

## 从状态表生成组合和时序逻辑

依据《Verilog HDL 电路设计指导书》PDF 第 16 页关于输出时序和分支互斥的讨论，以及《数字 IC 工作学习资料整理》编码风格章。为每个当前状态列出输入条件、次态、输出和优先级。Moore 输出按当前状态译码；Mealy 输出同时依赖输入。两类状态机均须按输入条件决定次态。对可能重叠的条件先决定优先级，再选 if/else 或 case。组合分支覆盖每条输出路径，时钟沿更新状态。

下面是本插件推导的一个完整示例。同步低有效复位；采样到 req 后下一周期显示 busy，一旦采样到 done 就结束。用 Verilog-2001 编写：

```verilog
module busy_ctrl (
    input  wire clk,
    input  wire rst_n,
    input  wire req,
    input  wire done,
    output wire busy
);
    localparam IDLE = 1'b0, ACTIVE = 1'b1;
    reg state_q, state_d;

    always @* begin
        state_d = state_q;
        case (state_q)
            IDLE:    if (req)  state_d = ACTIVE;
            ACTIVE:  if (done) state_d = IDLE;
            default: state_d = IDLE;
        endcase
    end

    always @(posedge clk) begin
        if (!rst_n)
            state_q <= IDLE;
        else
            state_q <= state_d;
    end

    assign busy = (state_q == ACTIVE);
endmodule
```

将此模块用于 SV 工程时，按同一状态表把组合块写作 always_comb、寄存块写作 always_ff，状态可用显式位宽 enum logic。核对两版在复位、IDLE 收 req、ACTIVE 收 done 时的逐拍序列。端口与中间表达式的位宽、符号和截断位置可逐项对照第 45 页的操作数位宽要求；例如 W 位无符号数求和需要保留进位时，将两个输入各补一个前导零，结果接 W+1 位。

**交付**包括接口时序、代码、一个能区分两种实现的输入序列及观察结果。对于上例，在时钟沿之间切换 req，观察 busy 是否仅随状态更新；同时置位 req/done，分别核对当前状态为 IDLE 和 ACTIVE 的结果。
