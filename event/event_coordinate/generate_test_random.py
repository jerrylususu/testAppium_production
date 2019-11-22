import random
import time

from appium import webdriver
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction

def drag_event(driver):
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    from_x = random.randint(0, width)
    from_y = random.randint(0, height)
    to_x = random.randint(0, width)
    to_y = random.randint(0, height)
    TouchAction(driver).long_press(el=None, x=from_x, y=from_y).move_to(to_x, to_y).release().perform()

def key_event(driver):
    # 3：HOME键
    # 4: 返回键
    # 5：拨号键
    # 6：挂机键
    # 24：音量增加键
    # 25：音量减小键
    # 26：电源键
    # 27：拍照键
    # 80：拍照对焦键
    # 82：菜单键
    # 83：通知键
    # 84：搜索键
    # 91：话筒静音键
    # 164：扬声器静音键
    keycode_list = [3, 4, 5, 6, 24, 25, 26, 27, 80, 82, 83, 84, 91, 164]
    select_keycode = random.choice(keycode_list)
    driver.press_keycode(select_keycode)

def long_press_event(driver):
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    x = random.randint(0, width)
    y = random.randint(0, height)
    TouchAction(driver).long_press(x, y).release().perform()

def long_press_key_event(driver):
    keycode_list = [3, 4, 5, 6, 24, 25, 26, 27, 80, 82, 83, 84, 91, 164]
    select_keycode = random.choice(keycode_list)
    driver.long_press_keycode(select_keycode)

def motion_event(driver):
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    # touch event
    x = random.randint(0, width)
    y = random.randint(0, height)
    TouchAction(driver).press(x, y).release().perform()
    # swipe event
    from_x = random.randint(0, width)
    from_y = random.randint(0, height)
    to_x = random.randint(0, width)
    to_y = random.randint(0, height)
    driver.swipe(from_x, from_y, to_x, to_y)

def pinch_event(driver):
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    # pinch
    action1 = TouchAction(driver).press(width * 0.2, height * 0.2).wait(1000).move_to(width * 0.4,
                                                                                      height * 0.4).release()
    action2 = TouchAction(driver).press(width * 0.8, height * 0.8).wait(1000).move_to(width * 0.6,
                                                                                      height * 0.6).release()
    pinch_action = MultiAction(driver)
    pinch_action.add(action1, action2)
    pinch_action.perform()

def zoom_event(driver):
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    # zoom
    action1 = TouchAction(driver).press(width * 0.4, height * 0.4).wait(1000).move_to(width * 0.2,
                                                                                      height * 0.2).release()
    action2 = TouchAction(driver).press(width * 0.6, height * 0.6).wait(1000).move_to(width * 0.8,
                                                                                      height * 0.8).release()
    pinch_action = MultiAction(driver)
    pinch_action.add(action1, action2)
    pinch_action.perform()

def other_multi_event(driver):
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    # other multi action
    random_action_num = random.randint(2, 6)
    multi_action = MultiAction(driver)
    for i in range(random_action_num):
        from_coordidate = (random.randint(0, width), random.randint(0, height))
        to_coordinate = (random.randint(0, width), random.randint(0, height))
        action = TouchAction(driver).press(from_coordidate[0], from_coordidate[1]). \
            wait(1000).move_to(to_coordinate[0], to_coordinate[1]).release()
        multi_action.add(action)
    multi_action.perform()

def tap_event(driver):
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    x = random.randint(0, width)
    y = random.randint(0, height)
    driver.tap(x, y)

def random_test(driver):
    assert isinstance(driver, webdriver.webdriver.WebDriver)
    event_list = ["drag", "key", "long_press", "long_press key",
                  "motion", "multi_touch", "tap", "throttle"]
    select_event = random.choice(event_list)
    # dragEvent
    if(select_event == "drag"):
        drag_event(driver)
    # keyEvent
    elif(select_event == "key"):
        key_event(driver)
    # longpress Event
    elif(select_event == "long_press"):
        long_press_event(driver)
    # longpress KeyEvent
    elif(select_event == "long_press key"):
        long_press_key_event(driver)
    # motionEvent(touch, swipe)
    elif(select_event == "motion"):
        motion_event(driver)
    # MultiTouchEvent(zoom, pinch)
    elif(select_event == "multi_touch"):
        multi_list = ["zoom", "pinch", "others"]
        select_action = random.choice(multi_list)
        if(select_action == "zoom"):
            zoom_event(driver)
        elif(select_action == "pinch"):
            pinch_event(driver)
        else:
            other_multi_event(driver)
    # TapEvent
    elif(select_event == "tap"):
        tap_event(driver)
    # throttleEvent
    elif(select_event == "throttle"):
        time.sleep(10000)

    # TODO 测试每一个event 功能就可不可以用
    # TODO 看看random的driver 会不会出问题 写一个exception 的类
    # TODO 去github或者别的平台上找一些 app
    # TODO 看看这个random 的driver 的覆盖率怎么样 达到多少

if __name__ == '__main__':
    pass