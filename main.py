from pdf2image import convert_from_path
import sys
import argparse
import os
from image_slicer import slice
import easyocr
from matplotlib import pyplot as plt
import cv2
from PIL import Image
import shutil
import glob
import sys

'''
Image to PDF conversion Arguments
Different arguments that can be passed to convert_from_path:
convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None,
fmt='ppm', jpegopt=None, thread_count=1, userpw=None, use_cropbox=False, strict=False,
transparent=False, single_file=False, output_file=str(uuid.uuid4()), poppler_path=None, 
grayscale=False, size=None, paths_only=False, use_pdftocairo=False, timeout=600)
'''

# Parser setup | Script arguments 
# -f = filename to convert
# -o = output folder
# -t = thread count, dont exceed 4. Optional argument, default is 1.
# -s = sliced image count, optional argument
parser = argparse.ArgumentParser(description='convert pdf to images')
parser.add_argument('-f','--fileName', help="PDF File name", type=str, required=True)
parser.add_argument('-o','--output', help="Output directory", type=str, required=True)
parser.add_argument('-t','--threadCount', help="Output directory",nargs='?', type=int, const = 1)
parser.add_argument('s','--slice', dest='slice', action='store_true')
parser.add_argument('-ns','--no-slice', dest='slice', action='store_false')
parser.set_defaults(slice=False) 
args = parser.parse_args()

# Create directories for clean output
output_dir = os.path.join(os.getcwd(),args.output)
img_path = os.path.join(output_dir,'crop_img')
txt_path = os.path.join(output_dir,'ocr_txt')

os.makedirs(output_dir)
os.mkdir(img_path)
os.mkdir(txt_path)

print('Output directories created...')

#Convert pdf file to 1 big image
images = convert_from_path(args.fileName, dpi=300, thread_count=args.threadCount) 

# Creates images object with each image(converted page) as an entry
# Careful of not having "output folder argument" 
# https://pypi.org/project/pdf2image/ 
# "A relatively big PDF will use up all your memory and cause the process to be killed (unless you use an output folder)"

# Load OCR Model, only runs on first run. needs internet connection
reader = easyocr.Reader(['en','en']) 


#Eventually these prints will be done properly with logging..
print(f".\n.\n.\nConverting file {args.fileName} from pdf to image ... please wait") 

# Helper function to convert list output from OCR to string to be written to a txt file

def listToString(s):
    str_a = ''
    for a in s:
        str_a += str(a[1]) + '\n'
    return str_a


# Go into output directory to begin work
os.chdir(img_path) 

# Image saving + cropping
for i in range(len(images)):
    # Save pages as images in the pdf

    out_img = (f'page{i}.png')
    images[i].save('page' + str(i) + '.png', 'png')

    if args.slice:
        slice(out_img, 100)  # 100 is number of slices

    #Moves the main high res image out of the folder to save time from applying OCR on it needlessly
    shutil.move(out_img, output_dir)

# lol
print(f".\n.\n.\nFile {args.fileName} converted, total of {i+1} image(s) created. Sliced : {args.slice}\n.\n.\n.\nApplying OCR ")

# OCR block

for filename in os.listdir(img_path):

    # Ensure that it is reading from the right directory

    os.chdir(img_path)
    filename_no_ext=os.path.splitext(filename)[0] #get filename without extension for later use
    image = cv2.imread(filename)
    result = reader.readtext(image, detail=1)
    # reads text in 0,90,180,270 degree orientations and picks result with highest confidence

    for detection in result:

        os.chdir(img_path)
        os.remove(filename)
        box_coords = detection[0]
        box_1 = tuple(detection[0][0])
        box_2 = tuple(detection[0][2])
        image = cv2.rectangle(image, ( int(box_1[0]), int(box_1[1]) ), ( int(box_2[0]) , int(box_2[1])), (0,255,0),3)
        cv2.imwrite(filename, image)
        ### Uncomment these 2 lines if you want to see output step by step  
        # plt.imshow(image)
        # plt.show()
        text = listToString(result)
        os.chdir(txt_path)
        with open(filename_no_ext+".txt",'w') as f: f.write(text)

print(".\n.\n.\n.\nStiching...")

# Stitching Area. It is very messy right now but will be cleaned up later. 

# read images from output folder
img_list = os.listdir(img_path)
os.chdir(img_path) #Ensure you are working in the right directory
sample = Image.open(img_list[0])
images = [Image.open(x) for x in img_list] #Load images
width, height = sample.size #obtain image size for offset calculation 
total_width = 10*width
max_height = 10*height
new_im = Image.new('RGB', (total_width, max_height))

#Initial values for image loop
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

os.chdir(output_dir)
new_im.save('ocr.jpg')

print("\n.\n.\n.\nOperation complete")
