from xml.dom.minidom import parse
import xml.dom.minidom

def parseXml(page_source):
    # attr_list = ["checked", "checkable", "clickable", "enabled", "focusable", "focused", "scrollable", "long-clickable", "password", "selected"]
    attr_list = ["checkable", "clickable", "focusable", "focused", "scrollable", "long-clickable"]
    attr_true_element_dict = {}
    # page_source = open(file).read()
    DOMTree = xml.dom.minidom.parseString(page_source)
    print("生成DOM tree")
    root = DOMTree.documentElement
    print("根节点为："+root.nodeName)
    queue = []
    queue.append(root)
    level = 1
    print("level " + str(level) + ':' + root.nodeName)
    for attr in attr_list:
        attr_true_element_dict[attr] = []
    while queue:
        level += 1
        parent = queue.pop(0)
        childnodes = parent.childNodes
        for childnode in childnodes:
            assert isinstance(childnode, xml.dom.minidom.Element)
            for attr in attr_list:
                attr_value = getAtrr(childnode, attr)
                if attr_value == "true":
                    resource_id = childnode.getAttribute("resource-id")
                    attr_true_element_dict[attr].append(resource_id)
                    # if(resource_id != ''):
                    #     attr_true_element_dict[attr].append(childnode.getAttribute("resource-id"))
                    # else:
                    #     if(childnode.hasChildNodes()):
                    #         first_childnode = childnode.childNodes[0]
                    #         attr_true_element_dict[attr].append('child'+'-'+first_childnode.getAttribute("resource-id"))
                    #     else:
                    #         attr_true_element_dict[attr].append('bounds'+'-'+childnode.getAttribute("bounds"))
                else:
                    pass
            print("level " + str(level) + ':' + childnode.nodeName)
            queue.append(childnode)
    print(attr_true_element_dict)
    return attr_true_element_dict


def getAtrr(childnode, attname):
    return childnode.getAttribute(attname)

if __name__ == '__main__':
    parseXml("page_source.xml")