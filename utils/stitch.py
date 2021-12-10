import os
import argparse
from PIL import Image
from math import sqrt

parser = argparse.ArgumentParser(description='convert pdf to images')
parser.add_argument('-f','--fileName', help="PDF File name", type=str, required=True)
parser.add_argument('-s','--slice', help="slice", type=int, required=True)
args = parser.parse_args()

cwd = os.getcwd()

img_path = args.fileName
img_list = os.listdir(img_path)
os.chdir(img_path)
test = Image.open(img_list[0])
images = [Image.open(x) for x in img_list]
width, height = test.size

multiplier = sqrt(args.slice)
print(multiplier)
total_width = int(multiplier*width)
max_height = int(multiplier*height)
new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
y_offset = 0

c = 0
for im in images:
 
    a = img_list[c].split('_')
    y = int(a[1])
    b = a[2]
    d = b.split('.')
    x = int(d[0])
    x_offset = im.size[0]*(x-1)
    y_offset = im.size[1]*(y-1)
    c += 1
    new_im.paste(im, (x_offset,y_offset))

os.chdir(cwd)
new_im.save('test.jpg')

print("\n.\n.\n.\nOperation complete")
