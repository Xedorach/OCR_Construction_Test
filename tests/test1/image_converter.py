from pdf2image import convert_from_path
import sys
import argparse
import os

parser = argparse.ArgumentParser(description='convert pdf to images')
parser.add_argument('-f','--fileName', help="PDF File name", type=str, required=True)
parser.add_argument('-o','--output', help="Output directory", type=str, required=True)
args = parser.parse_args()
images = convert_from_path(args.fileName, args.output)

output_dir = os.path.join(os.getcwd(),args.output)
os.mkdir(output_dir)
os.chdir(output_dir) 

print(f"Converting file {args.fileName} from pdf to image .. please wait")


for i in range(len(images)):
    # Save pages as images in the pdf
    images[i].save('page' + str(i) + '.png', 'png')

