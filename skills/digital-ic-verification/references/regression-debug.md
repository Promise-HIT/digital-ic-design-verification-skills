# 回归、复现与 Closure

## 分层回归

- pre-submit：编译、lint、smoke、变更相关 directed tests，分钟级。
- nightly：更多 seeds、配置、断言与覆盖收集。
- milestone：完整矩阵、长 stress、formal/CDC/coverage merge 与 waiver 审查。

每个 testlist 项记录 test、top/config、seed 策略、超时、tags、owner 和预期资源。先运行最小相关集；长回归会消耗许可证或计算资源时遵循项目审批。

## 可复现失败

保存 commit、工具版本、精确命令、seed、参数/plusargs、环境变量白名单、首个错误时间、wave 起止窗口和日志路径。先用同 seed 重现，再减小测试；不要一开始改多个变量。

失败分组优先使用稳定 signature：assertion 名称、UVM report ID、首个 mismatch 类型、编译错误位置。相同后续超时不应掩盖更早根因。

## Closure

关闭前确认：所有计划项有证据；失败为零或有批准 waiver；coverage exclusions 有依据；checker 自测完成；随机稳定性达到项目定义；已知 bug 与风险可追踪；重跑结果可复现。报告分母、配置和合并范围，不只给百分比。
