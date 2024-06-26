import random
import cv2
import pyautogui
import numpy as np
import time

# 找到指定图像位置的函数
def find_image_on_screen(image_path):
    screen = pyautogui.screenshot()
    screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)  # 将屏幕截图转换为灰度图像

    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 直接读取模板图像为灰度图像

    res = cv2.matchTemplate(screen_np, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    return (top_left[0] + template.shape[1] // 2, top_left[1] + template.shape[0] // 2)

def sleep(min, max):
    sleepTime = random.randint(min, max)
    if sleepTime < 0:
        return
    time.sleep(sleepTime)

# 主程序
def main():
    # 等待雷电模拟器启动和游戏加载
    sleep(1,5)
    while True:
        sleep(1,5)
        icon_path = 'resources/chuangci/zzc.png'  # 替换为你的图标文件路径
        target_pos = find_image_on_screen(icon_path)
        print(target_pos)
        if target_pos:
            pyautogui.moveTo(target_pos)
            pyautogui.click(target_pos)
    

# 执行主程序
if __name__ == "__main__":
    main()
