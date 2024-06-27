import re
import pyautogui
import cv2
import numpy

import glob
import time

import keyboard
import os

from threading import Thread

# Custom Variables
max_loop = 2
click_interval = 1
loop_interval = 1

def clickAndDragImage(image, threshold=0.5, drag_distance=(0, 0), drag_duration=0.5):
    """
    Search for the image on the screen, click on it, and drag the mouse by the specified distance.
    
    Parameters:
    - image: The path to the image file to search for on the screen.
    - threshold: The minimum similarity value to consider a match (default is 0.5).
    - drag_distance: A tuple (x, y) to specify how far to drag from the center of the image (default is (0, 0)).
    - drag_duration: Duration of the drag movement (default is 0.5 seconds).
    """
    
    # Take a screenshot
    screen_img = pyautogui.screenshot()
    screen_img_rgb = numpy.array(screen_img)
    
    # Convert screen image to grayscale
    screen_img_gray = cv2.cvtColor(screen_img_rgb, cv2.COLOR_BGR2GRAY)
    
    # Read the template image
    template = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]
    
    # Perform template matching
    res = cv2.matchTemplate(screen_img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    # If no image is found, return -1
    if max_val < threshold:
        return -1
    
    # Calculate the center of the matched area
    center_x = max_loc[0] + w / 2
    center_y = max_loc[1] + h / 2
    
    # Move the mouse to the center of the matched image
    pyautogui.moveTo(center_x, center_y, duration=0.2, tween=pyautogui.easeOutQuad)
    
    # Click at the center
    # pyautogui.click()
    
    # Drag the mouse by the specified distance
    end_x = center_x + drag_distance[0]
    end_y = center_y + drag_distance[1]
    pyautogui.dragTo(end_x, end_y, duration=drag_duration, button='left', tween=pyautogui.easeOutQuad)
    
    return 0

# search and click image in the center
def clickImage(image, threshold=0.5):

    # grab windows print screen
    screen_img = pyautogui.screenshot() 

    screen_img_rgb = numpy.array(screen_img)
    
    # convert screen img to grayscale
    screen_img_gray = cv2.cvtColor(screen_img_rgb, cv2.COLOR_BGR2GRAY) 
    
    # read image
    template = cv2.imread(image,cv2.IMREAD_GRAYSCALE)
    template.shape[::-1]

    # search for matching image in screen
    res = cv2.matchTemplate(screen_img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)    
    
    # no image is found 
    if max_val < threshold:
        return -1;
    
    # move mouse to center of image    
    pyautogui.moveTo(max_loc[0]+template.shape[1]/2, max_loc[1]+template.shape[0]/2, 0.5, pyautogui.easeOutQuad)    
        
    # left click   
    pyautogui.click()     
    return 0;    

#main thread
def main():
    loop = 0    
    time.sleep(1) 
    while loop < max_loop:
        # Search and sort images in input_images folder
        files = glob.glob("./setting/*.png")
        sorted_files = sorted(files, key=lambda x: int(re.search(r"(\d+)", os.path.basename(x)).group()))
        for file in sorted_files:
            print("File: " + file)
            substring = "12_book.png"
            ret = 0
            if substring in file:
                print(f"'{substring}' found in the string.")
                time.sleep(2)
                ret = clickAndDragImage(file, threshold=0.5, drag_distance=(0, -200), drag_duration=0.5)
            else:
                print(f"'{substring}' not found.")
                ret = clickImage(file)
            if ret == -1:
                loop = max_loop
                break
            time.sleep(click_interval)
        loop += 1
        time.sleep(loop_interval)
    
    os._exit(0)    

#interrupt thread
def key_listener():
    if keyboard.read_key() == "esc":
        print("Interrupted")
        os._exit(0)
        
try:
    print("Press 'Escape' to quit this application anytime")

    thread1 = Thread(target = main)
    thread2 = Thread(target = key_listener)
    
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    
except:
    print ("Exiting")
    os._exit(0)


 
