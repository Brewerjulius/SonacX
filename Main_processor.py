#  Import OS modules
import json
import os
import re
from os.path import exists
import xml.etree.ElementTree as etree
from datetime import datetime

#  These are the default paths
path_main = os.getcwd()
path_data = path_main + "/data"

#  Initialise some lists
html_name_list = []
html_content_list = []
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
#  Initialise variables
object_id_counter = 1
tag_counter = 1
tag_id = 0
length_hdx = 0
counterXML1 = 0
counterXLM2 = 0
counterDSD1 = 0

# Log counters
counterObjectID = 0
counterDisplayName = 0
counterObjectName = 0
counterTagID = 0
counterTag = 0
counterHDXBINDINGID = 0
counterXML_Object_ID = 0
counterDSD_Object_ID = 0
counterDSD_Tag = 0
counterLocatie_Top = 0
counterLocatie_Left = 0
counterWidth = 0
counterHeight = 0
counterFaceplate = 0

#  datetime object containing current date and time
now = datetime.now()

#  Make and fill a log file. Timeformat: dd-mm-YY H:M:S
dt_string = now.strftime("%d-%m-%Y %H.%M.%S")
print("date and time =", dt_string)

fileNameString = 'Log' + dt_string + '.txt'

#  Loop trough dirs and collect HTML filenames for list
print("Creating file list: ")

for (root, dirs, file) in os.walk(path_data):
    for f in file:
        if '.htm' in f:
            print(f)
            html_name_list.append(f)

print("\nList created.\n")

#  Get list length
length_html_list = len(html_name_list)

#  Loop through folder names
for (root, dirs, file) in os.walk(path_data):
    for f in dirs:
        list_of_folders.append(f)
#  Get bare filenames (without extension)

# Data processing message.
print("**Now processing data, please wait.**\n")

counterFiles = 0

