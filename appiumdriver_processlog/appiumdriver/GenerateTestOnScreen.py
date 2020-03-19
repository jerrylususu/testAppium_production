import random

from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction

from appiumdriver_processlog.appiumdriver.util.ProcessText import form_string


def generate_test_on_screen(driver, logging, i, appium_command):
    event_list = ['pinch', 'zoom']
    selected_event = random.choice(event_list)

    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']

    if selected_event == 'pinch':
        try:
            width = driver.get_window_size()['width']
            height = driver.get_window_size()['height']
            action1 = TouchAction(driver).press(el=None, x=width * 0.2, y=height * 0.2).wait(1000).move_to(el=None,
                                                                                                           x=width * 0.4,
                                                                                                           y=height * 0.4).release()
            action2 = TouchAction(driver).press(el=None, x=width * 0.8, y=height * 0.8).wait(1000).move_to(el=None,
                                                                                                           x=width * 0.6,
                                                                                                           y=height * 0.6).release()
            pinch_action = MultiAction(driver)
            pinch_action.add(action1, action2)
            pinch_action.perform()
            logging.info(form_string("{~}", "event {}:".format(i), "screen", "operation:", "pinch"))
            print(form_string("{~}", "event {}:".format(i), "screen", "operation:", "pinch"))
            appium_command.append("driver.multi_perform_pinch()")
        except Exception:
            print(form_string("{w}", "event {}:".format(i), "screen", "Something went wrong when pinch"))
            logging.error(form_string("{w}", "event {}:".format(i), "screen", "Something went wrong when pinch"))

    else:
        try:
            action1 = TouchAction(driver).press(el=None, x=width * 0.4, y=height * 0.4).wait(1000).move_to(el=None,
                                                                                                           x=width * 0.2,
                                                                                                           y=height * 0.2).release()
            action2 = TouchAction(driver).press(el=None, x=width * 0.6, y=height * 0.6).wait(1000).move_to(el=None,
                                                                                                           x=width * 0.8,
                                                                                                           y=height * 0.8).release()
            pinch_action = MultiAction(driver)
            pinch_action.add(action1, action2)
            pinch_action.perform()
            logging.info(form_string("{~}", "event {}:".format(i), "screen", "operation:", "zoom"))
            print(form_string("{~}", "event {}:".format(i), "screen", "operation:", "zoom"))
            appium_command.append("driver.multi_perform_zoom()")
        except Exception:
            print(form_string("{w}", "event {}:".format(i), "screen", "Something went wrong when zoom"))
            logging.error(form_string("{w}", "event {}:".format(i), "screen", "Something went wrong when zoom"))
