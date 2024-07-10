import os
import pyautogui
import cv2
import numpy as np
import time
import logging
from threading import Thread
from pynput import keyboard

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# Custom Variables
click_interval = 1  # Delay after clicking
check_interval = 1  # Delay between checks
restart_interval = 600  # Time to restart monitoring thread (in seconds)
activity_interval = 300  # Interval to click activity_image (in seconds)
three_image = "./setting/sure.png"
sure_image = "./setting/content.png"
activity_image = "./setting/activity.png"
shangfa = "./setting/shangfa.png"
scroll_image = "./setting/scroll.png"
goActivity = "./setting/goActivity.png"
close_activity = "./setting/close.png"
# Flag to control the running state of the script
running = True

def clickImage(image, threshold=0.7):
    try:
        screen_img = pyautogui.screenshot()
        screen_img_rgb = np.array(screen_img)
        screen_img_gray = cv2.cvtColor(screen_img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(screen_img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val < threshold:
            logging.info(f"No match found for {image}, max_val: {max_val}")
            return -1

        center_x = max_loc[0] + w / 2
        center_y = max_loc[1] + h / 2
        pyautogui.moveTo(center_x, center_y, duration=0.5, tween=pyautogui.easeOutQuad)
        pyautogui.click()
        return 0
    except Exception as e:
        logging.error(f"Error in clickImage: {e}")
        return -1

def clickAndDragImage(image, threshold=0.7, drag_distance=(0, -200), drag_duration=0.5):
    try:
        screen_img = pyautogui.screenshot()
        screen_img_rgb = np.array(screen_img)
        screen_img_gray = cv2.cvtColor(screen_img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(screen_img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val < threshold:
            logging.info(f"No match found for {image}, max_val: {max_val}")
            return -1

        center_x = max_loc[0] + w / 2
        center_y = max_loc[1] + h / 2
        pyautogui.moveTo(center_x, center_y, duration=0.5, tween=pyautogui.easeOutQuad)
        pyautogui.dragRel(drag_distance[0], drag_distance[1], duration=drag_duration, button='left')
        return 0
    except Exception as e:
        logging.error(f"Error in clickAndDragImage: {e}")
        return -1

def monitorImages():
    global running
    try:
        while running:
            ret = clickImage(three_image)
            if ret == 0:
                logging.info(f"{three_image} detected, clicking {sure_image}.")
                clickImage(sure_image)
                time.sleep(click_interval)
            time.sleep(check_interval)
    except Exception as e:
        logging.error(f"Exiting monitor due to an error: {e}")
        os._exit(0)

def activityClicker():
    global running
    try:
        while running:
            clickImage(activity_image)
            time.sleep(click_interval)
            ret = clickImage(shangfa)
            while ret != 0 and running:
                clickAndDragImage(scroll_image, threshold=0.7, drag_distance=(0, -200), drag_duration=0.5)
                ret = clickImage(shangfa)
            time.sleep(click_interval)
            ret = clickImage(goActivity)
            time.sleep(activity_interval)
    except Exception as e:
        logging.error(f"Exiting activity clicker due to an error: {e}")
        os._exit(0)

def restart_monitor():
    global monitor_thread, activity_thread
    while running:
        time.sleep(restart_interval)
        if not monitor_thread.is_alive():
            logging.info("Restarting monitor thread.")
            monitor_thread.join()
            monitor_thread = Thread(target=monitorImages)
            monitor_thread.start()
        if not activity_thread.is_alive():
            logging.info("Restarting activity thread.")
            activity_thread.join()
            activity_thread = Thread(target=activityClicker)
            activity_thread.start()

def on_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        logging.info("Exiting...")
        os._exit(0)

try:
    logging.info("Press 'Escape' to quit this application anytime")

    monitor_thread = Thread(target=monitorImages)
    activity_thread = Thread(target=activityClicker)
    monitor_thread.start()
    activity_thread.start()

    restart_thread = Thread(target=restart_monitor)
    restart_thread.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    monitor_thread.join()
    activity_thread.join()
    restart_thread.join()

except Exception as e:
    logging.error(f"Exiting due to an error: {e}")
    os._exit(0)
