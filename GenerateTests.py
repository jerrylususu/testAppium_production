from time import sleep

from appiumdriver_processlog.appiumdriver.AppiumDriver import appium_driver
from appiumdriver_processlog.processlog.ProcessLogFile import generate_test

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'emulator-5554'
desired_caps['appPackage'] = 'de.danoeh.antennapod'
desired_caps['appActivity'] = 'de.danoeh.antennapod.activity.SplashActivity'
desired_caps['eventTimings'] = True
desired_caps['automationName'] = 'UIAutomator2'
i = 0
# record target APIs triggered
trigger_native_APIs = set()
# record activities triggered
activities = set()
# record widgets triggered
widgets = set()
# record widgets in page_source
widgets_page_source = set()

while i < 3:
    try:
        print("\n{} test:\n".format(i))
        appium_command = appium_driver(desired_caps, 50, activities, widgets, widgets_page_source)
        print(appium_command)
        generate_test(appium_command, i, trigger_native_APIs)
    except Exception:
        print("error: {}".format(i) + "test")
    i += 1
    sleep(5)
print(activities)
print(widgets)
print(widgets_page_source)
