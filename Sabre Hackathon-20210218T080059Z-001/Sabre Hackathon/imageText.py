import cv2 
import pytesseract 
import time

def main(path):
    pytesseract.pytesseract.tesseract_cmd = 'D:/Program Files/Tesseract-OCR/tesseract.exe'      #set path to OCR
    img = cv2.imread(path)                                          #upload image file path
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    im2 = img.copy() 
    ret_string = ""
    for cnt in contours: 
        x, y, w, h = cv2.boundingRect(cnt) 
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2) 
        cropped = im2[y:y + h, x:x + w] 
        text = pytesseract.image_to_string(cropped)
        ret_string+= text                              #concatenate with newline delimiter
        
    print(ret_string.rstrip())
    return(ret_string.rstrip())
                                                         #return in string value
    