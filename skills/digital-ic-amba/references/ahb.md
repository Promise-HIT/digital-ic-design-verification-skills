# AHB-Lite 的地址相位和数据相位

以单 manager 的 AHB-Lite 接口为例。Arm IHI 0033C 的 Transfers 和 Transfer responses 章节给出相位、等待和错误响应。先核对工程的 HREADY 输入、各从设备 HREADYOUT 和互连返回路径。完整 AHB 的多主仲裁需要对应的集成契约。

1. 在 HCLK 上升沿，HREADY 为高时接受当前有效地址相位；对本从设备，有效条件包括 HSEL 和 HTRANS 为 NONSEQ/SEQ（HTRANS[1]）。保存 HADDR、HWRITE、HSIZE 和本笔所需属性。
2. 下一数据相位使用已保存的控制。写数据 HWDATA 属于该数据相位；读数据和响应由该相位的从设备提供。总线同拍可出现另一笔地址，互连返回 mux 应跟踪数据相位所属从设备。
3. 数据相位被等待时保留其所有者和事务记录。区分等待中地址控制的保持要求与规范允许的 IDLE、BUSY 或错误后的地址变化。对 ERROR 按两周期响应检查：首周期 HRESP=ERROR 且 HREADYOUT=0，次周期 HRESP=ERROR 且 HREADYOUT=1。下一笔是否取消按 manager 的允许行为判定。
4. 用“写 A 后紧接读 B”暴露地址相位错配，再让 A 等两拍，观察 B 只被接受一次。注入 ERROR，验证监视器不会在第一拍就结算。窄传输由 HSIZE、地址低位、总线宽度和项目端序确定有效 lane。

交付波形逐拍标注地址相位的候选事务与数据相位的完成事务。给出 wait、背靠背、错误三种 trace 的事务计数。
