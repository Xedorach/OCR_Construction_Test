from pdf2image import convert_from_path
import sys
import argparse
import os
from image_slicer import slice

# Image to PDF conversion script, takes 2 arguments: File name and output folder name
# Different arguments that can be passed to convert_from_path:

# convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None,
#  fmt='ppm', jpegopt=None, thread_count=1, userpw=None, use_cropbox=False, strict=False,
#  transparent=False, single_file=False, output_file=str(uuid.uuid4()), poppler_path=None, 
# grayscale=False, size=None, paths_only=False, use_pdftocairo=False, timeout=600)

parser = argparse.ArgumentParser(description='convert pdf to images')
parser.add_argument('-f','--fileName', help="PDF File name", type=str, required=True)
parser.add_argument('-o','--output', help="Output directory", type=str, required=True)
parser.add_argument('-t','--threadCount', help="Output directory",nargs='?', type=int, const = 2)
parser.add_argument('-s','--slice',help='How many slices for the image',nargs='?', type=int,
                     const=1)
args = parser.parse_args()
images = convert_from_path(args.fileName, dpi=300, thread_count = args.threadCount)

output_dir = os.path.join(os.getcwd(),args.output)
os.mkdir(output_dir)
os.chdir(output_dir) 

print(f"Converting file {args.fileName} from pdf to image .. please wait")


for i in range(len(images)):
    # Save pages as images in the pdf
    out_img = (f'page{i}.png')
    images[i].save('page' + str(i) + '.png', 'png')

    if args.slice:
        slice(out_img, args.slice)

print(f"File {args.fileName} converted, total of {i+1} images created with {args.slice} number of slices")