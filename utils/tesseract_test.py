import cv2
import pytesseract
from matplotlib import pyplot as plt
import os
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description='read text from images')
parser.add_argument('-f','--fileName', help="PDF File name", type=str, required=True)
parser.add_argument('-o','--output', help="filename", type=str, required=True)
args = parser.parse_args()

image = cv2.imread(args.fileName)
h, w, c = image.shape
boxes = pytesseract.image_to_boxes(image)
for b in boxes.splitlines():
    b = b.split(' ')
    image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

b,g,r = cv2.split(image)
rgb_img = cv2.merge([r,g,b])
txt = pytesseract.image_to_string(image)

directory = os.path.join(os.getcwd(), args.output)
with open(filename+".txt",'w') as f: f.write(str(txt))

print("\n --------------- \n Output \n ---------------")
print(txt)

plt.figure(figsize=(16, 12))
plt.imshow(image)
plt.title('PyTesseract test')
plt.show()