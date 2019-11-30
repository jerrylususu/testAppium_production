import signal
from time import sleep

from appium import webdriver
import random

import parseXML
from event.event_widgt import generate_test_baseon_widget
from event.event_coordinate import generate_test_random


desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'emulator-5554'
desired_caps['appPackage'] = 'com.menny.android.anysoftkeyboard'
desired_caps['appActivity'] = 'com.menny.android.anysoftkeyboard.LauncherSettingsActivity'



driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.end_test_coverage("Intent", "C:\\Users\\dell\\PycharmProjects\\testAppium\\coverage.txt")
i = 0
while True:
    # get page_source
    i += 1
    print("第 %d 个操作" % i)
    sleep(3)
    page_source = driver.page_source
    print("获取xml文件")
    # random test
    dict, package = parseXML.parseXml(page_source)
    print(package)
    print(desired_caps['appPackage'])
    if (package == desired_caps['appPackage']):
        random_num = random.random()
        if(random_num > 0.5):
            print("***test based on widget***")
            generate_test_baseon_widget.random_test(driver, dict)
        else:
            print("***test on the screen***")
            generate_test_random.random_test(driver)
    else:
        # try:
        #     driver.start_activity('com.menny.android.anysoftkeyboard', '.LauncherSettingsActivity')
        # except:
        #     print("can not launch main activity")
        break
