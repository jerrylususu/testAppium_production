import copy
import re

keywords = {
               'find elemnt': 'Find element command',
               'click': 'Click element command',
               'send text': 'send keys to element command',
               'scroll': 'JSON Payload',
               'pinch/zoom': '/touch/multi/perform',
               'keycode': 'Calling PressKeyCode',
               'get_page_source': '/source'
    }

driver_pinch = "width = driver.get_window_size()['width']"+"\n"+"height = driver.get_window_size()['height']"+"\n"+"action1 = TouchAction(driver).press(el=None, x=width * 0.2, y=height * 0.2).wait(1000).move_to(el=None,x=width * 0.4,y=height * 0.4).release()"+"\n"+"action2 = TouchAction(driver).press(el=None, x=width * 0.8, y=height * 0.8).wait(1000).move_to(el=None,x=width * 0.6,y=height * 0.6).release()"+"\n"+"pinch_action = MultiAction(driver)"+"\n"+"pinch_action.add(action1, action2)"+"\n"+"pinch_action.perform()"
driver_zoom = "width = driver.get_window_size()['width']"+"\n"+"height = driver.get_window_size()['height']"+"\n"+"action1 = TouchAction(driver).press(el=None, x=width * 0.4, y=height * 0.4).wait(1000).move_to(el=None,x=width * 0.2,y=height * 0.2).release()"+"\n"+"action2 = TouchAction(driver).press(el=None, x=width * 0.6, y=height * 0.6).wait(1000).move_to(el=None,x=width * 0.8,y=height * 0.8).release()"+"\n"+"pinch_action = MultiAction(driver)"+"\n"+"pinch_action.add(action1, action2)"+"\n"+"pinch_action.perform()"


def complete_swipe_command(raw_command):
    match = re.match(r"driver.swipe_(.*?)[(](.*?)[)]", raw_command)
    direction = match[1]
    resource_id = match[2]
    find_element = "select_element = driver.find_element_by_id({})\n".format(resource_id)
    get_size = "element_size_width = select_element.size['width']\nelement_size_height = select_element.size['height']\nelement_location_x = select_element.location['x']\nelement_location_y = select_element.location['y']\n"
    if direction == 'left':
        swipe = "driver.swipe(element_location_x+element_size_width*(1/4), element_location_y+element_size_height/2,element_location_x+element_size_width*(3/4), element_location_y+element_size_height/2, 1000)"
    elif direction == 'right':
        swipe = "driver.swipe(element_location_x + element_size_width*(3/4), element_location_y + element_size_height/2,element_location_x + element_size_width*(1/4), element_location_y + element_size_height/2, 1000)"
    elif direction == 'up':
        swipe = "driver.swipe(element_location_x+element_size_width/2, element_location_y+element_size_height*(3/4),element_location_x+element_size_width/2, element_location_y+element_size_height*(1/4), 1000)"
    else:
        swipe = "driver.swipe(element_location_x + element_size_width/2, element_location_y+element_size_height*(1/4),element_location_x + element_size_width/2, element_location_y+element_size_height*(3/4), 1000)"
    complete_command = find_element + get_size + swipe
    return complete_command


def check_line(resource_id, line, raw_command, f):
    if keywords['find elemnt'] in line:
        pattern = re.compile(r".*?selector ('.*?').*?")
        resource_id = pattern.match(line)[1]
    elif keywords['click'] in line:
        line_num = f.tell()
        while "AppiumResponse" not in line:
            line = f.readline()
        if "AppiumResponse" in line:
            if "\"value\":null" in line:
                raw_command.append("driver.find_element_by_id({}).click()".format(resource_id))
        f.seek(line_num)
    elif keywords['send text'] in line:
        line_num = f.tell()
        while "AppiumResponse" not in line:
            line = f.readline()
        if "AppiumResponse" in line:
            if "\"value\":null" in line:
                raw_command.append("driver.find_element_by_id({}).send_keys".format(resource_id))
        f.seek(line_num)
    elif keywords['scroll'] in line:
        line_num = f.tell()
        while "AppiumResponse" not in line:
            line = f.readline()
        if "AppiumResponse" in line:
            if "\"value\":null" in line:
                raw_command.append("driver.swipe")
        f.seek(line_num)
    elif keywords['pinch/zoom'] in line:
        line_num = f.tell()
        while "AppiumResponse" not in line:
            line = f.readline()
        if "AppiumResponse" in line:
            if "\"value\":null" in line:
                raw_command.append("multi_perform")
        f.seek(line_num)
    elif keywords['keycode'] in line:
        line_num = f.tell()
        while "AppiumResponse" not in line:
            line = f.readline()
        if "AppiumResponse" in line:
            if "\"value\":null" in line:
                raw_command.append("driver.press_keycode")
        f.seek(line_num)
    elif keywords['get_page_source'] in line:
        raw_command.append("sleep")
    else:
        pass
    return resource_id


