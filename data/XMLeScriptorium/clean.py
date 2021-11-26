import re
import xml.etree.ElementTree as ET

# important classes: Element, ElementTree
# important functions:
#                       ET.fromstring(String) --> Element
#                       ET.parse(File) --> ElementTree [objet]
#                       ET.tostring(Element) --> String

TEST = "data/XMLeScriptorium/19_janvier_1.pdf_page_1.xml"



tree = ET.parse(TEST)
root = tree.getroot()
print("The root.tag is {}".format(root.tag))
print("The root attribute is {}".format(root.attrib))

# get 'CONTENT' attribute of 'String' element
attribute = root.get('xmlns:xsi')
print("First attribute is {val}".format(val=attribute))

for child in root:
    print(child.tag, child.attrib)