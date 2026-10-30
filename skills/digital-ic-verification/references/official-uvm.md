# UVM 官方依据与版本选择

原始增强包记录日期：2026-10-30。链接和归档哈希继承自原包，本次公开整理未重新下载并验证这些归档。此处是任务路由和工程检查建议，不替代官方标准。以下来源均为 Accellera 官方发布或官方源码。

## 官方资料

|来源|用途与适用边界|
|---|---|
|[Accellera 下载页](https://www.accellera.org/downloads/standards/uvm)|核对可用版本；原包记录了 2020-3.2 参考实现，不能据此替项目升级|
|[UVM 1.2 User’s Guide](https://www.accellera.org/images/downloads/standards/uvm/uvm_users_guide_1.2.pdf)|2015-10-08；1.2 架构与方法学。§2.3.3 analysis、§3.5 driver/sequencer、§3.6 monitor、§3.11 结束、§4.4 config、§5.4 virtual sequence、§5.9 register layer|
|[UVM 1.2 Class Reference](https://www.accellera.org/images/downloads/standards/uvm/UVM_Class_Reference_Manual_1.2.pdf)|2014-06；核对 1.2 的类/方法契约。按方法名检索：`copy/clone/do_copy`、`uvm_config_db`、`uvm_objection`、`uvm_sequence_base`、`uvm_sqr_if_base`、`uvm_reg_map`|
|[2020-3.2 官方实现压缩包](https://www.accellera.org/images/downloads/standards/uvm/1800.2-2020.3.2%20Release.gz)|原包记录的 1800.2-2020 系列实现；归档 SHA256 见本目录 `official-source-lock.json`|
|[Accellera 官方 uvm-core](https://github.com/accellera-official/uvm-core)|分支内容会变化；使用时核对并固定 tag/commit，区分仓库版本与官网压缩包版本|
|[官方实现偏差说明](https://github.com/accellera-official/uvm-core/blob/main/DEVIATIONS.md)|实现和 IEEE 标准可能存在偏差；阅读匹配发布包内的同名文件|

不能宣称 1.2 User’s Guide 就是 IEEE 1800.2-2020 手册，也不能把参考实现全部公共方法称为 IEEE 标准 API。IEEE 标准全文未在本仓库整理过程中逐条审计；需要条款级结论时通过官方授权路径读取原文。

## 写代码之前

记录工程实际 library banner/version、库路径、工具自带补丁、语言模式、DPI 开关和编译宏。按这个版本选择文档；版本未知时先从工程日志/filelist 找，不盲猜。

2020 系列源码通过 `@uvm-ieee`、`@uvm-contrib`、`@uvm-accellera`、`@uvm-compat` 区分 API 来源。可移植代码避免依赖内部 `m_*` 实现；使用扩展或兼容 API 必须说明版本条件。兼容包用于适配旧 API，不保证在旧库中获得新 API。

## 从官方契约落实到检查

|主题|核对锚点|落实方式|
|---|---|---|
|analysis|`src/tlm1/uvm_analysis_port.svh::write`|function 广播，无自动 clone；必需订阅者显式检查连接|
|config|`src/base/uvm_config_db.svh::get/set`|模板类型、context/instance scope、调用阶段一致；运行 trace 诊断|
|sequence|`src/seq/uvm_sequence_base.svh::start_item/finish_item`|两者之间不插入耗时等待；失败随机化直接报错|
|driver|`src/tlm1/uvm_sqr_ifs.svh::get_next_item/item_done`|配对完成，区分消费请求与发送 response|
|copy|`src/base/uvm_object.svh::clone/copy/do_copy`|clone 使用 create+copy；核对自定义/嵌套字段|
|phase|`src/base/uvm_objection.svh`、`uvm_phase.svh`|明确 objection owner，结束前以 checker/outstanding 判定 drain|
|RAL|`src/reg/uvm_reg_predictor.svh`、`uvm_reg_map.svh`|预测来自实际总线观察；定义 mirror 更新所有者|

以上落实方式包含工程建议；官方定义与额外质量门禁不要混称。命令行 debug 开关是否支持由实际库/工具确认。

## 查证顺序

先查匹配版 Class Reference 的类/方法说明，再查该版库注释及实现，最后做最小编译/行为复现。API 签名正确不代表 sequence 生命周期、对象所有权或结束行为正确；每个新增环境至少跑可观察非零比较的 smoke。
