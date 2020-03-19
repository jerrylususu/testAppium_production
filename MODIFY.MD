# 我的修改

卢之睿

1. `docker_init.py`：用于启动测试用的 Docker 容器
2. `adb_connect_install.py`：用于在容器启动后连接并安装指定 APK
3. 上述二文件置于 `initialize_utils`：启动测试前的相关准备工具 
4. 为了符合我的本地结构，将 `GenerateTests.py` 置于外层，以解决依赖错误问题
5. 为了保证端口变化时，Appium 依然可以正常连接，为 `appium_driver` 函数增加了 `remote_addr` 参数
6. 因为我没有 root 权限，需要手动指定 adb 可执行文件位置，为 `appium_driver` 函数增加了 `apk_exe_path` 参数 