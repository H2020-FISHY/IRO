import xml.etree.ElementTree as ET
root = ET.parse('policies/hspl1.xml').getroot()
print(root)
for child in root:
    value = child.tag
    print(value, child.attrib)
print([elem.tag for elem in root.iter()])