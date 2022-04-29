import xml.etree.ElementTree as etree
import json
import os
from os.path import exists
#coding: utf-8

# This is my default path
path = r"C://Users//j.klein//PycharmProjects//my_sanitizer//Alle HTML + dsd en xml files"

# to store files in a list


listoffolders = []
counter = 0
counterXLM2 = 0
combined_dict_list = []

# dirs=directories

for (root, dirs, file) in os.walk(path):
    for f in dirs:
         listoffolders.append(f)

length = len(listoffolders)

print(listoffolders[39])

#////////////////////////////////////////////////////////////////////////////////////////////////

for counterXLM2 in range(236):
    file_existsXLM = exists(path + '//' + listoffolders[counter] + '//' + 'bindings.xml')
    if file_existsXLM is True:
        doc = etree.parse(path + '//' + listoffolders[counter] + '//' + 'bindings.xml') #In dezelfde directory als de .py zetten
        root = doc.getroot()

        for elem in root.findall("./binding"):
            if len(list(elem)) > 0 and elem.attrib["ID"] != "pageparam":
                attributes = elem.attrib
                child = list(elem)[0].attrib
                attributes["objectid"] = child["objectid"]
                attributes["Display"] = listoffolders[counter]
                print(attributes)
                combined_dict_list.append(attributes)
        counter = counter + 1
        print(counter)

    else:
        print("XXXXXXXXXXXXXXXXXXX")
        counter = counter + 1

with open(r"xmller.txt", 'w', encoding="utf-8") as f:
    for x in range(len(combined_dict_list)):
        print(combined_dict_list[x])
        f.write(json.dumps(combined_dict_list[x]))