def check_line_operation(line):
    if keywords['click'] in line or keywords['send text'] in line or keywords['scroll'] in line or keywords['pinch/zoom'] \
            in line or keywords['keycode'] in line:
        return True
    else:
        return False


def transfer_log_to_raw_command(adblog, trigger_target_APIs):
    trigger_target_APIs_one_test = set()
    comp_test = []
    raw_command = []
    test_trigger_native_APIs = set()
    resource_id = ''
    with open(adblog, 'r', encoding='utf-8') as f:
        line = f.readline().strip('\n')
        while line:
            match = re.match(r".*?TARGET API FOUND&(.*?)$", line)
            if match is not None:
                while line and not check_line_operation(line):
                    match = re.match(r".*?TARGET API FOUND&(.*?)$", line)
                    if match is not None:
                        API = match[1]
                        test_trigger_native_APIs.add(API)
                    else:
                        resource_id = check_line(resource_id, line, raw_command, f)
                    line = f.readline().strip("\n")
                if len(test_trigger_native_APIs-trigger_target_APIs_one_test) != 0:
                    tmp_command = copy.deepcopy(raw_command)
                    comp_test.append((tmp_command, test_trigger_native_APIs))
                trigger_target_APIs_one_test = trigger_target_APIs_one_test | test_trigger_native_APIs
                test_trigger_native_APIs = set()

            resource_id = check_line(resource_id, line, raw_command, f)
            line = f.readline().strip('\n')
        
        trigger_target_APIs.update(trigger_target_APIs_one_test)
        # this is a bug...
        # trigger_target_APIs = trigger_target_APIs | trigger_target_APIs_one_test
        return comp_test, raw_command


def check_and_complete_test(complete_command, appium_command, i, apk_name=""):
    with open(f'tests/test/{apk_name}_test_{i}.txt', "w", encoding='utf-8') as of:
        of.write("complete_test:"+"\n")
        for k in range(len(complete_command)):
                if complete_command[k] in appium_command[k]:
                    if appium_command[k] == 'driver.multi_perform_pinch()':
                        of.write(driver_pinch+"\n")
                    elif appium_command[k] == 'driver.multi_perform_zoom()':
                        of.write(driver_zoom+"\n")
                    elif complete_command[k] == 'driver.swipe':
                        swipe_command = complete_swipe_command(appium_command[k])
                        of.write(swipe_command+"\n")
                    else:
                        of.write(appium_command[k]+"\n")
                else:
                    of.write("error")
                    break


