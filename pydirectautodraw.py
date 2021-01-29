# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 23:30:55 2020

@author: Adriel Kim

Desc: An automated line art printer

Use: - Execute program in command line like so: python pydirectauthdraw.py image_name_here
        -Note: image must be placed in "photos" directory
     - Place cursor at top left corner of canvas of a program such as Microsoft Paint
     - Program will run automatically after 5 seconds, and draw the image as lineart pixel by pixel

Future features:
        3. Axis display for alignment
        4. Pausing
        5. Real-time resolution slider display
        7. Smooth and optimize with dragging and interpolation
"""
import sys
import os
import pyautogui as pa
import pydirectinput as pd
import time
import numpy
import cv2
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

def wait(seconds):
    for i in range(seconds, 0, -1):
        print("Countdown: ", i)
        time.sleep(1)

# def dodge(image, mask):
#     max_array = numpy.full_like(image, 255)
#     mask_div = numpy.divide(image, (max_array - mask))
#     mask_processed = numpy.interp(mask_div,(mask_div.min(), mask_div.max()), (0, 255))
#     #image_processed = max_array - image    
#     return mask_processed 

def dodgeCV2(image,mask):
    img_cv2 = numpy.asarray(image)
    mask_cv2 = numpy.asarray(mask)
    cv2_img = cv2.divide(img_cv2, 255-mask_cv2, scale=256)
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    img_final = imgEnhance(Image.fromarray(cv2_img))
    return img_final

# def burn(image, mask):
#     max_array = numpy.full_like(image, 255)
#     image_processed = max_array - image
#     mask_processed = max_array - mask
#     div_img = numpy.divide(image_processed, mask_processed)
#     div_img_scaled = numpy.interp(div_img, (div_img.min(), div_img.max()), (0, 256))

#     final_img = max_array-div_img_scaled
#     return final_img

def imgEnhance(image):
    image_sharp = ImageEnhance.Sharpness(image).enhance(5)
    image_dim = ImageEnhance.Brightness(image_sharp).enhance(0.9)
    image_enhanced = ImageEnhance.Contrast(image_dim).enhance(5)
    return image_enhanced


def imgProcess(image):
    gray_img = ImageOps.grayscale(image)
    inverted_img = ImageOps.invert(gray_img)
    blur_img = inverted_img.filter(ImageFilter.GaussianBlur(10))
    #final_img = Image.blend(blur_img, gray_img, -0.5)
    
    #final_img_burn = Image.fromarray(burn(numpy.asarray(gray_img), numpy.asarray(blur_img)).astype(numpy.uint8))
    #final_img_dodge = Image.fromarray(dodge(numpy.asarray(gray_img), numpy.asarray(blur_img)).astype(numpy.uint8))
    final_img = dodgeCV2(gray_img, blur_img)
    #final_img = Image.blend(final_img_burn, final_img_dodge, 1.5)
    return final_img

def getTimeEstimate(img, pause, threshold):
    bool_matrix = numpy.where(img > threshold, 0, 1)
    pixel_count = numpy.sum(bool_matrix)
    #print(pixel_count, "vs.", img.size)
    time_minutes = (pixel_count*pause)/60.0
    return time_minutes

def main(argv):

    photo_path = str(os.getcwd())+"/photos"
    os.chdir(photo_path)
    #print(os.getcwd())

    #Settings
    pause_time = 0.01 
    basewidth = 300 #width of base of image
    tolerance_percent = .70 #darkness level of a pixel required to draw.
    pd.PAUSE = pause_time
    
    image = Image.open(str(argv[0])).convert('L')
    ratio = image.size[1]/image.size[0]
    hsize = int(float(ratio*basewidth))
    image = image.resize((basewidth, hsize))
    tolerance = int(255*tolerance_percent)

    image = imgProcess(image).convert('L')
    image.save("resized.png")
    data = numpy.asarray(image)

    print_time = getTimeEstimate(data, pause_time*5, tolerance)
    print("Estimated print time: %.2f minutes"% (print_time))

    wait(5)

    #currentMouseX, currentMouseY = pa.position()
    inc = 1

    newline_inc = 0  
    new_y_inc = 0

    for i in range(0, data.shape[0]):
        k = 0
        move_inc = 0
        first_dot = True
        while(k < data.shape[1]):
            if(data[i][k]<tolerance):
                if(first_dot == True):
                    first_dot = False
                    pd.move(newline_inc+move_inc, new_y_inc)
                    newline_inc = 0
                    new_y_inc = 0
                else:
                    pd.move(move_inc, 0)
                pd.click()
                move_inc = 0
            
            move_inc += inc
            k+=1

        newline_inc += -(inc*basewidth)+move_inc
        new_y_inc += inc

if __name__ == "__main__":
    main(sys.argv[1:])
    #print(sys.argv[0])
    
   
    
    


    
        
    
    

    