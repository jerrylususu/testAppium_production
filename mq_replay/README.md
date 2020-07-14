# MQ-based replay

## 各个脚本描述

配置：
- replay_pool.json：描述了预期生成的虚拟设备的数量

脚本：
- replaytask: 消息传递类
- producer: 读取 testcase，生成 ReplayRequest，放入 MQ
- pool_virtual：根据 json 中的描述，生成对应的 docker，写入 pool_status 文件
- use.sh：根据 pool_status 文件，一个 docker 启动一个 runner，来具体从队列里获取 ReplayRequest
- pool_runner: 根据 ReplayRequest 执行 replay，结果打包成 ReplayResponse，放入 MQ
- conusmer：具体的 replay 过程描述
- result_receiver：把 ReplayResponse 写入文件，保存到磁盘（在当前单机暂时不需要，多机器环境下需要）
-- 其实大概也可以直接手动复制结果

## 数据描述

replay_request: routing_key=version.(virtual/physical) (f"{android_version}_{device_type}")

replay_response: routing_key=f"{replay_request.apkName}.{replay_request.androidVersion}.{testcase.testNumber}.{testcase.ctestNumber}"

status_line: f"{container.id},{adb_port},{appium_port},{version},{idx},{device_type(virtual/physical)},{emu_port},{gui_port}"


## 测试

### 原理性验证
1. adb uninstall 测试（手动启动）-> 已经确认 OK
2. routing_key 设置为 # 能否接受到所有消息（用官网示例）-> 已经确认可行

### 联调
2. 用一个testcase测试mq能否正常读入
3. 用一个简单的replay_pool.json测试virtual+启动脚本是否能正常完成一个replay流程
4. 测试3个app的所有testcase 


### 再说
1. adb 真机测试
5. 测试receiver能否正常完成写入


## 其他重要的文件夹记录

1. 生成阶段

    脚本：GenerateMulti.py

    文件夹
    - logs 生成过程中adb的记录
    - report 生成过程中driver的结果（注意这个coverage是有问题的）
    - generate_logs 生成过程中生成脚本的记录
    - tests/ctest 触发了 API 的测试样例
    - tests/test 没有触发 API 的测试样例

2. 转换阶段

    脚本：replay/testcase_txt_to_py.py

    文件夹：
    - replay/output 生成的测试样例 py 文件

3. 重放阶段：

    脚本：
    - 旧：docker_replay_multi_logging.py
    - 新：mq_replay/...

    文件夹：
    - replay/replay_adb：重放过程中adb的记录
    - replay/replay_logs：重放过程中脚本的记录（仅旧版本）
    - replay/replay_screenshots：重放过程中的截图
    - replay/replay_page_sources：重放过程中的page source

