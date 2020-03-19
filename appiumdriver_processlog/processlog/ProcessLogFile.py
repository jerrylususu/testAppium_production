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
        while "AppiumResponse" not in line:
            line = f.readline()
        if "AppiumResponse" in line:
            if "\"value\":null" in line:
                raw_command.append("driver.find_element_by_id({}).click()".format(resource_id))
    elif keywords['send text'] in line:
        while "AppiumResponse" not in line:
            line = f.readline()
        if "AppiumResponse" in line:
            if "\"value\":null" in line:
                raw_command.append("driver.find_element_by_id({}).send_keys".format(resource_id))
    elif keywords['scroll'] in line:
        while "AppiumResponse" not in line:
            line = f.readline()
        if "AppiumResponse" in line:
            if "\"value\":null" in line:
                raw_command.append("driver.swipe")
    elif keywords['pinch/zoom'] in line:
        while "AppiumResponse" not in line:
            line = f.readline()
        if "AppiumResponse" in line:
            if "\"value\":null" in line:
                raw_command.append("multi_perform")
    elif keywords['keycode'] in line:
        while "AppiumResponse" not in line:
            line = f.readline()
        if "AppiumResponse" in line:
            if "\"value\":null" in line:
                raw_command.append("driver.press_keycode")
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


def transfer_log_to_raw_command(adblog, trigger_native_APIs):
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
                if len(test_trigger_native_APIs-trigger_native_APIs) != 0:
                    comp_test.append((raw_command, test_trigger_native_APIs))
                trigger_native_APIs = trigger_native_APIs | test_trigger_native_APIs
                test_trigger_native_APIs = set()

            resource_id = check_line(resource_id, line, raw_command, f)
            line = f.readline().strip('\n')
        return comp_test, raw_command


def check_and_complete_test(complete_command, appium_command, i):
    with open('tests/test/test_{}.txt'.format(i), "w", encoding='utf-8') as of:
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


def check_and_complete_comp_test(comp_test, complete_command, appium_command, i):
    with open('tests/ctest/ctest_{}.txt'.format(i), "w", encoding='utf-8') as f:
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


def generate_test(appium_command, i, trigger_native_APIs):
    comp_test, complete_command = transfer_log_to_raw_command('log/adb.log', trigger_native_APIs)
    print(complete_command)
    if comp_test:
        check_and_complete_comp_test(comp_test, complete_command, appium_command, i)
    else:
        check_and_complete_test(complete_command, appium_command, i)


if __name__ == '__main__':
    # appium_command = ['sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/discovery_cover').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/advanced_search').click()", 'sleep(2)', "driver.find_element_by_id('android:id/title').click()", 'sleep(2)', 'driver.press_keycode', 'sleep(2)', 'driver.press_keycode', 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/imgvCover').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/butSubscribe').click()", 'sleep(2)', 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/butShowSettings').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/icon_frame').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/icon_frame').click()", 'sleep(2)', "driver.find_element_by_id('android:id/title').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/icon_frame').click()", 'sleep(2)', 'driver.press_keycode', 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/container').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/butAction2').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/txtvPodcastTitle').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/butPlaybackSpeed').click()", 'sleep(2)', "driver.swipe_up('aaa')", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/butPlay').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/page_indicator').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/set_sleeptimer_item').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/setSleeptimerButton').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/disableSleeptimerButton').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/cbShakeToReset').click()", 'sleep(2)', 'driver.press_keycode', 'sleep(2)', 'driver.press_keycode', 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/butSkip').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/container').click()", 'sleep(2)', 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/butAction2').click()", 'sleep(2)', 'sleep(2)', 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/audio_controls').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/skipSilence').click()", 'sleep(2)', "driver.find_element_by_id('android:id/button1').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/add_to_favorites_item').click()", 'sleep(2)', 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/butSkip').click()", 'sleep(2)', 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/refresh_item').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/secondaryActionButton').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/butShowInfo').click()", 'sleep(2)', "driver.find_element_by_id('de.danoeh.antennapod:id/visit_website_item').click()", 'sleep(2)', 'driver.press_keycode', 'sleep(2)']
    # generate_test(appium_command, 2)
    comp_test, raw_command = transfer_log_to_raw_command('log/adb.log', set())
    print(comp_test)
    print(raw_command)
