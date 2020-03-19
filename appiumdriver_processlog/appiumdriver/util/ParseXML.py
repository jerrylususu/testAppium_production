import xml.etree.cElementTree as ET


def parseXml(page_source):
    # root
    root = ET.fromstring(page_source)

    # find executable elements
    checkable = root.findall(".//*[@checkable='true']")
    checked = root.findall(".//*[@checked='true']")
    clickable = root.findall(".//*[@clickable='true']")
    focused = root.findall(".//*[@focused='true']")
    scrollable = root.findall(".//*[@scrollable='true']")

    click_elements = set(checkable+checked+clickable)
    for element in click_elements:
        element.set('operation', 'click')

    send_text_elements = set(focused)
    for element in send_text_elements:
        element.set('operation', 'send_text')

    scrollable_elements = set(scrollable)
    for element in scrollable_elements:
        element.set('operation', 'scroll')

    # executable elements
    executable_elements = list(click_elements.union(send_text_elements, scrollable_elements))
    return executable_elements
