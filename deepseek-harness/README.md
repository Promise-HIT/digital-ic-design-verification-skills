# 数字 IC 技能插件 · DeepSeek Harness

把本包安装到你运行的 Harness profile 后，模型可以从技能目录加载 RTL 设计、验证开发和故障评审的教材规则、代码练习与报告检查步骤。插件使用当前会话选中的模型和项目工作目录。

## 安装与启用

下例使用 `web` profile。终端用户把 `web` 换成 `tui`，脚本用户可换成 `headless`。首次使用需要可联网的 DeepSeek Harness，本文针对 0.2.2-rc.5，Node.js 24.9 或更新版本。

通过 GitHub 上固定版本的发布包安装：

```sh
dsh plugin --profile web add https://github.com/Promise-HIT/digital-ic-design-verification-skills/releases/download/dsh-v1.0.0/dsh-digital-ic-skills-1.0.0.tgz
dsh --profile web --dump-config
```

在输出中查找 `digital-ic-skills` 插件行。重新启动该 profile，开一个新会话。npm 公共注册表中对应的包名为 `dsh-digital-ic-skills`，可用以下命令查询发布状态并按名称安装：

```sh
npm search dsh-digital-ic-skills --registry=https://registry.npmjs.org
npm view dsh-digital-ic-skills version --registry=https://registry.npmjs.org
dsh plugin --profile web add dsh-digital-ic-skills
```

只需要将包下载到普通 Node 项目时，使用 `npm install dsh-digital-ic-skills`，也可把包名换成上面的完整 .tgz URL。Harness 的启用步骤是 `dsh plugin --profile … add …`。

## 第一次使用

在模型选择器中选择你的服务商已经配置的 **DeepSeek V4.1 Flash 1017** 或 **GLM-5.3**。模型 ID 和凭据由服务商管理。例如阿里云的对应 ID 是 `deepseek-v4.1-flash-1017` 和 `glm-5.3`。[服务商配置示例](https://www.alibabacloud.com/help/en/model-studio/deepseek-harness)

在有 RTL 或测试平台的工作目录发起一次任务。可明确指定技能名，也可描述工作，让模型按技能描述选择。

| 你想完成的事 | 可直接发送的请求 |
| --- | --- |
| 写 RTL | 请加载 digital-ic-rtl-design。按工程的 Verilog-2001 风格实现带背压的单级缓存，说明 stall 时如何保持数据，运行最小自检查测试。 |
| 写验证方案和代码 | 请加载 digital-ic-verification。为深度 3 的同步 FIFO 写需求表、独立队列 scoreboard 和满时同时读写的测试。固定 seed，证明故意改错一个有效数据位时 checker 会报错。 |
| 查 Synopsys 报告 | 请加载 digital-ic-review-debug。分析附带的 VCS 日志，用最早失败的事务定位 Verdi 应查看的信号，并区分已证实的原因与待查项。 |

模型响应中的技能调用及返回的正文可用于确认加载。在同一模型、同一 RTL 工程和同一测试集上对比启用前后的编译结果、边界用例通过数和 checker 注错检出率，可评估你的实际收益。仿真、综合和时序检查使用项目已有工具、许可和库。

## 从源码打包

在本目录执行 `npm pack`。包内的 curriculum/ 含三个独立入口，每组专业规则都附书名和页码或章节，可直接审阅。把生成的 .tgz 的绝对路径传给 `dsh plugin --profile web add` 即可试用。原有 Codex 工具仍随仓库根目录的 skills/ 分发。

[Harness 官方插件打包说明](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/publish.md) · [项目首页](https://github.com/Promise-HIT/digital-ic-design-verification-skills)
