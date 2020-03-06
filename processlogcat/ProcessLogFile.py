import os
import re

keywords = {
               'find elemnt': 'find element command using',
               'click': 'Click element command',
               'send text': 'send keys to element command',
               'scroll': 'JSON Payload',
               'pinch/zoom': '/touch/multi/perform',
               'keycode': 'Calling PressKeyCode',
               'get_page_source': '/source'
    }

driver_pinch = "width = driver.get_window_size()['width']"+"\n"+"height = driver.get_window_size()['height']"+"\n"+"action1 = TouchAction(driver).press(el=None, x=width * 0.2, y=height * 0.2).wait(1000).move_to(el=None,x=width * 0.4,y=height * 0.4).release()"+"\n"+"action2 = TouchAction(driver).press(el=None, x=width * 0.8, y=height * 0.8).wait(1000).move_to(el=None,x=width * 0.6,y=height * 0.6).release()"+"\n"+"pinch_action = MultiAction(driver)"+"\n"+"pinch_action.add(action1, action2)"+"\n"+"pinch_action.perform()"
driver_zoom = "width = driver.get_window_size()['width']"+"\n"+"height = driver.get_window_size()['height']"+"\n"+"action1 = TouchAction(driver).press(el=None, x=width * 0.4, y=height * 0.4).wait(1000).move_to(el=None,x=width * 0.2,y=height * 0.2).release()"+"\n"+"action2 = TouchAction(driver).press(el=None, x=width * 0.6, y=height * 0.6).wait(1000).move_to(el=None,x=width * 0.8,y=height * 0.8).release()"+"\n"+"pinch_action = MultiAction(driver)"+"\n"+"pinch_action.add(action1, action2)"+"\n"+"pinch_action.perform()"


def check_whether_trigger_native(file, out_file):
    trigger_native_APIs = []
    page_source = ""
    with open(out_file, 'w', encoding='utf-8') as of:
        with open(file, 'r', encoding='utf-8') as f:
            line = f.readline().strip('\n')
            while line:
                if 'TARGET API FOUND' in line:
                    trigger_native_APIs.append(line)
                    line = f.readline()
                    while line and re.match(r"channel read: GET .*?/source", line) is None:
                        if 'TARGET API FOUND' in line:
                            trigger_native_APIs.append(line)
                        line = f.readline().strip("\n")

                    while line and "AppiumResponse" not in line:
                        line = f.readline().strip("\n")
                    page_source = line
                    return trigger_native_APIs, page_source
                else:
                    of.write(line + "\n")
                    line = f.readline().strip("\n")
    return trigger_native_APIs, page_source


def filter_adblogfile(file, out_file):
    with open(out_file, 'w', encoding='utf-8') as of:
        with open(file, 'r', encoding='utf-8') as f:
            line = f.readline().strip('\n')
            while line:
                line = f.readline().strip('\n')
                for keyword in keywords.values():
                    if keyword in line:
                        of.write(line+'\n')
                        break


def check_line(resource_id, line, raw_command):
    if keywords['find elemnt'] in line:
        pattern = re.compile(r".*?selector ('.*?').*?")
        resource_id = pattern.match(line)[1]
        return resource_id
    elif keywords['click'] in line:
        raw_command.append("driver.find_element_by_id({}).click()".format(resource_id))
    elif keywords['send text'] in line:
        raw_command.append("driver.find_element_by_id({}).send_keys".format(resource_id))
    elif keywords['scroll'] in line:
        raw_command.append("driver.swipe")
    elif keywords['pinch/zoom'] in line:
        raw_command.append("multi_perform")
    elif keywords['keycode'] in line:
        raw_command.append("driver.press_keycode")
    elif keywords['get_page_source'] in line:
        raw_command.append("sleep(2)")
    else:
        pass


def transfer_log_to_raw_command(filter_adblog):
    raw_command = []
    resource_id = ''
    with open(filter_adblog) as f:
        line = f.readline().strip('\n')
        resource_id = check_line(resource_id, line, raw_command)
        while line:
            line = f.readline().strip('\n')
            resource_id = check_line(resource_id, line, raw_command)
        return raw_command


def check_and_complete_test(raw_command, appium_command, native_APIs, page_source, i):
    print(raw_command)
    if len(native_APIs) == 0:
        with open('tests/test/test{}.txt'.format(i), "w") as of:
            of.write("test:"+"\n")
            for i in range(len(raw_command)):
                    if raw_command[i] in appium_command[i]:
                        if appium_command[i] == 'driver.multi_perform_pinch()':
                            of.write(driver_pinch+"\n")
                        elif appium_command[i] == 'driver.multi_perform_zoom()':
                            of.write(driver_zoom+"\n")
                        else:
                            of.write(appium_command[i]+"\n")
                    else:
                        of.write("error")
                        break
    else:
        with open('tests/ctest/test{}.txt'.format(i), "w") as of:
            of.write("test:" + "\n")
            for i in range(len(raw_command)):
                    if raw_command[i] in appium_command[i]:
                        if appium_command[i] == 'driver.multi_perform_pinch()':
                            of.write(driver_pinch+"\n")
                        elif appium_command[i] == 'driver.multi_perform_zoom()':
                            of.write(driver_zoom+"\n")
                        else:
                            of.write(appium_command[i]+"\n")
                    else:
                        of.write("error")
                        break
            of.write("native_APIs:"+"\n")
            for native_API in native_APIs:
                of.write(native_API + "\n")
            of.write("page_source:"+"\n" + page_source)


def generate_test(appium_command, i):
    native_APIs, page_source = check_whether_trigger_native('log/adb.log', 'log/test.log')
    filter_adblogfile('log/test.log', 'log/filter_adb.log')
    raw_command = transfer_log_to_raw_command('log/filter_adb.log')
    check_and_complete_test(raw_command, appium_command, native_APIs, page_source, i)
    os.remove('log/test.log')
    os.remove('log/filter_adb.log')


if __name__ == '__main__':
    native, page = check_whether_trigger_native('log/adb.log', 'log/out.log')
