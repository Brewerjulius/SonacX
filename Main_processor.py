# Import OS modules
import json
import os
import re
from os.path import exists
import xml.etree.ElementTree as etree

# These are the default paths
path_main = os.getcwd()
path_data = path_main + "/data"

# Initialise some lists
html_name_list = []
html_content_list = []
content_list_verfied_full = []
sanatized_data_dict = []
result_faceplate_final = []
combined_dict_list = []
list_of_folders = []
xml_object_id = []
dsd_object_id_temp = []
dsd_tag_temp = []
dsd_object_id_to_dict = []
dsd_tag_to_dict = []
dsd_file_temp = []

# Initialise variables
# count = 1
object_id_counter = 1
tag_counter = 1
tag_id = 0
length_hdx = 0
counterXML1 = 0
counterXLM2 = 0
counterDSD1 = 0

# Loop trough dirs and collect HTML filenames for list
print("Creating file list: ")
for (root, dirs, file) in os.walk(path_data):
    for f in file:
        if '.htm' in f:
            print(f)
            html_name_list.append(f)

print("\nList created.\n")

# Get list length
length_html_list = len(html_name_list)

# Loop through folder names
for (root, dirs, file) in os.walk(path_data):
    for f in dirs:
        list_of_folders.append(f)
# Get bare filenames (without extension)

#Data processing message.
print("**Now processing data, please wait.**\n")

