# 使用示例

以下工具命令在本仓库根目录运行；安装后改为相应 Skill 的实际路径。示例中的工程、日志与输出目录需要替换成自己的路径。

## RTL 实现任务

```text
使用 $digital-ic-rtl-design 实现同步 FIFO。
工程路径：<project>；规格：<spec>；构建入口：<existing-command>。
数据宽度 32，深度需支持 1、2、3、16；保持现有 ready/valid 和 reset 约定。
先从规格确认满时同时入出、空时旁路和 flush 语义。
实现后运行工程已有的最小检查，报告命令、配置、结果及未验证项。
```

工程入口不清楚时，先只读盘点：

```bash
python skills/digital-ic-rtl-design/scripts/scan_hdl_project.py /path/to/project --json
```

这只是词法扫描，注释中的词也可能成为候选，不会推导真实时钟域或确认 top。

## 验证计划与关闭检查

```text
使用 $digital-ic-verification，为附带规格建立需求可追踪的验证计划。
沿用现有仿真器和 UVM 版本，先设计独立 checker，再定义激励与覆盖。
重点覆盖连续传输、背压、reset、flush、同时入出和合法参数边界。
将规格未定义的关键行为列为待确认项，不从 RTL 单方面补成规格。
```

检查仓库提供的计划样例：

```bash
python skills/digital-ic-verification/scripts/check_verification_plan.py skills/digital-ic-verification/assets/verification-plan-template.csv --json
```

正式 closure 需要自己的非空证据文件和完整字段：

```bash
python skills/digital-ic-verification/scripts/check_verification_plan.py /path/to/plan.csv --closure --json
```

`evidence` 相对 CSV 所在目录解析。`covered` 需要 evidence、configuration、tool_version、result、checker_selftest、coverage_hit；后两类通过值须满足脚本要求。`waived` 需要 waiver_rationale、waiver_scope、waiver_approval。模板只提供表头，不能直接视为关闭证据。

## 评审与日志分诊

```text
使用 $digital-ic-review-debug，审查这次 FIFO 修改及附带失败日志。
重点检查深度 1、满时同时入出、reset 后首拍和 scoreboard 采样。
本次只做评审：按严重度输出有证据的问题、位置、触发条件和最小修复方向。
```

```bash
python skills/digital-ic-review-debug/scripts/summarize_diagnostics.py /path/to/simulation.log --json --max-samples 3
```

分类可重叠，关键字可能误报。应检查首条因果诊断和原始上下文。

## 保存真实项目检查证据

在自己的工程准备 `checks.json`，命令来自已确认的项目入口：

```json
{
  "checks": [
    {
      "name": "smoke",
      "argv": ["make", "smoke"],
      "timeout_seconds": 120,
      "required": true
    }
  ]
}
```

```bash
python skills/digital-ic-rtl-design/scripts/run_hdl_checks.py /path/to/checks.json --repo /path/to/project --out /path/to/new-run
```

`make smoke` 仅作结构示例，不能假设工程支持。Windows 需要选择真实可用的可执行文件；脚本使用参数数组而不自动解释 shell 表达式。输出目录必须尚不存在，必需检查失败后后续项标记 `not_run`。

runner 保存进程结果，不能判断所有 UVM/断言/coverage 条件。形成工程结论前仍需核实检查器有效性、比较次数、工具版本、日志及配置。
