from time import sleep

from appiumdriver.AppiumDriver import appium_driver
from processlogcat.ProcessLogFile import generate_test

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'emulator-5554'
desired_caps['appPackage'] = 'de.danoeh.antennapod'
desired_caps['appActivity'] = 'de.danoeh.antennapod.activity.SplashActivity'
desired_caps['eventTimings'] = True
desired_caps['automationName'] = 'UIAutomator2'
i = 0
trigger_native_APIs = set()
while i < 3:
    try:
        print("\n{} test:\n".format(i))
        appium_command = appium_driver(desired_caps, 50)
        print(appium_command)
        generate_test(appium_command, i, trigger_native_APIs)
    except Exception:
        print("error: {}".format(i) + "test")
    i += 1
    sleep(5)


# TODO coverage
# TODO 解析apk拿到package，activity那些信息
# TODO 将这个做成一个可以自动化运行的程序。。
# TODO 给同学分配任务 卢自动化+筛选  余问一下API怎么分类80000多也太多了吧   张问问进展给他test的一个txt。。
