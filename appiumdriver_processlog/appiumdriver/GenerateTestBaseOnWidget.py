import random
import string

import base64

from appiumdriver_processlog.appiumdriver.util.ProcessText import form_string


def generate_test_base_on_widget(driver, executable_elements, logging, i, appium_command, widgets, **kwargs):
    if len(executable_elements) == 0:
        print("{w} There is no executable element")
        logging.warning("{w} There is no executable element")
    else:
        selected_ele = random.choice(executable_elements)
        resource_id = selected_ele.get('resource-id')

        print(form_string("{~}", "resource-id is", str(resource_id)))
        logging.info(form_string("{~}", "resource-id is", str(resource_id)))

        widgets.add(resource_id)
        if resource_id is None or resource_id == '':
            try:
                for node in selected_ele.iter():
                    if node.get('resource-id') is not None:
                        resource_id = node.get('resource-id')
                        print(form_string("{w} use resource-id of its child node", str(resource_id)))
                        logging.warning(form_string("{w} use resource-id of its child node", str(resource_id)))
                        break
            except Exception:
                print(form_string("{w} Something went wrong when using resource-id of its child node"))
                logging.error(form_string("{w} Something went wrong when using resource-id of its child node"))

        if resource_id is not None and resource_id != '':
            try:
                select_element = driver.find_element_by_id(resource_id)
                event = selected_ele.get('operation')

                # click
                if event == 'click':
                    try:
                        select_element.click()
                        logging.info(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                                 "click"))
                        print(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:", "click"))
                        appium_command.append("driver.find_element_by_id('{}').click()".format(resource_id))
                    except Exception:
                        logging.exception()
                        logging.error(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when click",
                                                  resource_id))
                        print(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when click", resource_id))

                # send text
                elif event == 'send_text':
                    random_text = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1, 10)))
                    try:
                        select_element.send_keys(random_text)
                        logging.info(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                                 "send text", "text:", random_text))
                        print(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                          "send text", "text:", random_text))
                        appium_command.append("driver.find_element_by_id('{}').send_keys('{}')".format(resource_id, random_text))
                    except Exception:
                        logging.error(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when send",
                                                  random_text, "to", resource_id))
                        print(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when send", random_text,
                                          "to", resource_id))
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
                            logging.info(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                                     "left scroll"))
                            print(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                              "left scroll"))
                            appium_command.append("driver.swipe_left('{}')".format(resource_id))
                        except Exception:
                            logging.error(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when left scroll",
                                                      resource_id))
                            print(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when left scroll",
                                              resource_id))
                    # right scroll
                    elif select_direction == "right":
                        try:
                            driver.swipe(element_location_x + element_size_width*(3/4), element_location_y + element_size_height/2,
                                         element_location_x + element_size_width*(1/4), element_location_y + element_size_height/2, 1000)
                            logging.info(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                         "right scroll"))
                            print(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                              "right scroll"))
                            appium_command.append("driver.swipe_right('{}')".format(resource_id))
                        except Exception:
                            logging.error(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when right scroll",
                                                      resource_id))
                            print(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when right scroll",
                                              resource_id))
                    # left scroll
                    elif select_direction == "up":
                        try:
                            driver.swipe(element_location_x+element_size_width/2, element_location_y+element_size_height*(3/4),
                                         element_location_x+element_size_width/2, element_location_y+element_size_height*(1/4), 1000)
                            logging.info(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                                     "up scroll"))
                            print(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                              "up scroll"))
                            appium_command.append("driver.swipe_up('{}')".format(resource_id))
                        except Exception:
                            logging.error(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when up scroll",
                                                      resource_id))
                            print(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when up scroll",
                                              resource_id))
                    # down scroll
                    elif select_direction == "down":
                        try:
                            driver.swipe(element_location_x + element_size_width/2, element_location_y+element_size_height*(1/4),
                                         element_location_x + element_size_width/2, element_location_y+element_size_height*(3/4), 1000)
                            logging.info(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                         "down scroll"))
                            print(form_string("{~}", "event {}:".format(i), "widget", "resource_id:", resource_id, "operation:",
                                              "down scroll"))
                            appium_command.append("driver.swipe_down('{}')".format(resource_id))
                        except Exception:
                            logging.error(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when down scroll",
                                                      resource_id))
                            print(form_string("{w}", "event {}:".format(i), "widget", "Something went wrong when down scroll",
                                              resource_id))
            except Exception:
                print(form_string("{w}", "Can not find element by", str(resource_id)))
                logging.error(form_string("{w}", "Can not find element by", str(resource_id)))

        else:
            print(form_string("{w} resource-id is still None"))
            logging.warning(form_string("{w} resource-id is still None"))