# Start of programm loop.
for x in range(length_html_list):

    # Log counters
    counterHDXBINDINGID_Per_File = 0
    counterXML_Object_ID_Per_File = 0
    counterDSD_Object_ID_Per_File = 0
    entryCounter = 0
    counterFiles = counterFiles + 1

    file_verification = False

    # Filling String with data from HTML file.
    html = open(path_data + "/" + html_name_list[x], 'r', encoding="latin-1").read()

    # Stripping the HTML string.
    stripped = re.sub(r"\s+", " ", html)

    # Delete the titles from the whole string to avoid random characters from interfering with the Regex later
    title_deletion = re.sub(r'title="(.+?)"', "", stripped)

    # Making list of all the lines between "<" and ">".
    result = re.findall(r'<.+?>', title_deletion)
    html_content_list.append(result)

    # Filter loop start.
    for x2 in range(len(html_content_list[x])):
        result_id = re.findall(r'id=(.+?) ', html_content_list[x][x2])
        result_tag = re.findall(r'Tag:(.+?);', html_content_list[x][x2])
        result_hdx_id = re.findall(r'HDXBINDINGID:(.+?);', html_content_list[x][x2])
        result_top = re.findall(r'[^0-9a-zA-Z\r] TOP: (.+?);', html_content_list[x][x2])
        result_left = re.findall(r'[^0-9a-zA-Z\r] LEFT: (.+?)[;"]', html_content_list[x][x2])
        result_faceplate_1 = re.findall(r'src = "[^0-9a-zA-Z\\]\\(.+?).sha', html_content_list[x][x2])
        result_width = re.findall(r'WIDTH: (.+?);', html_content_list[x][x2])
        result_height = re.findall(r'HEIGHT: (.+?);', html_content_list[x][x2])

        # Filtering the data from the Faceplate. Removing unwanted parts.
        if result_faceplate_1 != None:
            for x3 in range(len(result_faceplate_1)):
                result_faceplate_2 = re.search(r'\\', result_faceplate_1[x3])
                result_faceplate_3 = result_faceplate_2.end()
                result_faceplate_final = re.sub(r'.', '', result_faceplate_1[x3], count=result_faceplate_3)
        if result_faceplate_1 == None:
            result_faceplate_final = None

        # Verify if a ID is present.
        # IF no ID is found there is no data, and this loop will be skipped.
        # IF an ID is found the data is processed and added to a list.
        if "id=" in html_content_list[x][x2] and len(result_id) > 0: #  And len(Result_Tag) > 0: # <----------------------
            # content_list_verfied_full.append(html_content_list[x][x2])
            object_id_counter = object_id_counter + 1
            if len(result_tag) > 0:
                tag_id = tag_counter
                tag_counter = tag_counter + 1
            else:
                tag_id = None

            # Setting variables to None if the variable is 1 or lower.
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

            # Reading Data from XML files.
            file_existsXLM = exists(path_data + '/' + list_of_folders[x] + '/' + 'bindings.xml')
            if file_existsXLM is True:
                doc = etree.parse(path_data + '/' + list_of_folders[
                    counterXML1] + '/' + 'bindings.xml')
                root = doc.getroot()

                # Filtering data from XML files.
                for elem in root.findall("./binding"):
                    if len(list(elem)) > 0 and elem.attrib["ID"] != "pageparam":
                        attributes = elem.attrib
                        child = list(elem)[0].attrib
                        attributes["objectid"] = child["objectid"]
                        attributes["Display"] = list_of_folders[counterXML1]
                        if result_hdx_id is not None:
                            if attributes["ID"] == result_hdx_id[0]:
                                xml_object_id = attributes["objectid"]

                        else:
                            xml_object_id = None

            # Emptying DSD variables
            dsd_object_id_to_dict = None
            dsd_tag_to_dict = None
            dsd_object_id_temp = None
            dsd_tag_temp = None

            # Reading .dsd file data.
            file_exists_dsd = exists(path_data + '/' + list_of_folders[x] + '/' + 'DS_datasource1.dsd')
            if file_exists_dsd is True:
                if xml_object_id is not None:
                    doc = etree.parse(path_data + '/' + list_of_folders[x]
                                      + '/' + 'DS_datasource1.dsd')
                    root = doc.getroot()

                    # Filtering dsd file data.
                    for elem in root.findall("./dataobject"):
                        if dsd_object_id_to_dict is not None:
                            break

                        if len(list(elem)) > 0:
                            for z in range(len(list(elem))):
                                if list(elem)[z].attrib["name"] == "PointRefPointName":
                                    dsd_object_id_temp = elem.attrib["id"]
                                    dsd_tag_temp = list(elem)[z].text
                                    dsd_file_temp = list_of_folders[x]
                                    if dsd_object_id_temp is not None:

                                        if dsd_object_id_temp == xml_object_id:
                                            dsd_object_id_to_dict = elem.attrib["id"]
                                            dsd_tag_to_dict = list(elem)[z].text
                                            z = range(len(list(elem)))
                                            break
                                        else:
                                            dsd_object_id_to_dict = None
                                            dsd_tag_to_dict = None
            else:
                dsd_object_id_temp = None
                dsd_tag_temp = None

            if result_hdx_id is not None:
                counterHDXBINDINGID_Per_File = counterHDXBINDINGID_Per_File + 1

            if result_hdx_id is not None:
                counterXML_Object_ID_Per_File = counterXML_Object_ID_Per_File + 1

            if result_hdx_id is not None:
                counterDSD_Object_ID_Per_File = counterDSD_Object_ID_Per_File + 1

            # adding data to a dict.
            bigdict = {
                "ObjectID": object_id_counter,
                "DisplayID": x+1,
                "DisplayName": html_name_list[x],
                "ObjectName": result_id[0],
                "TagID": tag_id,
                "Tag": result_tag,
                "HDXBINDINGID": result_hdx_id,
                # HDX id is the key between XML and HTML
                "XML_Object_ID": xml_object_id,
                # XML id is the key between XML and DSD
                "DSD_Object_ID": dsd_object_id_to_dict,
                # DSD id is the key between XML and DSD
                "DSD_Tag": dsd_tag_to_dict,
                "Locatie_Top": result_top,
                "Locatie_Left": result_left,
                "Width": result_width,
                "Height": result_height,
                "Faceplate": result_faceplate_final
            }

            # Log counter
            entryCounter = entryCounter + 1

            if object_id_counter is not None:
                counterObjectID = counterObjectID + 1

            if html_name_list[x] is not None:
                counterDisplayName = counterDisplayName + 1

            if result_id[0] is not None:
                counterObjectName = counterObjectName + 1

            if tag_id is not None:
                counterTagID = counterTagID + 1

            if result_tag is not None:
                counterTag = counterTag + 1

            if result_hdx_id is not None:
                counterHDXBINDINGID = counterHDXBINDINGID + 1

            if xml_object_id is not None:
                counterXML_Object_ID = counterXML_Object_ID + 1

            if dsd_object_id_to_dict is not None:
                counterDSD_Object_ID = counterDSD_Object_ID + 1

            if dsd_tag_to_dict is not None:
                counterDSD_Tag = counterDSD_Tag + 1

            if result_top is not None:
                counterLocatie_Top = counterLocatie_Top + 1

            if result_left is not None:
                counterLocatie_Left = counterLocatie_Left + 1

            if result_width is not None:
                counterWidth = counterWidth + 1

            if result_height is not None:
                counterHeight = counterHeight + 1

            if result_faceplate_final is not None:
                counterFaceplate = counterFaceplate + 1

            # Error catcher. If no data is found, set file verification to True indicating something went wrong.
            if bigdict is not None:
                file_verification = True

            sanatized_data_dict.append(bigdict)

    with open(fileNameString, "a") as external_file:
        print("\nFile name processed: " + list_of_folders[x], file=external_file)
        print("counterHDXBINDINGID " + str(counterHDXBINDINGID_Per_File), file=external_file)
        print("counterXML_Object_ID " + str(counterXML_Object_ID_Per_File), file=external_file)
        print("counterDSD_Object_ID " + str(counterDSD_Object_ID_Per_File), file=external_file)
        print("entryCounter " + str(entryCounter), file=external_file)
        print("-----------------------------------------------------------------------------------", file=external_file)

    # Verify if a file had any data in it. IF its empty print message.
    if file_verification is False:

        print("File \"" + html_name_list[x] + "\" is invalid or has no data.")

        with open(fileNameString, "a") as external_file:
            logstring = (html_name_list[x] + "\" is invalid or has no data.\n")
            print(logstring, file=external_file)
            external_file.close()


