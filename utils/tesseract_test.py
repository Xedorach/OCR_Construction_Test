import cv2
import pytesseract
from matplotlib import pyplot as plt
import os
import argparse

parser = argparse.ArgumentParser(description='test image')
parser.add_argument('image')
args = parser.parse_args()

image = cv2.imread(args.image)
h, w, c = image.shape
boxes = pytesseract.image_to_boxes(image)
for b in boxes.splitlines():
    b = b.split(' ')
    image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

b,g,r = cv2.split(image)
rgb_img = cv2.merge([r,g,b])
txt = pytesseract.image_to_string(args.image)

directory = os.path.join(os.getcwd(), "tesseract_output")
with open(directory+".txt",'w') as f: f.write(str(txt))

print("\n --------------- \n Output \n ---------------")
print(txt)

plt.figure(figsize=(16, 12))
plt.imshow(rgb_img)
plt.title('PyTesseract test')
plt.show()