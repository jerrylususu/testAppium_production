# coding = 'UTF-8'
import os
import random
import subprocess
import sys
import traceback
from time import sleep

from appium import webdriver
import logging

from appiumdriver_processlog.appiumdriver.GenerateTestBaseOnWidget import generate_test_base_on_widget
from appiumdriver_processlog.appiumdriver.GenerateTestOnSystem import generate_test_on_system
from appiumdriver_processlog.appiumdriver.util import ParseXML
from appiumdriver_processlog.appiumdriver.util.ProcessText import form_string


def appium_driver(desired_caps, event_num, activities, widgets, widgets_page_source, test_num, remote_addr='http://localhost:4723/wb/hub', adb_exe_path="adb"):
    logging.basicConfig(level=logging.INFO, filename="log/appium.log", format="%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s")
    logging.info("start of test {}".format(test_num))

    log_file = open('log/adb.log', "w")
    err_file = open('log/adberr.log', "w")
    # clear all logcat buffer?
    # TODO: WARNING: This might affect other adb connection in the same host!
    os.system(adb_exe_path+" logcat -b all -c")

    # filter output?
    p = subprocess.Popen([adb_exe_path, "logcat", "appium:I", "System.err:W", "AndroidRuntime:E", "*:S"], stdout=log_file, stderr=err_file)
    appium_command = []
    print("{*} adb prepare done")

    try:
        print("{*} connecting to webdriver at " + remote_addr)
        logging.info("{*} connecting to webdriver at " + remote_addr)
        driver = webdriver.Remote(remote_addr, desired_caps)
        print("{*} driver initialized")
        # the number of the continuous same activities
        same_act_num = []

        # the number of the continuous same activities
        diff_package = []

        # the number of loop
        i = 0
        while i < event_num:
            print("{+} start of event", i)
            logging.info(form_string("{+}", "start of event {}".format(i)))

            # sleep for get page source
            sleep(1)
            appium_command.append("sleep(1)")
            page_source = driver.page_source

            # get the current activity, package
            activity = driver.current_activity
            package = driver.current_package

            # add activity to triggered activities
            activities.add(activity)

            # check current package
            if package == desired_caps['appPackage']:
                # update the different package
                diff_package = list()

                random_num = random.random()
                # if len(same_act_num) < 50:
                if random_num > 0.2:
                    print("{+} start event based on widget")
                    logging.info("{+} start event based on widget")

                    # get package name and executable widgets
                    executable_elements = ParseXML.parseXml(page_source)

                    # add excutable_elements to widgets_page_source
                    print("{~} debug: outputing executable_elements ")
                    for excutable_ele in executable_elements:
                        print("{~} -", excutable_ele, "->", excutable_ele.get('resource-id'))
                        a = form_string("{~} -", str(excutable_ele), "->", str(excutable_ele.get('resource-id')))
                        print(a)
                        logging.info(form_string("{~} -", str(excutable_ele), "->", str(excutable_ele.get('resource-id'))))
                        widgets_page_source.add(excutable_ele.get('resource-id'))
                    generate_test_base_on_widget(driver, executable_elements, logging, i, appium_command, widgets)

                else:
                    print("{+} start event based on system")
                    logging.info("{+} start event based on system")

                    generate_test_on_system(driver, logging, i, appium_command)

                i += 1

            else:
                diff_package.append(package)
                if len(diff_package) == 1:
                    try:
                        driver.press_keycode(4)
                        logging.warning("{w} the current package name is different from the given apk'")
                        print("{w} the current package name is different from the given apk'")

                        logging.info(form_string("{~}", "event {}:".format(i), "system", "keycode:", str(4)))
                        print(form_string("{~}", "event {}:".format(i), "system", "keycode:", str(4)))
                        appium_command.append("driver.press_keycode(4)")
                    except Exception:
                        print(form_string("{w}", "event {}:".format(i), "system", "Something went wrong when press", str(4)))
                        logging.error(
                            form_string("{w}", "event {}:".format(i), "system", "Something went wrong when press", str(4)))
                    finally:
                        i += 1
                else:
                    logging.warning(form_string("{w}", "the current package name is still different from the given apk'"))
                    print("{w}", "the current package name is still different from the given apk'")

                    break
        driver.quit()
    except Exception as excp:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_tb(exc_traceback_obj)
        print("wrong!!", excp)

    finally:
        p.kill()
        p.wait()
        logging.info(form_string("appium commands:", str(appium_command)))
        return appium_command

# TODO 不进行筛选  有多少出多少  看看还有重复的问题嘛  多跑几个apk 试试
# TODO 把GitHub上的传到服务器 看看可以吗
# TODO 怎么能够更智能化一点呢
# TODO replay 太随机了 有的可以有的不可以？？
# TODO 一定要确保。。。