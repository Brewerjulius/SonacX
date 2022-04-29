import xml.etree.ElementTree as etree
import json
import os
from os.path import exists


# This is my default path
path = "C://Users//j.klein//PycharmProjects//my_sanitizer//Alle HTML + dsd en xml files"

# to store files in a list
listoffolders = []
counter = 0
counterDSD2 = 0

# dirs=directories

for (root, dirs, file) in os.walk(path):
    for f in dirs:
         listoffolders.append(f)

length = len(listoffolders)

#/////////////////////////////////////////////////////


#doc = etree.parse('DS_datasource1.xml') #In dezelfde directory als de .py zetten
#root = doc.getroot()
#print(root.text)
combined_dict_list = []



for counterDSD2 in range(236):
    counterDSD2 = counterDSD2 + 1
    file_existsDSD = exists(path + '//' + listoffolders[counter] + '//' + 'DS_datasource1.dsd')
    print("xxxxxxxxxxx")
    print(counterDSD2)
    print("xxxxxxxxxxx")

    if file_existsDSD is True:

        doc = etree.parse(path + '//' + listoffolders[counter] + '//' + 'DS_datasource1.dsd')  # In dezelfde directory als de .py zetten
        root = doc.getroot()

        #for elem in root.findall("./binding/dataobject"):
        with open("dsd.txt", 'w') as f:
            for elem in root.findall("./dataobject"):
                if len(list(elem)) > 0:
                    for x in range(len(list(elem))):
                        if list(elem)[x].attrib["name"] == "PointRefPointName":
                            randomdictnaam = {}
                            randomdictnaam["objectid"] = elem.attrib["id"]
                            randomdictnaam["PointRefPointName"] = list(elem)[x].text
                            randomdictnaam["Display"] = listoffolders[counter]
                            print(randomdictnaam)
                            combined_dict_list.append(randomdictnaam)
                            #print(counterDSD2)
                            #print(counter)
            counter = counter + 1
    else:
        #print("XXXXXXXXXXXXXXXXXXX")
        counter = counter + 1
        print("yyyyyyyyyyyyy")
        print(counter)
        print("yyyyyyyyyyyyy")
print(combined_dict_list)
with open("dsd.txt", 'w') as f:
    for x3 in range(len(combined_dict_list)):
        #print(combined_dict_list[x3])
        #print("xxxxxxxxxxxxxxxxx")
        f.write(json.dumps(combined_dict_list[x3]))
