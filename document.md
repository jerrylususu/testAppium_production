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