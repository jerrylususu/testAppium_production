# TODO 处理两个logfile 直接得到一个命令的序列即一个test（test的最后要拿到page source 便于比较）
# TODO 把所有的test cases 都输出包括有触发的和没有触发的
import re

keywords = {
               'find elemnt': 'find element command using',
               'click': 'Click element command',
               'send text': 'send keys to element command',
               'scroll': 'JSON Payload',
               'pinch/zoom': '/touch/multi/perform',
               'keycode': 'Calling PressKeyCode',
               'target API': 'TARGET API FOUND'
    }

driver_pinch = "width = driver.get_window_size()['width']"+"\n"+"height = driver.get_window_size()['height']"+"\n"+"action1 = TouchAction(driver).press(el=None, x=width * 0.2, y=height * 0.2).wait(1000).move_to(el=None,x=width * 0.4,y=height * 0.4).release()"+"\n"+"action2 = TouchAction(driver).press(el=None, x=width * 0.8, y=height * 0.8).wait(1000).move_to(el=None,x=width * 0.6,y=height * 0.6).release()"+"\n"+"pinch_action = MultiAction(driver)"+"\n"+"pinch_action.add(action1, action2)"+"\n"+"pinch_action.perform()"
driver_zoom = "width = driver.get_window_size()['width']"+"\n"+"height = driver.get_window_size()['height']"+"\n"+"action1 = TouchAction(driver).press(el=None, x=width * 0.4, y=height * 0.4).wait(1000).move_to(el=None,x=width * 0.2,y=height * 0.2).release()"+"\n"+"action2 = TouchAction(driver).press(el=None, x=width * 0.6, y=height * 0.6).wait(1000).move_to(el=None,x=width * 0.8,y=height * 0.8).release()"+"\n"+"pinch_action = MultiAction(driver)"+"\n"+"pinch_action.add(action1, action2)"+"\n"+"pinch_action.perform()"

def filter_adblogfile(file, out_file):
    with open(out_file, 'w') as of:
        with open(file, 'r') as f:
            line = f.readline().strip('\n')
            while line:
                line = f.readline().strip('\n')
                for keyword in keywords.values():
                    if keyword in line:
                        if keyword == 'TARGET API FOUND':
                            return
                        else:
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
        raw_command.append("driver.find_element_by_id({}).send_keys()".format(resource_id))
    elif keywords['scroll'] in line:
        raw_command.append("driver.swipe()")
    elif keywords['pinch/zoom'] in line:
        raw_command.append("multi_perform")
    elif keywords['keycode'] in line:
        raw_command.append("driver.press_keycode")
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


def check_and_complete_test(raw_command, appium_command, outfilepath):
    print(raw_command)
    with open(outfilepath, "w") as of:
        for i in range(len(raw_command)):
                if raw_command[i] in appium_command[i]:
                    if appium_command == 'driver.multi_perform_pinch()':
                        of.write(driver_pinch+"\n")
                    elif appium_command == 'driver.multi_perform_zoom()':
                        of.write(driver_zoom+"\n")
                    else:
                        of.write(appium_command[i]+"\n")
                else:
                    of.write("error")
                    break


def generate_test(adblog, appium_command, outfile):
    # TODO
    filter_adblogfile(adblog, 'log/filter_adblog.log')
    raw_command = transfer_log_to_raw_command('log/filter_adblog.log')
    check_and_complete_test(raw_command, appium_command, outfile)


if __name__ == '__main__':
    # TODO
    appium_command = []
    generate_test('log/adblog.log', appium_command, 'test/testcase.txt')
