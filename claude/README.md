# Claude Skills

每个角色都可单独安装。五个 Claude ZIP 各有一个与 frontmatter 的 name 相同的顶层目录，目录内含 SKILL.md、所需参考和适用的工具。包内跨技能的 Markdown 引用已收进 related/，单独上传即可读取。技能使用 name 和 description 供 Claude 发现，脚本随任务按需调用。[Anthropic 自定义 Skill 规范](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

**Claude 网页版**　在 v1.1.1 发布页下载所需的 `claude-digital-ic-*.zip`，在 Customize → Skills 选择上传并启用该 ZIP。可用“请检查这个 APB 从设备在 PREADY 拉低时是否提前提交写事务”测试协议入口。[下载本版](https://github.com/Promise-HIT/digital-ic-design-verification-skills/releases/tag/v1.1.1) · [Claude 的 Skills 使用说明](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

**Claude Code**　在仓库根目录运行以下命令安装全部角色。个人安装使用 `~/.claude/skills`，项目安装使用项目的 `.claude/skills`。目录已存在时安装器会提示冲突，保留已有内容。[Claude Code Skills 文档](https://code.claude.com/docs/en/skills)

```shell
python scripts/install.py --platform claude --dest "~/.claude/skills"
```

在 Claude Code 输入 `/digital-ic-amba`、`/digital-ic-eda`、`/digital-ic-rtl-design`、`/digital-ic-verification` 或 `/digital-ic-review-debug` 并附任务。若需从源码重建上传包，运行 `python scripts/package_skills.py --out dist`。
