from appium import webdriver
import random

from event.event_widgt import generate_test_baseon_widget
from event.event_coordinate import generate_test_random

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'emulator-5554'
desired_caps['appPackage'] = 'com.codbking.calendar.exaple'
desired_caps['appActivity'] = 'com.codbking.calendar.exaple.MainActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
element = driver.find_element_by_id("com.codbking.calendar.exaple:id/text1")
element.click()
element_1 = driver.find_element_by_id("com.codbking.calendar.exaple:id/text")
element_1.click()
element_2 = driver.find_element_by_id("com.codbking.calendar.exaple:id/text")
element_2.click()
element_3 = driver.find_element_by_id("com.codbking.calendar.exaple:id/text")
element_3.click()
element_4 = driver.find_element_by_id("com.codbking.calendar.exaple:id/text")
element_4.click()
element_5 = driver.find_element_by_id("android:id/text1")
element_5.click()


# while True:
#     # get page_source
#     page_source = driver.page_source
#     print(page_source)
#     # random test
#     random_num = random.random()
#     # if(random_num > 0.5):
#     generate_test_baseon_widget.random_test(driver, page_source)
#     # else:
#     #     generate_test_random.random_test(driver)
