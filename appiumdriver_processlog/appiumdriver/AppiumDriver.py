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

from func_timeout import func_timeout, FunctionTimedOut, func_set_timeout
import base64
from initialize_utils.timeout_fix import timeout_exception_wrapper

@timeout_exception_wrapper
@func_set_timeout(300)
def appium_driver(desired_caps, event_num, activities, widgets, widgets_page_source, test_num, remote_addr='http://localhost:4723/wb/hub', adb_exe_path="adb", apk_name="", adb_port=5554):
    # appium_log = f"log/{apk_name}_appium.log"
    # logging.basicConfig(level=logging.INFO, filename=appium_log, format="%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s")
    logging.info("start of test {}".format(test_num))

    log_file = open(f'log/{apk_name}_adb{test_num}.log', "w")
    # err_file = open('log/adberr{}.log'.format(test_num), "w")
    # clear all logcat buffer?
    # TODO: WARNING: This might affect other adb connection in the same host!
    print("adb 1")
    os.system(adb_exe_path+" devices")
    print(adb_exe_path+f" -s localhost:{adb_port}" +" logcat -b all -c")
    os.system(adb_exe_path+f" -s localhost:{adb_port}" +" logcat -b all -c")
    # subprocess.Popen(adb_exe_path+f" -s localhost:{adb_port}" +" logcat -b all -c", shell=True)

    print("adb 2")

    # filter output?
    p = subprocess.Popen([adb_exe_path,  "-s",  f"localhost:{adb_port}", "logcat", "-s","appium:I", "System.err:W", "AndroidRuntime:E", "*:S"], stdout=log_file)
    print("adb 3")
    
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
                if random_num > 0:
                    print("{+} start event based on widget")
                    logging.info("{+} start event based on widget")

                    # get package name and executable widgets
                    executable_elements = ParseXML.parseXml(page_source)

                    # add excutable_elements to widgets_page_source
                    print("{~} debug: outputing executable_elements ")
                    for excutable_ele in executable_elements:
                        # print("{~} -", excutable_ele, "->", excutable_ele.get('resource-id'))
                        # a = form_string("{~} -", str(excutable_ele), "->", str(excutable_ele.get('resource-id')))
                        # logging.info(form_string("{~} -", str(excutable_ele), "->", str(excutable_ele.get('resource-id'))))
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
        
        with open(f"generate_screenshots/{apk_name}_{str(test_num)}.png","wb") as pngfile:
            pngfile.write(base64.b64decode(driver.get_screenshot_as_base64()))
        
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
