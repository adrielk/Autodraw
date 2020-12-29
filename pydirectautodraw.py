# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 23:30:55 2020

@author: Adriel Kim

Desc: Simple image printer.
Use: - Add line drawing of choice and name it "test.png"
     - Place cursor at top left corner of canvas
     - Program will run automatically after 5 seconds, and draw the image pixel by pixel

Future features:
        1. Easy image loading/browsing through your files
        2. Automated image process (black and white, linear convoluton)
        3. Axis display for alignment
        4. Pausing
        5. Real-time resolution slider display
        6. Time estimation
        7. Smooth and optimize with dragging and interpolation
        8. Robotic marker drawer integration
"""

import pyautogui as pa
import pydirectinput as pd
import time
import numpy
from PIL import Image

basewidth = 300
#put ur image name here
image = Image.open('test.png').convert('L')

ratio = image.size[1]/image.size[0]
hsize = int(float(ratio*basewidth))
image = image.resize((basewidth, hsize))
data = numpy.array(image)

image.save("resized.png")

time.sleep(5)


#currentMouseX, currentMouseY = pa.position()
inc = 1


newline_inc = 0  
new_y_inc = 0

for i in range(0, data.shape[0]):
    k = 0
    move_inc = 0
    first_dot = True
    while(k < data.shape[1]):
        if(data[i][k]<180):
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
    
   
    
    


    
        
    
    

    