# Data dumb from all the filtered data to a text file.
with open("HTML_XML_Datasource_Sanatized.txt", 'w') as f:
    for x3 in range(len(sanatized_data_dict)):
        f.write(json.dumps(sanatized_data_dict[x3]))

with open(fileNameString, "a") as external_file:
    print("***********************************************************************************", file=external_file)
    print("Total counters: ", file=external_file)
    print("counterObjectID " + str(counterObjectID), file=external_file)
    print("counterDisplayName " + str(counterDisplayName), file=external_file)
    print("counterObjectName " + str(counterObjectName), file=external_file)
    print("counterTagID " + str(counterTagID), file=external_file)
    print("counterTag " + str(counterTag), file=external_file)
    print("counterHDXBINDINGID " + str(counterHDXBINDINGID), file=external_file)
    print("counterXML_Object_ID " + str(counterXML_Object_ID), file=external_file)
    print("counterDSD_Object_ID " + str(counterDSD_Object_ID), file=external_file)
    print("counterDSD_Tag " + str(counterDSD_Tag), file=external_file)
    print("counterLocatie_Top " + str(counterLocatie_Top), file=external_file)
    print("counterLocatie_Left " + str(counterLocatie_Left), file=external_file)
    print("counterWidth " + str(counterWidth), file=external_file)
    print("counterHeight " + str(counterHeight), file=external_file)
    print("counterFaceplate " + str(counterFaceplate), file=external_file)
    print("\nEntries processed: " + str(len(sanatized_data_dict)), file=external_file)
    print("\nHTML files processed: " + str(counterFiles), file=external_file)
    print("\nXML files processed: " + str(counterFiles), file=external_file)
    print("\nDSD files processed: " + str(counterFiles), file=external_file)

# Programm end with error catch.
if(len(sanatized_data_dict) < 1):
    print("A fatal error has occured")
else:
    print("\nEntries processed: " + str(len(sanatized_data_dict)))
    print("\nEnd of program")

input("Press Enter to continue...")