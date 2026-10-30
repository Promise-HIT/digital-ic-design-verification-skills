# UVM 可执行工程检查

主要依据为 [Accellera 官方指南/API 与参考实现](official-uvm.md)。本地《UVM 实战》明确基于 UVM 1.1d，仅作辅助案例。先读取工程 UVM 版本和库源码；1.1d、1.2、IEEE 1800.2 的废弃接口和兼容模式不能混用。禁止自动升级工程 UVM 库。

## 编译与启动

明确 simulator/语言模式、UVM 库由工具预编译还是源码编译，禁止重复编译不同版本。顺序通常为公共 package、interface、transaction/config/agent/env/test package、top；包含依赖决定具体顺序。宏头文件不替代 `import uvm_pkg::*`。

先跑最小 smoke，确认 `run_test` 入口、test 名、factory 注册、拓扑、virtual interface 配置和时钟/reset。编译通过后 test 未被创建也不能算通过。

## 配置与连接

- virtual interface 的类型（含 modport/参数）必须和 `config_db` 的模板类型一致；`set` 应在消费者 `get` 前完成；关键 `get` 失败立即 fatal。
- scope 路径优先精确到实例；通配符可能污染多个 agent。调试时打印 topology/config trace，避免反复盲改字符串。
- `build_phase` 创建组件和获取配置，`connect_phase` 连接 TLM。遵循 `super` 调用要求；不要手动调用组件 phase 来“修复”调度。
- active agent 有 sequencer/driver，passive agent 只观察；多 agent 共享资源和配置要有明确所有者。

## 事务所有权和并发

sequence 只描述事务，driver 执行协议。`get_next_item` 与 `item_done` 配对，不能过早通知完成后继续修改同一对象；明确请求接受与响应返回的不同时间点。

analysis `write()` 是 function，不能阻塞等待。发布的是对象句柄；monitor 每次创建新对象，或者消费者在缓存前 clone/copy。检查自定义字段是否被 `do_copy`/field 宏覆盖，嵌套对象是否深拷贝。事务打印正确不证明比较/拷贝字段完整。

多个 monitor 同时到达时，scoreboard 不依赖同时间槽调用顺序；可按 timestamp/cycle/tag 入队后统一匹配。乱序用 ID 和 reset epoch 管理，检测重复 ID、丢失响应、超时和未匹配队列。不能以 DUT 输出反填 expected。

## Phase、结束与复位

由 test/virtual sequence 等明确所有者管理 objection，在首个耗时等待前 raise，等待 stimulus 完成和 scoreboard drain 后 drop。无限 monitor 不永久持有 objection；遗漏 drop 是 hang 的根因候选。drain time 是辅助机制，不能替代完成条件。

phase jump/reset 不会自动清空所有用户队列、mailbox、sequence 或 outstanding。定义 reset 时谁停止驱动、取消/重启 sequence、丢弃或保留哪一代事务，之后才重新允许检查。运行中 reset 要有独立测试。

## 错误和收尾

`randomize()` 失败必须触发失败；report catcher/严重度降级须有项目依据。最终检查 UVM_ERROR/FATAL、checker mismatch、assertion failure、协议违规、未完成事务和覆盖目标；退出码为 0 不是唯一条件。

RAL 只在寄存器验证需要时引入：检查 adapter byte enable、endianness、frontdoor/backdoor、volatile/W1C/RC 语义、predictor 与 auto_predict 是否重复更新 mirror，以及 reset 后 mirror 同步。
