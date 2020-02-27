# coding = 'UTF-8'
import os
import random
import subprocess
from time import sleep

from appium import webdriver
import logging

from testgenerate.GenerateTestBaseOnWidget import generate_test_base_on_widget
from testgenerate.GenerateTestOnScreen import generate_test_on_screen
from testgenerate.GenerateTestOnSystem import generate_test_on_system
from util import ParseXML
from util.ProcessText import delete_text

delete_text('log/logcat.log')
delete_text('log/runlog.log')
logging.basicConfig(level=logging.INFO, filename="log/runlog.log", format="%(asctime)s%(filename)s [line:%(lineno)d] %(levelname)s %(message)s")

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'emulator-5554'
desired_caps['appPackage'] = 'de.danoeh.antennapod'
desired_caps['appActivity'] = 'de.danoeh.antennapod.activity.SplashActivity'
desired_caps['eventTimings'] = True
logging.info("logging app...")

p = subprocess.Popen("exec " + "adb logcat > log/logcat.log", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# sleep for get true page source
sleep(2)

i = 1
while i < 50:
    # get page_source
    page_source = driver.page_source

    # get package name and executable widgets
    package, executable_elements = ParseXML.parseXml(page_source)

    # check current package
    if package == desired_caps['appPackage']:
        random_num = random.random()
        if random_num > 0.2:
            succeed = generate_test_base_on_widget(driver, executable_elements, logging, i)
        elif random_num > 0.1:
            succeed = generate_test_on_screen(driver, logging, i)
        else:
            succeed = generate_test_on_system(driver, logging, i)
        if succeed:
            i += 1
    else:
        break
p.kill()
