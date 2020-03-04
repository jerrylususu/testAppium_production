from appiumdriver.AppiumDriver import appium_driver
from appiumdriver.DriverConfig import config
from processlogcat.ProcessLogFile import check_and_complete_test, generate_test

desired_caps = config()
appium_command = appium_driver(desired_caps, 'log/appiumlog.log', 'log/adblog.log', 'log/adberr.log', 30)
print(appium_command)
generate_test('log/adblog.log', appium_command)

