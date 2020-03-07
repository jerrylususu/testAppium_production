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
while i < 1:
    try:
        print("\n{} test:\n".format(i))
        appium_command = appium_driver(desired_caps, 50)
        print(appium_command)
        generate_test(appium_command, i)
    except Exception:
        print("error: {}".format(i) + "test")
    i += 1
    sleep(5)
