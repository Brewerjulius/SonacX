# import OS module
import json
import os
import re
import csv

from os.path import exists
import xml.etree.ElementTree as etree

# This is my default path
path = "C://Users//j.klein//PycharmProjects//my_sanitizer"

# to store files in a list
HTML_Name_List = []

HTML_Content_List = []
Content_List_Verfied_Full = []
Sanatized_Data_Dict = []
Result_Faceplate_Final = []

count = 1
y = 1
T = 1
TI = 0
LengteHDX = 0
# dirs=directories

for (root, dirs, file) in os.walk(path):
    for f in file:
        if '.htm' in f:
            print(f)
            HTML_Name_List.append(f)


Length_HTML_List = len(HTML_Name_List)

listoffolders = []
counterXML1 = 0
counterXLM2 = 0
combined_dict_list = []

XML_Object_ID = []
# dirs=directories

for (root, dirs, file) in os.walk(path):
    for f in dirs:
         listoffolders.append(f)


for x in range(Length_HTML_List):
    html = open(path + "//Alle HTML + dsd en xml files//" + HTML_Name_List[x], 'r', encoding="latin-1").read()
    stripped = re.sub(r"\s+", " ", html)

    result = re.findall(r'<.+?>', stripped)
    HTML_Content_List.append(result)

    for x2 in range(len(HTML_Content_List[x])):
        Result_ID = re.findall(r'id=(.+?) ', HTML_Content_List[x][x2])
        Result_Tag = re.findall(r'Tag:(.+?);', HTML_Content_List[x][x2])
        Result_HDX_ID = re.findall(r'HDXBINDINGID:(.+?);', HTML_Content_List[x][x2])
        Result_Top = re.findall(r'[^0-9a-zA-Z\r] TOP: (.+?);', HTML_Content_List[x][x2])
        Result_Left = re.findall(r'[^0-9a-zA-Z\r] LEFT: (.+?)[;"]', HTML_Content_List[x][x2])
        Result_Faceplate1 = re.findall(r'[^0-9a-zA-Z\\]\\(.+?).sha', HTML_Content_List[x][x2])
        if Result_Faceplate1 != None:
            for x3 in range(len(Result_Faceplate1)):
                Result_Faceplate2 = re.search(r'\\', Result_Faceplate1[x3])
                #print(Result_Faceplate2)
                Result_Faceplate3 = Result_Faceplate2.end()
                #print(Result_Faceplate3)
                Result_Faceplate_Final = re.sub(r'.', '', Result_Faceplate1[x3], count=Result_Faceplate3)
        if Result_Faceplate1 == None:
            Result_Faceplate_Final == None

        #print(Result_ID)
        #print(Result_Faceplate1)
        if "id=" in HTML_Content_List[x][x2] and len(Result_ID) > 0: #and len(Result_Tag) > 0: #<---------------------------------------------
            Content_List_Verfied_Full.append(HTML_Content_List[x][x2])
            y = y+1
            if len(Result_Tag) > 0:
                TI = T
                T = T+1
            else:
                TI = None

            if len(Result_HDX_ID) > 0:
                LengteHDX = LengteHDX + 1

            if len(Result_HDX_ID) < 1:
                Result_HDX_ID = None

            if len(Result_Top) < 1:
                Result_Top = None

            if len(Result_Left) < 1:
                Result_Left = None

            if len(Result_Faceplate_Final) < 1:
                Result_Faceplate1 = None



            file_existsXLM = exists(path + '//' + listoffolders[Length_HTML_List] + '//' + 'bindings.xml')
            if file_existsXLM is True:
                doc = etree.parse(path + '//' + listoffolders[
                    counterXML1] + '//' + 'bindings.xml')  # In dezelfde directory als de .py zetten
                root = doc.getroot()

                for elem in root.findall("./binding"):
                    if len(list(elem)) > 0 and elem.attrib["ID"] != "pageparam":
                        attributes = elem.attrib
                        child = list(elem)[0].attrib
                        attributes["objectid"] = child["objectid"]
                        attributes["Display"] = listoffolders[counterXML1]
                        #print(attributes)
                    if child["objectid"] is Result_HDX_ID:
                        XML_Object_ID = elem.attrib["ID"]
                    else:
                        XML_Object_ID = None

            bigdict = {
                "ObjectID": y,
                "displayID": x+1,
                "Object": Result_ID[0],
                "TagID": TI,
                "Tag": Result_Tag,
                "HDXBINDINGID": Result_HDX_ID,
                "XML_Object_ID": XML_Object_ID,
                "Locatie_Top": Result_Top,
                "Locatie_Left": Result_Left,
                "Faceplate": Result_Faceplate_Final
            }

            Sanatized_Data_Dict.append(bigdict)

with open("HTML_XML_Datasource_Sanatized.txt", 'w') as f:
    for x3 in range(len(Sanatized_Data_Dict)):
        print(Sanatized_Data_Dict[x3])
        f.write(json.dumps(Sanatized_Data_Dict[x3]))

print(len(Sanatized_Data_Dict))
print(LengteHDX)