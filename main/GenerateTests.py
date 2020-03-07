from time import sleep

from appiumdriver.AppiumDriver import appium_driver
from appiumdriver.DriverConfig import config
from processlogcat.ProcessLogFile import generate_test

# TODO 统计覆盖率 activity/widget
i = 0
while i < 10:
    desired_caps = config()
    try:
        print("\n{} test:\n".format(i))
        appium_command = appium_driver(desired_caps, 100)
        print(appium_command)
        generate_test(appium_command, i)
    except Exception:
        print("error: " + i + "test")
    i += 1
    sleep(5)