def check_and_complete_comp_test(comp_test, complete_command, appium_command, i, apk_name=""):
    with open(f'tests/ctest/{apk_name}_ctest_{i}.txt', "w", encoding='utf-8') as f:
        for j in range(len(comp_test)):
            raw_command = comp_test[j][0]
            native_APIs = comp_test[j][1]
            f.write("test{}:".format(j)+"\n")
            for k in range(len(raw_command)):
                if raw_command[k] in appium_command[k]:
                    if appium_command[k] == 'driver.multi_perform_pinch()':
                        f.write(driver_pinch + "\n")
                    elif appium_command[k] == 'driver.multi_perform_zoom()':
                        f.write(driver_zoom + "\n")
                    elif complete_command[k] == 'driver.swipe':
                        swipe_command = complete_swipe_command(appium_command[k])
                        f.write(swipe_command+"\n")
                    else:
                        f.write(appium_command[k] + "\n")
                else:
                    f.write("error")
                    break
            f.write("native_APIs:"+"\n")
            for native_API in native_APIs:
                f.write(native_API + "\n")
            f.write("\n")

        f.write("complete_test:" + "\n")
        for k in range(len(complete_command)):
            if complete_command[k] in appium_command[k]:
                if appium_command[k] == 'driver.multi_perform_pinch()':
                    f.write(driver_pinch + "\n")
                elif appium_command[k] == 'driver.multi_perform_zoom()':
                    f.write(driver_zoom + "\n")
                elif complete_command[k] == 'driver.swipe':
                    swipe_command = complete_swipe_command(appium_command[k])
                    f.write(swipe_command + "\n")
                else:
                    f.write(appium_command[k] + "\n")
            else:
                f.write("error")
                break


def generate_test(appium_command, i, trigger_target_APIs, apk_name=""):
    comp_test, complete_command = transfer_log_to_raw_command(f'log/{apk_name}_adb{i}.log', trigger_target_APIs)
    print(complete_command)
    if comp_test:
        check_and_complete_comp_test(comp_test, complete_command, appium_command, i, apk_name=apk_name)
    else:
        check_and_complete_test(complete_command, appium_command, i, apk_name=apk_name)


if __name__ == '__main__':
    appium_command = ['sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/butConfirm').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/discovery_cover').click()", 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/txtvDescription').click()", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_icon').click()", 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').send_keys('WQRjut6eL')", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').send_keys('NTRxA6Cm4i')", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').send_keys('ko0D5LyVU7')", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_close_btn').click()", 'sleep(1)', 'sleep(1)', 'sleep(1)', 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').click()", 'sleep(1)', 'sleep(1)', 'sleep(1)', 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').send_keys('TGVHEON')", 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').send_keys('Fu')", 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_close_btn').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').send_keys('4LlyKXnUQ')", 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').send_keys('vkw2Ts1aMW')", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_close_btn').click()", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').send_keys('C')", 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_close_btn').click()", 'sleep(1)', 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').send_keys('i')", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/search_src_text').send_keys('UoWMxy')", 'sleep(1)', 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/discovery_cover').click()", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/etxtFeedurl').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/discovery_cover').click()", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/butConfirm').click()", 'sleep(1)', "driver.find_element_by_id('android:id/button3').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/discovery_cover').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/txtvTitle').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/txtvDescription').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/butSubscribe').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/container').click()", 'sleep(1)', "driver.swipe_right('de.danoeh.antennapod:id/content_root')", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/imgvCover').click()", 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/imgvCover').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/visit_website_item').click()", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/txtvUrl').click()", 'sleep(1)', "driver.swipe_left('de.danoeh.antennapod:id/scrollView')", 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/txtvDetailsAuthor').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/visit_website_item').click()", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/secondaryActionButton').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/container').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/visit_website_item').click()", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/butShowSettings').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/icon_frame').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/icon_frame').click()", 'sleep(1)', "driver.find_element_by_id('android:id/title').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/icon_frame').click()", 'sleep(1)', "driver.find_element_by_id('android:id/switch_widget').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/icon_frame').click()", 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/icon_frame').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/icon_frame').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/icon_frame').click()", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/visit_website_item').click()", 'sleep(1)', 'driver.press_keycode(4)', 'sleep(1)', 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/butAction2').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/txtvEpisodeTitle').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/butRev').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/butSkip').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/container').click()", 'sleep(1)', "driver.find_element_by_id('de.danoeh.antennapod:id/visit_website_item').click()"]
    # generate_test(appium_command, 2)
    comp_test, raw_command = transfer_log_to_raw_command('/Users/a00/Desktop/log/adb2.log', set())
    for t in comp_test:
        print(t)
    print(raw_command)
