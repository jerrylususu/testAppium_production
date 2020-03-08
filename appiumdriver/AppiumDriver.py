# coding = 'UTF-8'
import os
import random
import subprocess
from time import sleep

from appium import webdriver
import logging

from appiumdriver.GenerateTestBaseOnWidget import generate_test_base_on_widget
from appiumdriver.GenerateTestOnScreen import generate_test_on_screen
from appiumdriver.GenerateTestOnSystem import generate_test_on_system
from util import ParseXML
from util.ProcessText import delete_text, form_string


def appium_driver(desired_caps, event_num, activities, widgets, widgets_page_source):
    logging.basicConfig(level=logging.INFO, filename='log/appium.log', format="%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s")
    logging.info("logging app...")

    try:
        delete_text('log/appium.log')
    except FileNotFoundError:
        logging.error("appium log is not found")
        print("appium log is not found")

    log_file = open('log/adb.log', "w")
    err_file = open('log/adberr.log', "w")
    os.system("adb logcat -b all -c")
    p = subprocess.Popen(["adb", "logcat", "appium:I", "System.err:W", "AndroidRuntime:E", "*:S"], stdout=log_file, stderr=err_file)
    appium_command = []

    try:
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        # the number of the continuous same activities
        same_act_num = []

        # the number of the continuous same activities
        diff_package = []

        # the number of loop
        i = 0
        while i < event_num:
            # sleep for get page_source
            sleep(1.5)
            appium_command.append("sleep(1.5)")
            page_source = driver.page_source

            # get the current activity, package
            activity = driver.current_activity
            package = driver.current_package

            # add activity to triggered activities
            activities.add(activity)

            # get package name and executable widgets
            executable_elements = ParseXML.parseXml(page_source)

            # add excutable_elements to widgets_page_source
            for excutable_ele in executable_elements:
                widgets_page_source.add(excutable_ele.get('resource-id'))

            # check current package
            if package == desired_caps['appPackage']:
                # update the different package
                diff_package = list()

                # update the number of the continuous same activities
                if len(same_act_num) == 0:
                    same_act_num.append(activity)
                elif activity == same_act_num[-1]:
                    same_act_num.append(activity)
                else:
                    same_act_num = list()
                    same_act_num.append(activity)
                random_num = random.random()
                if random_num > 0.2:
                    succeed = generate_test_base_on_widget(driver, executable_elements, logging, i, appium_command, widgets)
                elif random_num > 0.1:
                    succeed = generate_test_on_system(driver, logging, i, appium_command)
                else:
                    succeed = generate_test_on_screen(driver, logging, i, appium_command)
                if succeed:
                    i += 1
            else:
                diff_package.append(package)
                if len(diff_package) == 1:
                    try:
                        driver.press_keycode(4)
                        logging.warning("the current package name is different from the given apk'")
                        print("the current package name is different from the given apk'")
                        logging.info(form_string("event {}:".format(i), "system", "keycode:", str(4)))
                        print(form_string("event {}:".format(i), "system", "keycode:", str(4)))
                        appium_command.append("driver.press_keycode(4)")
                        i += 1
                    except Exception:
                        print(form_string("event {}:".format(i), "system", "Something went wrong when press", str(4)))
                        logging.error(
                            form_string("event {}:".format(i), "system", "Something went wrong when press", str(4)))
                else:
                    logging.warning("the current package name is still different from the given apk'")
                    print("the current package name is still different from the given apk'")

                    break
        driver.quit()

    except:
        print("remote collection went wrong")

    finally:
        p.kill()
        p.wait()
        return appium_command
