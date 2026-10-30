# 签核检查清单

## RTL

- 接口与参数配置有明确契约；边界配置实际展开。
- 编译、lint、综合无未解释高严重度问题；warning waiver 可追踪。
- reset/clock/CDC/RDC 结构与约束一致；所有 crossing 已分类。
- STA 的 clocks、I/O delay、exceptions、generated clocks 有审查；无意外 unconstrained path。
- DFT/test/低功耗控制在功能与测试模式下均有定义。

## 验证

- requirement 到 test/checker/coverage 可追踪；negative 和 reset 场景不缺失。
- scoreboard 无 outstanding；assertion 无被静默禁用；checker 有自测或已注入错误验证。
- 回归配置、seed、工具版本和日志可复现；flaky tests 不计作通过。
- functional/code/assertion coverage 联合审查；排除与 waiver 有依据。
- 未关闭 bug、风险和工具限制在结论中可见。

## 结论措辞

只对实际运行的配置和范围下结论。例如“在 commit X、配置 Y、工具 Z 上，相关 smoke 通过；未运行 CDC/STA”，而不是笼统的“设计已验证”。
