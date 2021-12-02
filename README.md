# OCR_Construction_Test
OCR on different construction documents using different models. 
More details will be added later.
## Dependencies:
Dependency installations using conda, figure out how to do it for your platform for now.
note: It only works with python 3.7, going higher will result in dependency clash between image2pdf and easyocr

**Pytesseract**

conda install -c conda-forge tesseract

**Popper**

conda install -c conda-forge poppler

**CUDA**

Cuda 11.3, find it for your system 

**Pytorch**

conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch

Dont forget to add the stuff to your path, better documentation will be added as the project grows
