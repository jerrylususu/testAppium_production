from appium import webdriver
import util

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'emulator-5554'
desired_caps['appPackage'] = 'com.codbking.calendar.exaple'
desired_caps['appActivity'] = 'com.codbking.calendar.exaple.MainActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
page_source = driver.page_source
print(page_source)
util.StringToXml(page_source)

driver.find_element_by_id('com.codbking.calendar.exaple:id/text1').click()








