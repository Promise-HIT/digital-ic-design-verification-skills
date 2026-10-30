# 验证工具与证据

先使用项目现有 simulator、UVM 版本、编译脚本和 test runner。不得假设 VCS、Xcelium、Questa、Verilator、Icarus 或 formal 工具的选项可互换。开源工具对完整 SystemVerilog class/UVM/SVA 的支持范围有限，调用前读取项目和工具版本说明。

最小执行序列通常是：编译/展开 → 单 test 固定 seed → 相关 testlist → 覆盖收集/合并。失败后停止盲目扩大回归，先做重现和分类。

证据表至少包括：需求 ID、test/property、checker、配置、seed、工具/版本、命令、结果、日志、coverage link、限制。对“pass with warnings”逐条判断 warning 是否影响结论。

工具未安装、许可证不可用、运行超时或环境不完整都属于“未得到证据”，不是 DUT 或 test 通过。
