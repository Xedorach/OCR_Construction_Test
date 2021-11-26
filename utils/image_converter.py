from pdf2image import convert_from_path
import sys
import argparse
import os


# Image to PDF conversion script, takes 2 arguments: File name and output folder name

parser = argparse.ArgumentParser(description='convert pdf to images')
parser.add_argument('-f','--fileName', help="PDF File name", type=str, required=True)
parser.add_argument('-o','--output', help="Output directory", type=str, required=True)
parser.add_argument('-t','--threadCount', help="Output directory", type=int, const = 2)
args = parser.parse_args()
images = convert_from_path(args.fileName, dpi=300, thread_count = args.threadCount)

output_dir = os.path.join(os.getcwd(),args.output)
os.mkdir(output_dir)
os.chdir(output_dir) 

print(f"Converting file {args.fileName} from pdf to image .. please wait")


for i in range(len(images)):
    # Save pages as images in the pdf
    images[i].save('page' + str(i) + '.png', 'png')

print(f"File {args.fileName} converted, total of {i+1} images creates")