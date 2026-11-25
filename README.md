# Digital IC Design & Verification Skills

面向数字 IC 设计、验证与实现的五个中文 Agent Skills，涵盖 RTL、AMBA 协议、验证开发、故障定位，以及从仿真到签核的 EDA 工具与脚本。

[English overview](README.en.md) · [使用示例](docs/EXAMPLES.md) · [贡献说明](CONTRIBUTING.md) · [MIT License](LICENSE)

## v1.1.1 安装入口

| 平台 | 安装与调用 |
| --- | --- |
| ChatGPT / Codex | 网页版从发布页选择一个 `chatgpt-digital-ic-*.zip`，在 Plugins → Skills → Create 中上传。Codex 本机使用下方安装器，可用 `$digital-ic-amba` 等名称调用。 |
| Claude / Claude Code | 网页版使用对应的 `claude-digital-ic-*.zip`。Claude Code 可安装到个人或项目的 `.claude/skills`，通过 `/digital-ic-amba` 等名称调用。详见 [Claude 安装说明](claude/README.md)。 |
| DeepSeek Harness（dsh） | 一个原生插件注册全部五个角色，从当前 profile 加载。使用 [dsh 安装说明](deepseek-harness/README.md) 中的 v1.1.1 包。 |

[下载 v1.1.1](https://github.com/Promise-HIT/digital-ic-design-verification-skills/releases/tag/v1.1.1) · [课程资料来源](docs/COURSE-NOTES.md) · [ChatGPT Skills 官方说明](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)

## 五个专业入口

| Skill | 适用任务 | 主要内容 |
| --- | --- | --- |
| [digital-ic-rtl-design](skills/digital-ic-rtl-design/SKILL.md) | 新模块、功能修改、RTL 重构 | 接口契约、微架构、FSM/FIFO/握手、位宽、复位、CDC/RDC、EDA 流程 |
| [digital-ic-verification](skills/digital-ic-verification/SKILL.md) | 验证规划、环境开发、覆盖闭环 | 需求追踪、独立 checker、SystemVerilog/UVM、SVA、RAL、回归与证据 |
| [digital-ic-review-debug](skills/digital-ic-review-debug/SKILL.md) | RTL/TB 评审、日志分诊、失败定位 | 严重度排序、首因假设、最小复现、签核缺口与修复验证 |
| [digital-ic-amba](skills/digital-ic-amba/SKILL.md) | 总线、外设、桥与协议监视器 | APB 等待和副作用、AHB-Lite 流水、AXI 通道配对 |
| [digital-ic-eda](skills/digital-ic-eda/SKILL.md) | 常用 EDA 工具、日志与自动化 | 从仿真到物理签核，按产品手册编写 Tcl/Python/Shell 并核对报告 |

核心原则：先确认契约，再实现与检查；区分规格、推断和工具证据；只对实际执行的配置与范围下结论。小任务按需读取参考资料，不强制套用完整流程。

五个 Skill 共享部分相对链接，建议一起安装，并保持在同一个父目录下。它们包含 5 个 Python 工具和可复制的设计/验证模板。参考资料以中文为主。

## 安装

克隆仓库，或从 GitHub 的 **Code → Download ZIP** 下载并解压。以下命令在仓库根目录运行。

```bash
git clone https://github.com/Promise-HIT/digital-ic-design-verification-skills.git
cd digital-ic-design-verification-skills
```

仓库提供一个仅使用 Python 标准库的安装器，复制全部五个 Skill；若目标已存在同名目录，会停止且不覆盖。Python 需要 **3.10 或更新版本**。

个人安装，供本机 Codex 使用：

```powershell
# Windows PowerShell
python scripts/install.py --dest "$env:USERPROFILE/.agents/skills"
```

```bash
# macOS / Linux
python3 scripts/install.py --dest "$HOME/.agents/skills"
```

项目安装：

```bash
python scripts/install.py --dest /path/to/your-project/.agents/skills
```

安装器的默认目标格式为 Codex。各平台的安装位置详见上表。[Codex Skills 说明](https://learn.chatgpt.com/docs/build-skills)

## 快速使用

在支持 `$skill-name` 的 Codex 界面中可这样发起任务：

```text
使用 $digital-ic-rtl-design，为现有工程实现参数化同步 FIFO。
先检查接口规格和构建入口，明确同时入出、深度 1 和复位语义，再实现并运行可用检查。
```

```text
使用 $digital-ic-verification，为这个 ready/valid 模块建立可追踪验证计划。
覆盖背压、reset、flush 和参数边界，给出独立 checker 和覆盖目标。
```

```text
使用 $digital-ic-review-debug，审查这次 RTL/TB diff，并分析附带仿真日志。
按影响排序报告有证据的问题，说明触发条件、位置和最小复现。
```

宿主也可根据 Skill 描述自动选择。更完整的任务输入示例和工具命令见 [docs/EXAMPLES.md](docs/EXAMPLES.md)。

## 工具与模板

以下路径相对于仓库根目录；安装后使用各 Skill 目录内对应路径。

| 工具 | 用途 | 边界 |
| --- | --- | --- |
| `skills/digital-ic-rtl-design/scripts/scan_hdl_project.py` | 只读列出 HDL、构建入口及 clock/reset 名称候选 | 词法线索，不能替代 HDL 解析与时钟域分析 |
| `skills/digital-ic-rtl-design/scripts/run_hdl_checks.py` | 执行显式配置的项目命令，保存日志和 JSON 结果 | 只记录退出码；命令需自行核对，退出码 0 不等于设计验证通过 |
| `skills/digital-ic-verification/scripts/check_verification_plan.py` | 校验需求计划 CSV；`--closure` 检查关闭证据字段 | 校验元数据与文件存在性，不鉴定证据真伪或证明 RTL 正确 |
| `skills/digital-ic-review-debug/scripts/summarize_diagnostics.py` | 按模式归并 HDL/验证日志 | 辅助分诊，根因须回到原始上下文核实 |
| `skills/digital-ic-eda/scripts/read_uvm_summary.py` | 读取单次 UVM 标准摘要的 ERROR/FATAL 次数与原始行号 | 区分非零、零和不完整摘要，验证结论另查运行结束与实际比较数 |

EDA Skill 附 [Vivado 报告 Tcl](skills/digital-ic-eda/assets/vivado-checkpoint-reports.tcl) 和[官方手册索引](skills/digital-ic-eda/references/manuals.md)。

模板位于 RTL 与验证 Skill 的 `assets/`：设计契约、验证计划、回归清单和 closure 元数据。

## 目录

```text
skills/
  digital-ic-rtl-design/       # SKILL.md、agents、references、scripts、assets
  digital-ic-verification/     # SKILL.md、agents、references、scripts、assets
  digital-ic-review-debug/     # SKILL.md、agents、references、scripts
  digital-ic-amba/             # APB、AHB-Lite 和 AXI
  digital-ic-eda/              # EDA 全流程、报告与脚本
scripts/                      # 仓库校验与安装器
tests/                        # 工具行为回归
docs/                         # 使用示例与来源说明
.github/workflows/            # Windows / Linux 自动检查
```

## 本地检查

Skill 内的 5 个工具和安装器只依赖标准库。仓库结构校验额外使用 PyYAML：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

CI 检查 Skill 元数据、相对链接、Python 语法，以及工具成功、失败、超时、未运行检查和证据缺失等行为。它不进行芯片设计签核，也不代表真实 RTL、UVM 或 EDA 环境已经验证。

## 来源与许可

本仓库根据用户提供的“数字 IC 设计与验证 Skill 增强版”整理。保留五个 Skill 的工程方法、参考路由与工具；移除个人绝对路径、重复备份和过往运行报告。

[来源说明](docs/SOURCES.md) 区分本仓库内容与外部文献。仓库不分发原书、企业手册、EDA 软件、工艺库或 UVM 发行包。原包的来源清单和归档哈希仅供定位，不能当作本次重新核验的结果。

仓库内容按 [MIT License](LICENSE) 发布；外部链接及所引用资料的权利归各自权利人所有。
