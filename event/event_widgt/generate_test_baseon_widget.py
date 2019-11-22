import random
import string

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

import parseXML
def random_generate_test_baseon_widget(driver, element_dict):
    print(type(element_dict))
    assert isinstance(element_dict, dict)
    attrs = []
    for key in element_dict.keys():
        if(len(element_dict[key]) != 0):
            attrs.append(key)
    select_attr = random.choice(attrs)

    # 随机选择可选中控件
    if(select_attr == "checkable"):
        elements = element_dict.get("checkable")
        resource_id = random.choice(elements)
        select_element = driver.find_element_by_id(resource_id)
        select_element.click()

    # 随机选择可点击控件
    elif(select_attr == "clickable"):
        elements = element_dict.get("clickable")
        resource_id = random.choice(elements)
        select_element = driver.find_element_by_id(resource_id)
        select_element.click()

    # 随机选择可获得焦点控件
    elif(select_attr == "focusable"):
        elements = element_dict.get("focusable")
        resource_id = random.choice(elements)
        select_element = driver.find_element_by_id(resource_id)
        select_element.click()
        assert isinstance(select_element, webdriver.webelement.WebElement)
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        select_element.send_keys(ran_str)

    # 随机选择已经获得焦点的控件
    elif(select_attr == "focused"):
        elements = element_dict.get("focusable")
        resource_id = random.choice(elements)
        select_element = driver.find_element_by_id(resource_id)
        assert isinstance(select_element, webdriver.webelement.WebElement)
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        select_element.send_keys(ran_str)

    # 随机选择可滑动控件
    elif(select_attr == "scrollable"):
        elements = element_dict.get("scrollable")
        resource_id = random.choice(elements)
        select_element = driver.find_element_by_id(resource_id)
        assert isinstance(select_element, webdriver.webelement.WebElement)
        assert isinstance(driver, webdriver.webdriver.WebDriver)
        element_size_width = select_element.size['width']
        element_size_height = select_element.size['height']
        element_location_x = select_element.location['x']
        element_location_y = select_element.location['y']
        direction = ["left", "right", "up", "down"]
        select_direction = random.choice(direction)
        # 向左划
        if(select_direction == "left"):
            driver.swipe(element_location_x, element_location_y+element_size_height/2,
                         element_location_x+element_size_width, element_location_y+element_size_height/2, 1000)
        # 向右划
        elif(select_direction == "right"):
            driver.swipe(element_location_x + element_size_width, element_location_y + element_size_height / 2,
                         element_location_x, element_location_y + element_size_height / 2, 1000)
        # 向上划
        elif(select_direction == "up"):
            driver.swipe(element_location_x+element_size_width/2, element_location_y+element_size_height,
                         element_location_x+element_size_width/2, element_location_y, 1000)

        # 向下划
        elif (select_direction == "up"):
            driver.swipe(element_location_x + element_size_width / 2, element_location_y,
                         element_location_x + element_size_width / 2, element_location_y + element_size_height, 1000)

    # 随机选择可长按控件
    elif(select_attr == "long-clickable"):
        elements = element_dict.get("focused")
        resource_id = random.choice(elements)
        select_element = driver.find_element_by_id(resource_id)
        assert isinstance(select_element, webdriver.webelement.WebElement)
        # select_element
        TouchAction(driver).long_press(select_element).perform()
        TouchAction(driver).long_press()


def random_test(driver, page_source):
    element_dict = parseXML.parseXml(page_source)
    random_generate_test_baseon_widget(driver, element_dict)

if __name__ == "__main__":
    pass


#TODO 问题1 解析xml的时候怎么没有resource_id 是空呢 看一下 uiautomator 出了什么问题？
#TODO 问题1 解答1：因为当他有两个子节点的时候， 子节点是有resource-id 的，但是不可点击， 父节点可以点击但是没有 resource_id 这时候用孩子节点的
#TODO 来代替父节点的 解决2：因为可以根据获取该父控件的屏幕坐标屏幕坐标，但是这个在不同的手机上是要进行坐标转化的