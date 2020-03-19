import random

from appiumdriver_processlog.appiumdriver.util.ProcessText import form_string


def generate_test_on_system(driver, logging, i, appium_command):
    '''
    KEYCODE_HOME: 3
    KEYCODE_BACK: 4
    KEYCODE_VOLUME_UP: 24
    KEYCODE_VOLUME_DOWN: 25
    KEYCODE_MENU: 82
    '''
    keycode_list = [4, 24, 25, 82]
    selected_key = random.choice(keycode_list)
    try:
        driver.press_keycode(selected_key)
        logging.info(form_string("{~}", "event {}:".format(i), "system", "keycode:", str(selected_key)))
        print(form_string("{~}", "event {}:".format(i), "system", "keycode:", str(selected_key)))
        appium_command.append("driver.press_keycode({})".format(selected_key))
    except Exception:
        print(form_string("{w}", "event {}:".format(i), "system", "Something went wrong when press", str(selected_key)))
        logging.error(form_string("{w}", "event {}:".format(i), "system", "Something went wrong when press", str(selected_key)))
