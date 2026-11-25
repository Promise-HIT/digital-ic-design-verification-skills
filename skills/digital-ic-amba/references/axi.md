# AXI 的独立通道

课程库的旧版 AMBAaxi 为 Arm IHI 0022B。IHI 0022L 的修订记录说明已移除 AXI3、AXI4、AXI4-Lite 等早期接口的专门内容；AXI4 或 AXI4-Lite 项目应使用覆盖该版的规范，如 IHI 0022H。先核对 full/Lite、ID、burst、最大 outstanding、顺序要求和可选属性。以下讨论常规 VALID/READY 传输。

- **逐通道成交**。在本通道 VALID 与 READY 同时为高的上升沿取样。源端有可发送项时不能等本通道 READY 才拉 VALID。VALID 拉起未握手时保持 VALID 和该通道有效负载。对所有输入到输出的组合路径按接口要求审查，可用寄存切片或有容量的缓冲断开相关路径。
- **写地址与写数据**。AW 与 W 可先后或同时到达。以 AXI4-Lite 单未完成写为例，分别记住已接受地址与数据/strb，配齐后执行一次写并生成一次 B。BVALID 持续到 BREADY。允许等另一通道有 VALID 再给 READY 的从设备，仍需核查握手依赖与系统活性。不要把 AW、W 必须同拍当作源端义务。
- **读与突发**。AR 与 R 各自接受。full AXI 维护事务描述符、剩余拍数及 ID，按该版本支持的 burst 类型计算地址与有效字节。对有 AxLEN 的配置，拍数为 AxLEN+1；末拍核对 RLAST/WLAST。测试靠近 4 KiB 边界的合法末拍，单笔突发不得跨越 4 KiB 边界。Lite 每笔单拍，省去 burst/last 逻辑。
- **独立预测**。按配置和每个 ID 的顺序规则匹配响应，不把不同 ID 的完成顺序硬编码为发出顺序。AXI4 写数据按写地址事务顺序配对；旧 AXI3 的 WID/可选写数据交织不能直接移入 AXI4。对乱序能力、错误状态和 reset 清理分别定义测试。

用四条写序列验证 Lite 从设备：AW 先到、W 先到、同拍到达、B 长时间背压且下一笔尝试进入。记录 AW/W/B 三组接受数，队列 drain 后核对配对、地址、掩码与副作用。读通道另测 R 停顿直到接收沿，保持 RID（如有）、响应和读数据。

AXI4-Lite 子集和可选行为可查 B1.1，包括从设备限制 outstanding 的方式及支持的写掩码策略。[Arm IHI 0022H](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)
