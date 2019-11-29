from appium import webdriver
import random

from event.event_widgt import generate_test_baseon_widget
from event.event_coordinate import generate_test_random

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'emulator-5554'
desired_caps['appPackage'] = 'com.menny.android.anysoftkeyboard'
desired_caps['appActivity'] = 'com.menny.android.anysoftkeyboard.LauncherSettingsActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


while True:
    # get page_source
    page_source = driver.page_source
    print(page_source)
    # random test
    random_num = random.random()
    # if(random_num > 0.5):
    generate_test_baseon_widget.random_test(driver, page_source)
    # else:
    #     generate_test_random.random_test(driver)
