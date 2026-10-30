# Sequence、Factory 与寄存器验证

需要这些能力时才读取；官方入口见 [official-uvm.md](official-uvm.md)。以下工程建议应在项目匹配版本上验证。

## Sequence/driver 的完成语义

`start_item` 获得许可后 randomize，随后 `finish_item`。两者之间不插入 `#delay`、event wait 等耗时操作。返回不自动代表 DUT 已返回响应，具体取决于 driver 的完成契约。

driver 的 `get_next_item/item_done` 与 `get/put` 是不同交互模式，不混搭随意多调用 `item_done`。流水 driver 需要单独定义 request 生命周期和 response 通道；response 正确继承 request 的 sequence/transaction 身份，例如匹配版 `set_id_info(req)`，并有消费者读取响应，避免 response queue overflow。

virtual sequence 协调多个 sequencer；它本身不是 pin driver。检查句柄配置、sequence 生命周期、并发顺序和结束 drain。锁定/抢占仲裁只在必要范围使用，reset/kill 后需释放资源。自动 phase objection 依赖有效 starting phase；无限 body 不适合依赖自动结束。

sequence 的 `pre_body/post_body` 在某些子 sequence 调用方式下可被跳过，不能把必需初始化或唯一 objection 逻辑放进去而不检查调用语义。关键配置在 `pre_start` 或明确的 test 层生命周期处理时仍需匹配版本。

## Factory

需要可覆盖的 component/object 通过 `type_id::create`；直接 `new` 会绕过该创建点的 factory override。核对类型注册、type override/instance override、层级路径和设置时机。参数化类宏与非参数化宏区别要与库版本一致；不要假设字符串名称自动包含参数。

先输出实际拓扑/创建类型再调试 stimulus。所有权明确的内部小对象无需为了形式统一强制 factory 化。

## RAL 路径与语义

从寄存器规格提取 address map、bus width、endianness、byte enable、访问权限、reset kind/value、volatile 和 side effect。W1C/RC、硬件自更新和 alias 需单独测试；只跑普通 RW bit-bash 不够。

adapter 完成 `reg2bus/bus2reg` 映射和 status，明确总线响应模型/`provides_responses`。模型 `build`、map/base address、sequencer+adapter、`lock_model` 和 predictor 连接顺序按工程版本执行。

选择一种清晰的 mirror 更新策略：map auto-predict 或基于 monitor 的显式 predictor；避免同一访问重复预测。外部 master 和硬件自更新不能仅靠本 test 的写入来更新 expected。memory 默认不等同于寄存器 mirror，不能承诺 predictor 自动覆盖所有存储内容。

区分 desired、mirrored 与实际 DUT 值：`set` 改模型 desired，`update` 才可能发起访问；`get_mirrored_value` 不执行物理读。`reset()` 重置模型不代表已经驱动 DUT reset。`read/write/mirror` 的访问路径、检查开关和 side effect 必须分别审查。

backdoor 需核对 HDL path、位切片、可见性和权限；backdoor 写不能代替 frontdoor 协议验证。测试至少覆盖 reset 值、合法读写、byte enable、权限/side effect、硬件更新与多访问源冲突，并保存真实总线 monitor 证据。
