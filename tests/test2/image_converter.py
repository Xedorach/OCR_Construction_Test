from pdf2image import convert_from_path
import sys
import argparse
import os

parser = argparse.ArgumentParser(description='convert pdf to images')
parser.add_argument('filePath')
args = parser.parse_args()
images = convert_from_path(args.filePath)

output_dir = os.path.join(os.getcwd(),"Output_images")
os.mkdir(output_dir)
os.chdir(output_dir) 

print(f"Converting file {args.filePath} from pdf to image .. please wait")


for i in range(len(images)):
    # Save pages as images in the pdf
    images[i].save('page' + str(i) + '.jpg', 'JPEG')

print(f"File {args.filePath} converted, total of {i} images creates")