#Start of programm loop.
for x in range(length_html_list):
    file_verification = False

    #Filling String with data from HTML file.
    html = open(path_data + "/" + html_name_list[x], 'r', encoding="latin-1").read()

    #Stripping the HTML string.
    stripped = re.sub(r"\s+", " ", html)

    #Making list of all the lines between "<" and ">".
    result = re.findall(r'<.+?>', stripped)
    html_content_list.append(result)

    #Filter loop start.
    for x2 in range(len(html_content_list[x])):
        result_id = re.findall(r'id=(.+?) ', html_content_list[x][x2])
        result_tag = re.findall(r'Tag:(.+?);', html_content_list[x][x2])
        result_hdx_id = re.findall(r'HDXBINDINGID:(.+?);', html_content_list[x][x2])
        result_top = re.findall(r'[^0-9a-zA-Z\r] TOP: (.+?);', html_content_list[x][x2])
        result_left = re.findall(r'[^0-9a-zA-Z\r] LEFT: (.+?)[;"]', html_content_list[x][x2])
        result_faceplate_1 = re.findall(r'src = "[^0-9a-zA-Z\\]\\(.+?).sha', html_content_list[x][x2])
        result_width = re.findall(r'WIDTH: (.+?);', html_content_list[x][x2])
        result_height = re.findall(r'HEIGHT: (.+?);', html_content_list[x][x2])

        #Filtering the data from the Faceplate. Removing unwanted parts.
        if result_faceplate_1 != None:
            for x3 in range(len(result_faceplate_1)):
                result_faceplate_2 = re.search(r'\\', result_faceplate_1[x3])
                result_faceplate_3 = result_faceplate_2.end()
                result_faceplate_final = re.sub(r'.', '', result_faceplate_1[x3], count=result_faceplate_3)
        if result_faceplate_1 == None:
            result_faceplate_final = None

        #Verify if a ID is present.
        #IF no ID is found there is no data, and this loop will be skipped.
        #IF an ID is found the data is processed and added to a list.
        if "id=" in html_content_list[x][x2] and len(result_id) > 0: # And len(Result_Tag) > 0: #<----------------------
            content_list_verfied_full.append(html_content_list[x][x2])
            object_id_counter = object_id_counter + 1
            if len(result_tag) > 0:
                tag_id = tag_counter
                tag_counter = tag_counter + 1
            else:
                tag_id = None

            #Setting variables to None if the variable is 1 or lower.
            if len(result_hdx_id) > 0:
                length_hdx = length_hdx + 1

            if len(result_hdx_id) < 1:
                result_hdx_id = None

            if len(result_top) < 1:
                result_top = None

            if len(result_left) < 1:
                result_left = None

            if len(result_faceplate_final) < 1:
                result_faceplate_1 = None

            if len(result_width) < 1:
                result_width = None

            if len(result_height) < 1:
                result_height = None

            #Reading Data from XML files.
            file_existsXLM = exists(path_data + '/' + list_of_folders[length_html_list] + '/' + 'bindings.xml')
            if file_existsXLM is True:
                doc = etree.parse(path_data + '/' + list_of_folders[
                    counterXML1] + '/' + 'bindings.xml')
                root = doc.getroot()

                #Filtering data from XML files.
                for elem in root.findall("./binding"):
                    if len(list(elem)) > 0 and elem.attrib["ID"] != "pageparam":
                        attributes = elem.attrib
                        child = list(elem)[0].attrib
                        attributes["objectid"] = child["objectid"]
                        attributes["Display"] = list_of_folders[counterXML1]
                        if result_hdx_id is not None:
                            if attributes["ID"] is result_hdx_id[0]:
                                xml_object_id = attributes["objectid"]
                        else:
                            xml_object_id = None

            #Emptying DSD variables
            dsd_object_id_to_dict = None
            dsd_tag_to_dict = None
            dsd_object_id_temp = None
            dsd_tag_temp = None

            #Reading .dsd file data.
            file_exists_dsd = exists(path_data + '/' + list_of_folders[length_html_list] + '/' + 'DS_datasource1.dsd')
            if file_exists_dsd is True:
                if xml_object_id is not None:
                    doc = etree.parse(path_data + '/' + list_of_folders[length_html_list]
                                      + '/' + 'DS_datasource1.dsd')
                    root = doc.getroot()

                    #Filtering dsd file data.
                    for elem in root.findall("./dataobject"):
                        if len(list(elem)) > 0:
                            for z in range(len(list(elem))):
                                if list(elem)[z].attrib["name"] == "PointRefPointName":
                                    dsd_object_id_temp = elem.attrib["id"]
                                    dsd_tag_temp = list(elem)[z].text
                                    dsd_file_temp = list_of_folders[length_html_list]
                                    if dsd_object_id_temp is not None:

                                        if dsd_object_id_temp == xml_object_id:
                                            dsd_object_id_to_dict = elem.attrib["id"]
                                            dsd_tag_to_dict = list(elem)[z].text
                                            break
            else:
                dsd_object_id_temp = None
                dsd_tag_temp = None

            #adding data to a dict.
            bigdict = {
                "ObjectID": object_id_counter,
                "DisplayID": x+1,
                "DisplayName": html_name_list[x],
                "ObjectName": result_id[0],
                "TagID": tag_id,
                "Tag": result_tag,
                "HDXBINDINGID": result_hdx_id,
                #HDX id is the key between XML and HTML
                "XML_Object_ID": xml_object_id,
                #XML id is the key between XML and DSD
                "DSD_Object_ID": dsd_object_id_to_dict,
                #duplicate van XML_Object_ID, alleen voor testen van functionaliteit, verwijder later.
                "DSD_Tag": dsd_tag_to_dict,
                "Locatie_Top": result_top,
                "Locatie_Left": result_left,
                "Width": result_width,
                "Height": result_height,
                "Faceplate": result_faceplate_final
            }

            #Error catcher. If no data is found, set file verification to True indicating something went wrong.
            if bigdict is not None:
                file_verification = True

            sanatized_data_dict.append(bigdict)

    #Verify if a file had any data in it. IF its empty print message.
    if file_verification is False:
        print("File \"" + html_name_list[x] + "\" is invalid or has no data.")

#Data dumb from all the filtered data to a text file.
with open("HTML_XML_Datasource_Sanatized.txt", 'w') as f:
    for x3 in range(len(sanatized_data_dict)):
        f.write(json.dumps(sanatized_data_dict[x3]))

#Programm end with error catch.
if(len(sanatized_data_dict) < 1):
    print("A fatal error has occured")
else:
    print("\nEntries processed: " + str(len(sanatized_data_dict)))
    print("\nEnd of program")
input("Press Enter to continue...")