#!/usr/bin/env python3
import os, re, pandas
import xml.etree.ElementTree as et
from pandas import DataFrame

base_path = os.path.dirname(os.path.realpath(__file__))
filename = input('Input your file path here:\n> ')
xml_path = os.path.join(base_path, filename)
# Define which file to par
tree = et.parse(xml_path)
# Create empty arrays
data, name, app_url, app_ipaddr, app_port = [], [], [], [], []

for each in tree.iterfind('Services/HTTP/ServiceList/ReverseList/HTTP_Reverse/HTTP_ReverseSubservice/HTTP_HostSubserviceList'):
    for i in each:
        data.append(i.attrib)

# Filter data
for line in data:
    name.append(str(line).split(':')[2].split(',')[0])
    app_url.append(str(line).split(':')[5].split(',')[0])

# IPs Addresses Section
for each in tree.iterfind('Services/HTTP/ServiceList/ReverseList/HTTP_Reverse/HTTP_ReverseSubservice/HTTP_HostSubserviceList/HTTP_HostSubservice/Webserver/ServerAddressList'):
    ipaddr = ''
    for i in each.iterfind('ServerAddress'):
        ipaddr = ipaddr + str(i.attrib).split(':')[1].replace('Order','')
        ipaddr = re.sub('\'\'|\s\s', '', ipaddr)
        ipaddr = re.sub(',\s$', '', ipaddr)
        ipaddr = re.sub('\'\s\'', '\',\'', ipaddr)
    app_ipaddr.append(ipaddr)

# Ports Addresses Section
for each in tree.iterfind('Services/HTTP/ServiceList/ReverseList/HTTP_Reverse/HTTP_ReverseSubservice/HTTP_HostSubserviceList/HTTP_HostSubservice/Webserver'):
    for i in each:
        if i.tag == 'Port':
            app_port.append(str(i.attrib).split(':')[1].strip('\}'))

# Creates the csv file
file = open("sample.txt", "w")

for result in zip(name, app_url,app_ipaddr,app_port):
        result = re.sub('\'\'|\s\s|\s\'|\'|[\(\)\"]', '', str(result))
        result = re.sub(', ', ';', result)
        result = re.sub('$', '\n', result)
        file.write(result)

file.close()

# Read data from file
data = pandas.read_csv("sample.txt",delimiter=';')

# Edit the column name to certain strings
data.columns=['Application Name','URL','IP Address','Port']
print(data)
# Set DataFrame input and export to file
df = DataFrame(data)
export_excel = df.to_excel(r'output.xlsx', index=None, header=True)
