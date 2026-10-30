---
name: digital-ic-verification
description: 数字 IC 验证规划与实现：建立需求可追踪 testplan、SystemVerilog/UVM testbench、SVA、约束随机、scoreboard、功能覆盖率和回归闭环。用于验证方案、环境开发或 coverage closure；不从 RTL 单方面猜测未定义规格。
---

# 数字 IC 验证

交付能独立判断 DUT 是否符合规格、可复现且可追踪到需求的验证证据。

整体任务需要衔接设计、验证和实现阶段时，读取配套 RTL skill 的 [开发流程](../digital-ic-rtl-design/references/development-flow.md)；工具流程问题读取 [EDA 使用与脚本开发](../digital-ic-rtl-design/references/eda-workflow.md)。小任务只取相关阶段。

## 权限与判断

- 规划、解释或审查请求：读取材料并产出结论，不修改验证环境。
- 创建、实现或修复请求：完成范围内本地编辑与相关非破坏性测试。
- 在用户已授权范围内运行必要验证；额外大规模计算或许可证成本先核对授权，不为常规本地回归重复询问。
- 只询问会改变 checker 的关键语义；其他不确定性以显式假设记录。

## 执行流程

1. 读取规格、RTL 接口、已有 testplan/bench、filelist、CI/回归入口和工具版本。把需求、实现观察、环境事实和推断分开。
2. 将需求拆成唯一 ID，并映射到 stimulus、独立 checker、coverage、验证层级、优先级和完成条件。
3. 先设计观察与判定，再选择最轻的环境：简单 block 用 self-checking bench；需要复用、多 agent 或复杂并发时再使用 class/UVM。
4. 覆盖 smoke、合法等价类、边界、negative/error、reset、背压/并发、stress 和参数组合。
5. 分配检查职责：局部时序与不变量用 SVA；端到端 transaction 用 monitor + scoreboard/reference model；长窗口统计用离线分析。
6. 先固定 seed 跑最小测试，再跑相关 suite。记录工具版本、精确命令、配置、seed、退出码与日志；失败先归并并定位首因。
7. 将功能覆盖率绑定到需求和风险，代码覆盖率用于发现盲区；逐项处理 exclusion、不可达项和 waiver。

已有 CSV 计划时可直接执行 `python3 scripts/check_verification_plan.py <plan.csv>`；无需先读取脚本源码。

## 验证不变量

- driver 与 monitor 使用正确的驱动/采样区域，避免 DUT/TB race。
- monitor 只重建实际 transaction；reference model 不照抄 DUT 算法；scoreboard 明确顺序、超时、reset/flush 和 outstanding。
- SVA 明确 clock、reset、采样值与有界/无界语义；constraint 可解，`randomize()` 失败即测试失败。
- coverage cross 只表达有价值交互；illegal/ignore bins 和 waiver 均有规格依据。
- 不以固定延迟代替协议同步，不以日志字符串、单一 seed、零 assertion failure 或单项 100% coverage 宣告完成。

## 按需读取

- 创建 testplan 或确定完成标准：[references/verification-plan.md](references/verification-plan.md)
- 搭建 procedural/UVM 环境或解决竞态：[references/testbench-architecture.md](references/testbench-architecture.md)
- 编写 SVA、形式属性或 coverage model：[references/assertions-formal-coverage.md](references/assertions-formal-coverage.md)
- 处理随机失败、回归或 closure：[references/regression-debug.md](references/regression-debug.md)
- 选择仿真/形式工具或记录证据：[references/tool-and-evidence.md](references/tool-and-evidence.md)
- 新计划可复制 [assets/verification-plan-template.csv](assets/verification-plan-template.csv)；回归清单可复制 [assets/regression-testlist-template.csv](assets/regression-testlist-template.csv)。

通常只读取当前分支所需资料。

## 实现门禁与深度参考

先固定 simulator、SystemVerilog 语言模式、UVM 精确版本/来源、top、filelist、宏和参数。UVM 内容以 [official-uvm.md](references/official-uvm.md) 中 Accellera 官方指南、API 参考及对应版本参考实现为主要依据；项目用旧库时保留兼容性，不能混用新 API 或自动升级。

- UVM 工程落地、config/factory、TLM、sequence/driver、objection/reset：[uvm-practical.md](references/uvm-practical.md)。
- 调度、独立 oracle、对象生命周期、checker 注错、SVA vacuity：[checker-and-scheduling.md](references/checker-and-scheduling.md)。
- 寄存器模型和多 sequence：[uvm-sequences-ral.md](references/uvm-sequences-ral.md)。
- 书籍核心参考：[local-library.md](references/local-library.md)。官方 UVM 资料优先于本地 1.1d 教材。

自检查 smoke 必须同时证明：test 被创建、激励被接受、monitor 观察到事务、checker 比较非零、正常 drain 且 watchdog 未触发。针对新增 checker 做适度注错确认它能拒绝错误；不能把“没有 error”视为已经检查过。

`scripts/check_verification_plan.py plan.csv --closure` 在关闭验证计划时要求证据文件、配置、工具版本、checker 自检及覆盖命中，或完整 waiver 元数据。它仅校验可追踪性和字段，不验证日志真伪或证明 RTL 正确。

关闭证据字段见 [verification-closure-template.csv](assets/verification-closure-template.csv)，只在需要正式 closure 时使用。

## 完成输出

直接给出：需求追踪与检查架构；新增或修改文件；实际命令/配置/seed/结果；覆盖与 waiver；未关闭问题。无法执行的检查标为验证缺口。
