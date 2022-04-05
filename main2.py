# import OS module
import json
import os
import re
import csv

# This is my default path
path = "C://Users//j.klein//PycharmProjects//my_sanitizer"

# to store files in a list
list = []
lines = []
htmllist = []
nogeenfuckinglijst = []
finalcountdown = []
result10 = []

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
            list.append(f)


length = len(list)


for x in range(length):
    html = open(path + "//Alle HTML + dsd en xml files//" + list[x], 'r', encoding="latin-1").read()
    stripped = re.sub(r"\s+", " ", html)

    result = re.findall(r'<.+?>', stripped)
    htmllist.append(result)

    for x2 in range(len(htmllist[x])):
        result2 = re.findall(r'id=(.+?) ', htmllist[x][x2])
        result3 = re.findall(r'Tag:(.+?);', htmllist[x][x2])
        result4 = re.findall(r'HDXBINDINGID:(.+?);', htmllist[x][x2])
        result5 = re.findall(r'[^0-9a-zA-Z\r] TOP: (.+?);', htmllist[x][x2])
        result6 = re.findall(r'[^0-9a-zA-Z\r] LEFT: (.+?)[;"]', htmllist[x][x2])
        result7 = re.findall(r'[^0-9a-zA-Z\\]\\(.+?).sha', htmllist[x][x2])
        if result7 != None:
            for x3 in range(len(result7)):
                result8 = re.search(r'\\', result7[x3])
                #print(result8)
                result9 = result8.end()
                #print(result9)
                result10 = re.sub(r'.', '', result7[x3], count=result9)
        if result7 == None:
            result10 == None

        #print(result2)
        #print(result7)
        if "id=" in htmllist[x][x2] and len(result2) > 0: #and len(result3) > 0: #<---------------------------------------------
            nogeenfuckinglijst.append(htmllist[x][x2])
            y = y+1
            if len(result3) > 0:
                TI = T
                T = T+1
            else:
                TI = None

            if len(result4) > 0:
                LengteHDX = LengteHDX + 1

            if len(result4) < 1:
                result4 = None

            if len(result5) < 1:
                result5 = None

            if len(result6) < 1:
                result6 = None

            if len(result10) < 1:
                result7 = None

            bigdict = {
                "ObjectID": y,
                "displayID": x+1,
                "Object": result2[0],
                "TagID": TI,
                "Tag": result3,
                "HDXBINDINGID": result4,
                "Locatie_Top": result5,
                "Locatie_Left": result6,
                "Faceplate": result10
            }

            finalcountdown.append(bigdict)

with open("Darius.txt", 'w') as f:
    for x3 in range(len(finalcountdown)):
        print(finalcountdown[x3])
        f.write(json.dumps(finalcountdown[x3]))

print(len(finalcountdown))
print(LengteHDX)