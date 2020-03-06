from time import sleep

from appiumdriver.AppiumDriver import appium_driver
from appiumdriver.DriverConfig import config
from processlogcat.ProcessLogFile import generate_test

i = 0
while i < 100:
    desired_caps = config()
    try:
        print("{} test:\n".format(i))
        appium_command = appium_driver(desired_caps, 50)
        print(appium_command)
        generate_test(appium_command, i)
    except Exception:
        print("error: " + i + "test")
    i += 1
    sleep(5)
