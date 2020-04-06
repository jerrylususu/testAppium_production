# problem & solve

### problem already solved
+ Resource-id is null, try to find child node whose resource-id is not null.
+ Wait 2 second to get the true page source

### problem to be solved
+ Test always in a activity, can not transform to another activity. what should i do? 

     **Check the number of the continuous activities**
+ Many widgets' resource-id is also null. why? 

     **Just ignore**.
+ UIAutomator shut down uncorrectly

     **Change to  UIAutomator2**
+ Proxy error: Could not proxy command to remote server. Original error: Error: socket hang up.  ??

     **do not know how to do**
+ time of beginning of adb logcat

    **https://developer.android.com/studio/command-line/logcat?hl=zh-cn**
+ when the program is exit unexpectedly the adb logcat will continue

    **May be can use signal to check whether the problem is exited, if then kill the subprocess use try finally**

+ adb logcat can not be killed

    **just start adb server directly not start shell then start adb, so set shell=False**
    
+ adb logcat time is not consistent with appium log

    **can not make sure that they are sync, and also appium base on network, so use timestamp is infeasible**
    
+ So what should I get correct test case.

    **just analyse adb logcat to get Appium command(test cases)**

+ after run test need we reboot the emunlator????

    **do not know**
    
+ 由于网络问题，页面不出来，那么有些按钮就找不出来，不能复现

    **不知道怎么做，多运行几遍, 把sleep(2)加进去**
    
+ 问题：例如
03-07 00:27:21.936  4957  5275 W System.err: TARGET API FOUND&android.media.MediaCodec.queueInputBuffer(int,int,int,long,int)
03-07 00:27:21.961  4957  5275 W System.err: TARGET API FOUND&android.media.MediaCodec.queueInputBuffer(int,int,int,long,int)
03-07 00:27:21.995  4957  5275 W System.err: TARGET API FOUND&android.media.MediaCodec.queueInputBuffer(int,int,int,long,int)
03-07 00:27:22.017  4957  5275 W System.err: TARGET API FOUND&android.media.MediaCodec.queueInputBuffer(int,int,int,long,int)
03-07 00:27:22.040  4957  5275 W System.err: TARGET API FOUND&android.media.MediaCodec.queueInputBuffer(int,int,int,long,int)
03-07 00:27:22.055  4957  5275 W System.err: TARGET API FOUND&android.media.MediaCodec.queueInputBuffer(int,int,int,long,int)
这种API是一直在触发的。。。。解决看一下是否已经有这个的test了，如果有就直接跳过。。
如果没有出现再加进来。。
  **解决了 看看这个API是否已经触发过**

+ 问题：为啥按返回键之后相同activity的数量还是超出呢？？
  **解决：直接去掉这一个限制，反正有50的限制就好了**

+ 为啥会断开呢？？自己就结束了？？会回到主界面？退出app
    **突然断开连接，topping uiautomator2 io.appium.uiautomator2.http io.appium.uiautomator2.server**
    
+ 不考虑是否有bug出现，不考虑crush，不考虑是否断开，就只是找出来那些触发targetAPI的event trace就好了。。


+ 从adblog 文件里面分析出来的test和本身记录的不一致，从adblog 文件里面的command是多的，里面有的是没有执行成功的，也加进去了，，
 **解决方法，要去看下appiumresponse，把那些没有执行成功的找出来就不要加入test里面了。。**
 
+ An unknown server-side error occurred while processing the command. Original error: Could not proxy. Proxy error: Could not proxy command to remote server. Original error: Error: socket hang up
 **这个还不知道怎么解决**
 
+ 本地是使用的adb logcat来拿到日志文件的，看看到服务器上还可以吗
+ 我用的是android 9 的版本 而且是固定机型的 不知道别的机型的日志文件和这个是一样的吗，如果不一样的话，应该怎么办呢
+ 关于从apk里面拿到他的activity的信息。

+ 关于无法复现的问题，是因为zoom和pinch的原因
**应该把zoom和pinch去掉** 
现在发现滚动也会造成问题了。。问题很少发生，，，
只剩下 点击和滚动了 


* Explanation

注：下文中
test case = test
一个test含有多个event

AnalyseAPK 需要apkutils：分析 sdk_version, MainActivity
- 可能需要全部 activity （为了覆盖率）（现在已经有全部activity了 只是这里筛选了main）

ParseXML：给一个 page source 的 xml 字符串，可以解析出所有可以点击的按钮的信息
ProcessText：字符串处理 util

AppiumDriver
- desired_caps Appium运行的参数（sdk_ver, mainActivity, apk...）
- event_num 一个test case有多少个event
- activities 记录触发了哪些activity
- widgets 记录点击了那些widget（真正点到的）
- widgets_page_source 所有运行过程中可以点击的widget（一个大list）
- test_num 生成的test case的数量
- remote_addr （用于docker协调）远端 appium 地址
- adb_exe_path adb可执行文件的路径

-> appium_log 运行时的appium log
--- 现在是一个大文件 所有test都在一个log文件里（bug 没有修，但是似乎也没关系了）
-> log_file 运行时的adb log 每个test都会生成一个（到 log 文件夹下）
-> line 34 try 开始真正跑的部分
--> 34~47 连接, diff_package 判断结束条件（结束条件：连续2次不是当前package就退出）
--> line 47 while：真正跑各个 event
---> line 52 sleep 每一次操作完之后等多久才开始拿 page source
----> line 64 if 判断当前package是否和目标package一致
OnWidget：点击、send_text、滚动
OnScreen：pinch、zoom（当前已经没在再使用）
OnSystem：按物理按键 back, home, menu, vol up/down（当前没有在使用）
-----> line 68：原来是随机从三个生成机制里选一个生成下一步动作，现在只有 OnWidget了
-----> line 94：进入了和目标package不一样的package
------> line 96：如果只是一次不一样 尝试back返回
------> line 111：如果一次以上 认为被跳到不同程序了 test结束

ProcessLogFile
每个test中的event会被记录在一个list中（line 187, generate_test）
line 187 generate_test方法：解析log 文件夹里的log，检查是否触发了target_api，转换成appium的python代码，放到 tests 文件夹下（有触发放到 ctest，无触发放到 test）
appium_command 执行过的event的list
i 第几个test
trigger_target_APIs 所有test trigger到的API的全集

report
所有test生成完之后生成的总的report
1 triggered activities 所有的test case trigger的activity
2 triggered executable elements 所有的test case trigger的element
3 triggered target APIs 所有的test case trigger的target API（之前apk已经插过桩了 如果触发了target API 会在log中显示）
4 all achievable executable elements 所有遇到的page source里能点的element的全集
5 widget coverage: len(2) / len(4)

GenerateTests
line 70：test_num 生成 test 的数量
line 73：100 每个test内 event的限制


