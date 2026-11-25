# APB 寄存器和外设

Arm IHI 0024E 第 3 章给出传输和错误响应，第 4 章给出运行状态。先区分 APB2、引入 PREADY/PSLVERR 的 APB3，以及支持 PSTRB/PPROT 的 APB4。项目可省略部分可选信号。下例假设单个选定外设、有 PREADY 的接口。

| PCLK 上升沿采样 | 含义 | 实现与验证 |
| --- | --- | --- |
| PSELx=1，PENABLE=0 | SETUP | 捕获地址、方向、选通及写数据，为下一拍 ACCESS 作准备。 |
| PSELx=1，PENABLE=1，PREADY=0 | ACCESS 等待 | 保持选择、使能及该传输的请求字段。monitor 累加等待周期。 |
| PSELx=1，PENABLE=1，PREADY=1 | ACCESS 完成 | monitor 记一笔；读时采 PRDATA，有 PSLVERR 时在此拍取样。同一外设的下一笔可保持选中，但必须经过 PENABLE=0 的 SETUP。 |

写寄存器时若项目规定“成功写在完成沿生效”，用完成事件、PWRITE 与成功响应共同限定副作用。APB 本身允许出错的访问改变外设状态，错误读数据也可能无效。predictor 应从寄存器规格取得出错时的状态语义。PSTRB 按字节选择写通道，带 PSTRB 的接口读时所有 strobe 为零。多外设共享 PENABLE，某个未选中外设也可能见到 PENABLE=1，局部断言应带本外设的 PSELx。

以下 SVA 片段用于 APB4 的基本写请求信号，PRESETn 低电平取消检查；若工程有附加属性，把需保持的字段按版次加入。属性在最后一个等待拍仍要求下一采样拍保持请求，因此能检查释放等待的边界。

```systemverilog
assert property (@(posedge PCLK) disable iff (!PRESETn)
  PSELx && PENABLE && !PREADY && PWRITE
  |=> PSELx && PENABLE && PWRITE && $stable({PADDR, PWDATA, PSTRB}));
cover property (@(posedge PCLK) disable iff (!PRESETn)
  (PSELx && PENABLE && !PREADY && PWRITE) ##1
  (PSELx && PENABLE && PREADY && PWRITE));
```

最小序列：SETUP 写 A，ACCESS 等待两拍，第三个 ACCESS 完成，紧接 SETUP 读 B。测试等待为 0、1、多拍，检查完成数、读数据及规定的写脉冲数。只在末个等待拍到完成拍之间改变 PWDATA，保持其余信号相同，保持断言应失败。课程两套 APB 工程分别提供有等待、无等待的激励思路。
