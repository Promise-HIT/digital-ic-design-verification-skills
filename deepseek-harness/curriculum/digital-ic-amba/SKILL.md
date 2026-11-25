---
name: digital-ic-amba
description: 为 AMBA APB、AHB-Lite 和 AXI 接口编写或评审协议 RTL、桥、接口监视器与断言。适用于等待周期、分通道握手、突发、字节写使能、响应与顺序问题。
---

# AMBA 接口设计与验证

先从端口、IP 配置与集成规范确认协议版次、角色、时钟域、数据宽度、可选信号和支持的事务子集。写出接受地址、接受数据、完成响应和产生外设副作用的各自条件。在逐拍表里为每个事件分一列，再写状态转移、缓冲容量和 checker。


跨协议桥先画一笔访问在两侧分别何时被接受。为已经接受但下游仍在等待的地址、数据、掩码及响应分配存储。时钟不同时另行设计双向 CDC。验证上游停顿、下游停顿、错误传播及连续不同地址。只有确认下游接受后才推进对应事务；哪些上游请求能提前应答由桥的规格决定。

输出包括实现或评审位置、采用的版次与可选项、覆盖的事务和实际运行的检查。

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

# AHB-Lite 的地址相位和数据相位

以单 manager 的 AHB-Lite 接口为例。Arm IHI 0033C 的 Transfers 和 Transfer responses 章节给出相位、等待和错误响应。先核对工程的 HREADY 输入、各从设备 HREADYOUT 和互连返回路径。完整 AHB 的多主仲裁需要对应的集成契约。

1. 在 HCLK 上升沿，HREADY 为高时接受当前有效地址相位；对本从设备，有效条件包括 HSEL 和 HTRANS 为 NONSEQ/SEQ（HTRANS[1]）。保存 HADDR、HWRITE、HSIZE 和本笔所需属性。
2. 下一数据相位使用已保存的控制。写数据 HWDATA 属于该数据相位；读数据和响应由该相位的从设备提供。总线同拍可出现另一笔地址，互连返回 mux 应跟踪数据相位所属从设备。
3. 数据相位被等待时保留其所有者和事务记录。区分等待中地址控制的保持要求与规范允许的 IDLE、BUSY 或错误后的地址变化。对 ERROR 按两周期响应检查：首周期 HRESP=ERROR 且 HREADYOUT=0，次周期 HRESP=ERROR 且 HREADYOUT=1。下一笔是否取消按 manager 的允许行为判定。
4. 用“写 A 后紧接读 B”暴露地址相位错配，再让 A 等两拍，观察 B 只被接受一次。注入 ERROR，验证监视器不会在第一拍就结算。窄传输由 HSIZE、地址低位、总线宽度和项目端序确定有效 lane。

交付波形逐拍标注地址相位的候选事务与数据相位的完成事务。给出 wait、背靠背、错误三种 trace 的事务计数。

# AXI 的独立通道

课程库的旧版 AMBAaxi 为 Arm IHI 0022B。IHI 0022L 的修订记录说明已移除 AXI3、AXI4、AXI4-Lite 等早期接口的专门内容；AXI4 或 AXI4-Lite 项目应使用覆盖该版的规范，如 IHI 0022H。先核对 full/Lite、ID、burst、最大 outstanding、顺序要求和可选属性。以下讨论常规 VALID/READY 传输。

- **逐通道成交**。在本通道 VALID 与 READY 同时为高的上升沿取样。源端有可发送项时不能等本通道 READY 才拉 VALID。VALID 拉起未握手时保持 VALID 和该通道有效负载。对所有输入到输出的组合路径按接口要求审查，可用寄存切片或有容量的缓冲断开相关路径。
- **写地址与写数据**。AW 与 W 可先后或同时到达。以 AXI4-Lite 单未完成写为例，分别记住已接受地址与数据/strb，配齐后执行一次写并生成一次 B。BVALID 持续到 BREADY。允许等另一通道有 VALID 再给 READY 的从设备，仍需核查握手依赖与系统活性。不要把 AW、W 必须同拍当作源端义务。
- **读与突发**。AR 与 R 各自接受。full AXI 维护事务描述符、剩余拍数及 ID，按该版本支持的 burst 类型计算地址与有效字节。对有 AxLEN 的配置，拍数为 AxLEN+1；末拍核对 RLAST/WLAST。测试靠近 4 KiB 边界的合法末拍，单笔突发不得跨越 4 KiB 边界。Lite 每笔单拍，省去 burst/last 逻辑。
- **独立预测**。按配置和每个 ID 的顺序规则匹配响应，不把不同 ID 的完成顺序硬编码为发出顺序。AXI4 写数据按写地址事务顺序配对；旧 AXI3 的 WID/可选写数据交织不能直接移入 AXI4。对乱序能力、错误状态和 reset 清理分别定义测试。

用四条写序列验证 Lite 从设备：AW 先到、W 先到、同拍到达、B 长时间背压且下一笔尝试进入。记录 AW/W/B 三组接受数，队列 drain 后核对配对、地址、掩码与副作用。读通道另测 R 停顿直到接收沿，保持 RID（如有）、响应和读数据。

AXI4-Lite 子集和可选行为可查 B1.1，包括从设备限制 outstanding 的方式及支持的写掩码策略。[Arm IHI 0022H](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)
