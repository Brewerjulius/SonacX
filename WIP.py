import json
import os
import re
import csv
from os.path import exists

a = []
b = []


a = open('HTML_XML_Datasource_Sanatized.txt', 'r', encoding="latin-1").read()
b = open('HTML_XML_Datasource_Sanatized_old.txt', 'r', encoding="latin-1").read()
print(hash(a))
print(hash(b))

