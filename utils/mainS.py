from pdf2image import convert_from_path
import sys
import argparse
import os
from image_slicer import slice
import easyocr
from matplotlib import pyplot as plt
import cv2

'''
Image to PDF conversion Arguments
Different arguments that can be passed to convert_from_path:

convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None,
fmt='ppm', jpegopt=None, thread_count=1, userpw=None, use_cropbox=False, strict=False,
transparent=False, single_file=False, output_file=str(uuid.uuid4()), poppler_path=None, 
grayscale=False, size=None, paths_only=False, use_pdftocairo=False, timeout=600)
'''

# Scripts arguments 
# -f = filename to convert
# -o = output folder
# -t = thread count, dont exceed 4. Optional argument, default is 2.
# -s = sliced image count, optional argument
parser = argparse.ArgumentParser(description='convert pdf to images')
parser.add_argument('-f','--fileName', help="PDF File name", type=str, required=True)
parser.add_argument('-o','--output', help="Output directory", type=str, required=True)
parser.add_argument('-t','--threadCount', help="Output directory",nargs='?', type=int, const = 2)
parser.add_argument('-s','--slice',help='How many slices for the image',nargs='?', type=int,
                     const=1)
args = parser.parse_args()

# Make directory for output images to keep stuff clean
output_dir = os.path.join(os.getcwd(),args.output)
os.makedirs(output_dir)
crop_img_path = os.path.join(output_dir,'crop_img')
txt_path = os.path.join(output_dir, 'ocr_txt')
ocr_img_path = os.path.join(output_dir, 'ocr_img')

os.mkdir(crop_img_path)
os.mkdir(txt_path)
os.mkdir(ocr_img_path)

#Convert pdf file to 1 big image
images = convert_from_path(args.fileName, dpi=300, thread_count=args.threadCount) 

# Load OCR Model, only runs on first run. needs internet connection
reader = easyocr.Reader(['en','en']) 

# Creates images object with each image(converted page) as an entry

# Careful of not having "output folder argument" 
# https://pypi.org/project/pdf2image/ 
# "A relatively big PDF will use up all your memory and cause the process to be killed (unless you use an output folder)"

#Eventually these prints will be done properly with logging..

print(f"Converting file {args.fileName} from pdf to image .. please wait") 

def listToString(s):
    str_a = ''
    for a in s:
        str_a += str(a[1]) + '\n'
    return str_a

os.chdir(output_dir) 


for i in range(len(images)):
    # Save pages as images in the pdf
    os.chdir(crop_img_path)
    out_img = (f'page{i}.png')
    images[i].save('page' + str(i) + '.png', 'png')
    
    if args.slice:
        slice(out_img, args.slice)

print(f"File {args.fileName} converted, total of {i+1} images created with {args.slice} number of slices...\nApplying OCR.. ")


for filename in os.listdir(crop_img_path):
    os.chdir(crop_img_path)
    image = cv2.imread(str(filename))
    result = reader.readtext(image, rotation_info = [0,270])
    filename_no_ext= os.path.splitext(filename)[0]
    os.chdir(ocr_img_path)
    for detection in result:
        box_coords = detection[0]
        box_1 =  tuple(detection[0][0])
        box_2 =  tuple(detection[0][2])
        image = cv2.rectangle(image, ( int(box_1[0]), int(box_1[1]) ), ( int(box_2[0]) , int(box_2[1])), (0,255,0),3)
        cv2.imwrite(str(filename_no_ext) + '_ocr.png', image)
    def listToString(s):
        str_a = ''
        for a in s:
            str_a += str(a[1]) + '\n'
        return str_a

    # plt.imshow(image)
    # plt.show()
    text = listToString(result)
    os.chdir(txt_path)
    with open(filename_no_ext+".txt",'w') as f: f.write(text)











