import re
import pyautogui
import cv2
import numpy as np
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
    """
    # Take a screenshot
    screen_img = pyautogui.screenshot()
    screen_img_rgb = np.array(screen_img)
    
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
    
    # Drag the mouse by the specified distance
    end_x = center_x + drag_distance[0]
    end_y = center_y + drag_distance[1]
    pyautogui.dragTo(end_x, end_y, duration=drag_duration, button='left', tween=pyautogui.easeOutQuad)
    
    return 0

def clickImage(image, threshold=0.5):
    """
    Search for the image on the screen and click on it.
    """
    # Grab the screen
    screen_img = pyautogui.screenshot()
    screen_img_rgb = np.array(screen_img)
    
    # Convert screen image to grayscale
    screen_img_gray = cv2.cvtColor(screen_img_rgb, cv2.COLOR_BGR2GRAY)
    
    # Read the template image
    template = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    
    # Perform template matching
    res = cv2.matchTemplate(screen_img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    # If no image is found, return -1
    if max_val < threshold:
        return -1
    
    # Move the mouse to the center of the matched image
    center_x = max_loc[0] + template.shape[1] / 2
    center_y = max_loc[1] + template.shape[0] / 2
    pyautogui.moveTo(center_x, center_y, duration=0.5, tween=pyautogui.easeOutQuad)
    
    # Click at the center
    pyautogui.click()
    
    return 0

def main():
    loop = 0
    time.sleep(1)
    while loop < max_loop:
        # Search and sort images in input_images folder
        files = glob.glob("./lian/*.png")
        sorted_files = sorted(files, key=lambda x: int(re.search(r"(\d+)", os.path.basename(x)).group()))
        
        for file in sorted_files:
            print("File: " + file)
            ret = clickImage(file)
            if ret == -1:
                loop = max_loop
                break
            time.sleep(click_interval)
        
        loop += 1
        time.sleep(loop_interval)
    
    os._exit(0)

def key_listener():
    try:
        while True:
            if keyboard.read_key() == "esc":
                print("Interrupted")
                os._exit(0)
    except:
        print("Key listener encountered an error.")

try:
    print("Press 'Escape' to quit this application anytime")

    thread1 = Thread(target=main)
    thread2 = Thread(target=key_listener)
    
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

except Exception as e:
    print(f"Exiting due to an error: {e}")
    os._exit(0)
