import cv2
import pytesseract
from matplotlib import pyplot as plt
import os
import argparse
from pdf2image import convert_from_path

# Fix parser to take output path properly
# check why OCR breaks in loop

parser = argparse.ArgumentParser(description='convert pdf to images')
parser.add_argument('-f','--fileName', help="PDF File name", type=str, required=True)
parser.add_argument('-o','--output', help="Output directory", type=str, required=True)
parser.add_argument("-v", "--verbose", help="show output",
                    action="store_true")
args = parser.parse_args()
images = convert_from_path(args.fileName)

output_dir = os.path.join(os.getcwd(), args.output)
os.mkdir(output_dir)
os.chdir(output_dir) 

print(f"Converting file {args.fileName} from pdf to image .. please wait")

for i in range(len(images)):
    # Save pages as images in the pdf
    images[i].save('page' + str(i) + '.jpg', 'JPEG')
    image = cv2.imread(f'page{i}.jpg')
    h, w, c = image.shape
    boxes = pytesseract.image_to_boxes(image)

    for b in boxes.splitlines():
        b = b.split(' ')
        image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    b,g,r = cv2.split(image)
    rgb_img = cv2.merge([r,g,b])
    txt = pytesseract.image_to_string(image)
    print("\n --------------- \n Output \n ---------------")
    print(txt)
    directory = os.path.join(os.getcwd(), f'output {i}')
    with open(directory+".txt",'w') as f: f.write(str(txt))


    if args.verbose:
        plt.figure(figsize=(16, 12))
        plt.imshow(rgb_img)
        plt.title('PyTesseract test')
        plt.show()

print(f"File {args.fileName} converted, total of {i} images created")


