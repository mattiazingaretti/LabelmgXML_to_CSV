import xml.etree.ElementTree as ET
import csv
import os

XML_FOLDER = 'data/xml/'
IMAGES_FOLDER = 'data/imgs'


records = list()
"""
annotations.csv format:
 path,x1,y1,x2,y2,class_name
 path,,,,,                      (if no obj is present) 
"""


"""
Function that returns the number of objects in the xml file
@author: Mattia Zingaretti
"""
def how_many_obj(xml_file):
    root = ET.parse(os.path.join(XML_FOLDER,xml_file))
    return len(root.findall('object'))


"""
Function that returns a map to all subelements of all the objects in the xml file
return value list of dict where key=obj_instance, value = subdict with all subelements.
@author: Mattia Zingaretti 
"""
def get_objects(root):
    objects = list()
    i = 0
    for obj in root.findall("object"):
        object = dict()
        childs = {child.tag:child.text for child in obj if child.tag != 'bndbox'}
        for bndbox in obj.findall('bndbox'):
            childs[bndbox.tag] = {subel.tag:subel.text for subel in bndbox }
        object[i] = childs
        i += 1
        objects.append(object)
    return objects




def has_xml(file_name):
    for fn in os.listdir(XML_FOLDER):
        if fn[:-4] == file_name[:-4]:
            return True
    return False



def file_formatter( filename):
    i = 0
    print(filename)
    if has_xml(filename):
        xml_filename = filename[:-4] + '.xml'
        root = ET.parse(XML_FOLDER+xml_filename)
        objects = get_objects(root)
        for obj in objects:
            row = list()
            row.append(IMAGES_FOLDER+filename)
            row.append(obj[i]['bndbox']['xmin'])
            row.append(obj[i]['bndbox']['ymin'])
            row.append(obj[i]['bndbox']['xmax'])
            row.append(obj[i]['bndbox']['ymax'])
            row.append(obj[i]['name'])
            records.append(row)
            i += 1
    else:
        row = list()
        row.append(IMAGES_FOLDER + filename)
        while i < 5:
            row.append(None)
            i+=1
        records.append(row)
    return


for img in os.listdir(IMAGES_FOLDER):
    file_formatter(img)


with open('annotations.csv',mode='w') as out:
    out_writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in records:
        out_writer.writerow(row)
