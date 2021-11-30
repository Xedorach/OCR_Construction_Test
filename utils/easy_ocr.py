import easyocr 
import os
import argparse
import cv2
from matplotlib import pyplot as plt

reader = easyocr.Reader(['en','en']) # this needs to run only once to load the model into memory

parser = argparse.ArgumentParser(description='read text from images')
parser.add_argument('-f','--fileName', help="image File name", type=str, required=True)
parser.add_argument('-o','--output', help="output file name", type=str, required=True)
args = parser.parse_args()

image = cv2.imread(args.fileName)
result = reader.readtext(image, rotation_info = [0,270])

for detection in result:
    box_coords = detection[0]
    box_1 =  tuple(detection[0][0])
    box_2 =  tuple(detection[0][2])
    image = cv2.rectangle(image, ( int(box_1[0]), int(box_1[1]) ), ( int(box_2[0]) , int(box_2[1])), (0,255,0),3)

def listToString(s):
    str_a = ''
    for a in s:
        str_a += str(a[1]) + '\n'
    return str_a

plt.imshow(image)
plt.show()
text = listToString(result)

with open(args.output+".txt",'w') as f: f.write(text)

