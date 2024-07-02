import re
import pyautogui
import cv2
import numpy as np
import time
import keyboard
import os
import logging
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Custom Variables
click_interval = 1  # Delay after clicking
check_interval = 1  # Delay between checks
restart_interval = 600  # Time to restart monitoring thread (in seconds)
three_image = "./setting/1_three.png"
sure_image = "./setting/2_sure.png"

# search and click image in the center
def clickImage2(image, threshold=0.5):

    # grab windows print screen
    screen_img = pyautogui.screenshot() 

    screen_img_rgb = np.array(screen_img)
    
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

def clickImage(image, threshold=0.5):
    """
    Search for the image on the screen and click on it.
    """
    try:
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
            logging.info(f"No match found for {image}, max_val: {max_val}")
            return -1
        
        # Calculate the center of the matched area
        center_x = max_loc[0] + w / 2
        center_y = max_loc[1] + h / 2
        
        # Move the mouse to the center of the matched image
        pyautogui.moveTo(center_x, center_y, duration=0.2, tween=pyautogui.easeOutQuad)
        
        # Click at the center
        pyautogui.click()
        
        return 0
    except Exception as e:
        logging.error(f"Error in clickImage: {e}")
        return -1

def monitorImages():
    try:
        while True:
            ret = clickImage2(three_image)
            if ret == 0:
                logging.info(f"{three_image} detected, clicking {sure_image}.")
                time.sleep(3)
                clickImage2(sure_image)
                time.sleep(click_interval)  # Delay after action to avoid rapid triggering
            time.sleep(check_interval)  # Delay between checks to reduce CPU usage
    except Exception as e:
        logging.error(f"Exiting monitor due to an error: {e}")
        os._exit(0)

def key_listener():
    try:
        while True:
            if keyboard.read_key() == "esc":
                logging.info("Interrupted by user.")
                os._exit(0)
    except:
        logging.error("Key listener encountered an error.")

def restart_monitor():
    global monitor_thread
    while True:
        time.sleep(restart_interval)
        if monitor_thread.is_alive():
            logging.info("Restarting monitor thread.")
            monitor_thread.join()
            monitor_thread = Thread(target=monitorImages)
            monitor_thread.start()

try:
    logging.info("Press 'Escape' to quit this application anytime")

    monitor_thread = Thread(target=monitorImages)
    key_listener_thread = Thread(target=key_listener)
    restart_thread = Thread(target=restart_monitor)

    monitor_thread.start()
    key_listener_thread.start()
    restart_thread.start()
    
    monitor_thread.join()
    key_listener_thread.join()
    restart_thread.join()

except Exception as e:
    logging.error(f"Exiting due to an error: {e}")
    os._exit(0)
