def StringToXml(page_source):
    xml = ""
    for char in page_source:
        if (char != ">"):
            xml += char
        else:
            xml += char
            xml += "\n"
            xml += "    "
    print(xml)
