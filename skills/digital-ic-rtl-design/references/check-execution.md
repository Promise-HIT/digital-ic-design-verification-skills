# 运行检查与证据落盘

先沿用项目工具。需要统一保存多条命令时，创建 JSON：

```json
{"checks":[{"name":"smoke","argv":["make","smoke"],"timeout_seconds":120,"required":true}]}
```

```text
python scripts/run_hdl_checks.py checks.json --repo <repo> --out <new-run-directory>
```

`argv` 必须来自已核对的项目入口；不接受 shell 拼接，不从书中直接执行命令。Windows 的 `.cmd/.bat` 或 shell builtin 需要按环境显式选择解释器并正确引用；不能把 Bash/PowerShell 语法混用。若 Python 只是 WindowsApps 别名，先用真正解释器的完整路径运行。

每次输出目录必须是新目录，日志合并 stdout/stderr，保存 argv/cwd/退出码/耗时和状态；必需检查失败后停止。timeout/unavailable 都是未验证。runner 的 pass 仅表示进程退出码 0；仍须审查 UVM_ERROR、断言、比较次数、覆盖与工具版本，再形成设计结论。

不会自动推导 top、filelist、库、seed 或工具命令，也不会证明 checker 正确。不要用这个包装器取代成熟回归系统。
