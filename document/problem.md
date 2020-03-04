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

    **不知道怎么做，多运行几遍**