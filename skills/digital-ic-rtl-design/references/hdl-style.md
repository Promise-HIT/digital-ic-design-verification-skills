# Verilog / SystemVerilog 交付风格

**FSM 练习**取自《Verilog HDL 电路设计指导书》PDF 第 16 页讨论的输出时序和分支覆盖问题。设计 req/ack 控制器时，先为每个状态写出「条件、下一状态、输出、采样边沿」四列。两个条件可以同时为真时，显式给出优先级。若 ack 由当前状态和 req 组合生成，检查 req 到 ack 的组合路径；若 ack 只由状态译码，核对接受请求到应答的拍数。Moore、Mealy 按输出与输入的关系区分，两种结构的下一状态都可以取决于输入。用一个 req 在两次采样沿之间翻转的波形检查输出契约。

先检查 filelist、语言开关和相邻模块。要求 Verilog-2001 的 .v 文件使用 wire/reg、always @* 和显式端口连接。SystemVerilog 工程沿用 logic、always_comb、always_ff、typedef enum 和项目已有的 package。修改现有模块时保持端口、复位极性、时序语义和命名惯例。新模块缺少约定时，可用小写下划线命名信号，低有效端口加 _n，组合下一值和寄存值分别加 _d、_q。

下面两个片段实现相同的单拍 valid 寄存器。例子采用同步低有效复位、同步 flush，flush 优先于 enable。复位是否异步由目标项目决定。

```verilog
// Verilog-2001, valid_q declared as reg
always @(posedge clk) begin
    if (!rst_n || flush)
        valid_q <= 1'b0;
    else if (enable)
        valid_q <= valid_i;
end
```

```systemverilog
// SystemVerilog, valid_q declared as logic
always_ff @(posedge clk) begin
    if (!rst_n || flush)
        valid_q <= 1'b0;
    else if (enable)
        valid_q <= valid_i;
end
```

每个寄存器只由一个时序块更新。组合块用阻塞赋值并覆盖所有路径。算术先列出输入、中间量和输出的范围，再决定扩展、舍入和截断位置。深度 1 检查索引位宽，深度 3 检查显式回绕。控制状态和 valid 的复位语义明确后，再决定 payload 是否需要复位。注释说明同拍冲突的优先级和接口约束。

交付时给出工程实际使用的语言模式与检查命令。对含 backpressure 的接口，用连续有效、stall 后释放和满时同时入出三个短序列，核对每个接受事件对应的数据及 sideband。
