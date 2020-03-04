import random
import string

from util.ProcessText import form_string


def generate_test_base_on_widget(driver, executable_elements, logging, i, appium_command):
    if len(executable_elements) == 0:
        print(form_string("widget", "There is no executable element"))
        logging.warning((form_string("widget", "There is no executable element")))
        return 0
    else:
        selected_ele = random.choice(executable_elements)
        resource_id = selected_ele.get('resource-id')
        if resource_id == '':
            try:
                for node in selected_ele.iter():
                    if node.get('resource-id') != '':
                        resource_id = node.get('resource-id')
                        print(form_string("widget", "use resource-id of its child node"))
                        logging.warning(form_string("widget", "use resource-id of its child node"))
                        break
            except Exception:
                print(form_string("widget",
                                  "Something went wrong when using resource-id of its child node"))
                logging.error(form_string("widget",
                                          "Something went wrong when using resource-id of its child node"))

        if resource_id != '':
            try:
                select_element = driver.find_element_by_id(resource_id)
                event = selected_ele.get('operation')

                # click
                if event == 'click':
                    try:
                        select_element.click()
                        logging.info(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                                 "click"))
                        print(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:", "click"))
                        appium_command.append("driver.find_element_by_id('{}').click()".format(resource_id))
                        return 1
                    except Exception:
                        logging.error(form_string("event {}:".format(i), "widget", "Something went wrong when click",
                                                  resource_id))
                        print(form_string("event {}:".format(i), "widget", "Something went wrong when click", resource_id))
                        return 0

                # send text
                elif event == 'send_text':
                    random_text = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1, 10)))
                    try:
                        select_element.send_keys(random_text)
                        logging.info(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                                 "send text", "text:", random_text))
                        print(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                          "send text", "text:", random_text))
                        appium_command.append("driver.find_element_by_id('{}').send_keys('{}')".format(resource_id, random_text))
                        return 1
                    except Exception:
                        logging.error(form_string("event {}:".format(i), "widget", "Something went wrong when send",
                                                  random_text, "to", resource_id))
                        print(form_string("event {}:".format(i), "widget", "Something went wrong when send", random_text,
                                          "to", resource_id))
                        return 0
                # scroll
                elif event == 'scroll':
                    element_size_width = select_element.size['width']
                    element_size_height = select_element.size['height']
                    element_location_x = select_element.location['x']
                    element_location_y = select_element.location['y']
                    direction = ["left", "right", "up"]
                    select_direction = random.choice(direction)
                    # left scroll
                    if select_direction == "left":
                        try:
                            driver.swipe(element_location_x+element_size_width*(1/4), element_location_y+element_size_height/2,
                                         element_location_x+element_size_width*(3/4), element_location_y+element_size_height/2, 1000)
                            logging.info(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                                     "left scroll"))
                            print(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                              "left scroll"))
                            appium_command.append("driver.swipe({}, {}, {}, {}, {})".format(element_location_x+element_size_width*(1/4),
                                element_location_y + element_size_height/2, element_location_x+element_size_width*(3/4),
                                                                        element_location_y+element_size_height/2, 1000))
                            return 1
                        except Exception:
                            logging.error(form_string("event {}:".format(i), "widget", "Something went wrong when left scroll",
                                                      resource_id))
                            print(form_string("event {}:".format(i), "widget", "Something went wrong when left scroll",
                                              resource_id))
                            return 0
                    # right scroll
                    elif select_direction == "right":
                        try:
                            driver.swipe(element_location_x + element_size_width*(3/4), element_location_y + element_size_height/2,
                                         element_location_x + element_size_width*(1/4), element_location_y + element_size_height/2, 1000)
                            logging.info(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                         "right scroll"))
                            print(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                              "right scroll"))
                            appium_command.append("driver.swipe({}, {}, {}, {}, {})".format(element_location_x + element_size_width*(3/4),
                                        element_location_y + element_size_height/2, element_location_x + element_size_width*(1/4),
                                                                            element_location_y + element_size_height/2, 1000))
                            return 1
                        except Exception:
                            logging.error(form_string("event {}:".format(i), "widget", "Something went wrong when right scroll",
                                                      resource_id))
                            print(form_string("event {}:".format(i), "widget", "Something went wrong when right scroll",
                                              resource_id))
                            return 0
                    # left scroll
                    elif select_direction == "up":
                        try:
                            driver.swipe(element_location_x+element_size_width/2, element_location_y+element_size_height*(3/4),
                                         element_location_x+element_size_width/2, element_location_y+element_size_height*(1/4), 1000)
                            logging.info(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                                     "up scroll"))
                            print(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                              "up scroll"))
                            appium_command.append("driver.swipe({}, {}, {}, {}, {})".format(element_location_x+element_size_width/2,
                                                                                            element_location_y+element_size_height*(3/4),
                                         element_location_x+element_size_width/2, element_location_y+element_size_height*(1/4), 1000))
                            return 1
                        except Exception:
                            logging.error(form_string("event {}:".format(i), "widget", "Something went wrong when up scroll",
                                                      resource_id))
                            print(form_string("event {}:".format(i), "widget", "Something went wrong when up scroll",
                                              resource_id))
                            return 0
                    # down scroll
                    elif select_direction == "down":
                        try:
                            driver.swipe(element_location_x + element_size_width/2, element_location_y+element_size_height*(1/4),
                                         element_location_x + element_size_width/2, element_location_y+element_size_height*(3/4), 1000)
                            logging.info(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                         "down scroll"))
                            print(form_string("event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                              "down scroll"))
                            appium_command.append("driver.swipe({}, {}, {}, {}, {})".format(element_location_x + element_size_width/2,
                                                                                            element_location_y+element_size_height*(1/4),
                                         element_location_x + element_size_width/2, element_location_y+element_size_height*(3/4), 1000))
                            return 1
                        except Exception:
                            logging.error(form_string("event {}:".format(i), "widget", "Something went wrong when down scroll",
                                                      resource_id))
                            print(form_string("event {}:".format(i), "widget", "Something went wrong when down scroll",
                                              resource_id))
                            return 0
            except Exception:
                print(form_string("widget", "Can not find element by", resource_id))
                logging.error(form_string("widget", "Can not find element by", resource_id))
                return 0

        else:
            print(form_string("widget", "resource-id is null"))
            logging.warning(form_string("widget", "resource-id is null"))
            return 0
