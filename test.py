import random
import cv2
import pyautogui
import numpy as np
import time

# 找到所有指定图像位置的函数
def find_all_images_on_screen(image_path, threshold=0.6):
    screen = pyautogui.screenshot()
    screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)  # 保持屏幕截图为彩色图像

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)  # 读取模板图像为彩色
    template_h, template_w = template.shape[:2]

    res = cv2.matchTemplate(screen_np, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    positions = [(int(pt[0] + template_w // 2), int(pt[1] + template_h // 2)) for pt in zip(*loc[::-1])]
    
    return positions

# 找到指定图像位置的函数（使用指定阈值）
def find_image_on_screen(image_path, threshold=0.4):
    screen = pyautogui.screenshot()
    screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)  # 保持屏幕截图为彩色图像

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)  # 读取模板图像为彩色

    res = cv2.matchTemplate(screen_np, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val, max_val)
    if max_val >= threshold:  # 仅在匹配值超过阈值时返回位置
        top_left = max_loc
        return (top_left[0] + template.shape[1] // 2, top_left[1] + template.shape[0] // 2)
    else:
        return None
# 等待函数
def sleep(min_seconds, max_seconds):
    sleep_time = random.uniform(min_seconds, max_seconds)  # 使用 float 随机等待时间
    if sleep_time < 0:
        return
    time.sleep(sleep_time)

# 主程序
def main():
    # 等待雷电模拟器启动和游戏加载
    sleep(1, 5)
    while True:
        sleep(1, 5)
        xue_path = 'resources/chuangci/xue.png'  # 替换为你的图标文件路径
        xue_pos = find_image_on_screen(xue_path)
        ciyi_path = 'resources/chuangci/ciyi2.png'  # 替换为你的图标文件路径
        ciyi_pos = find_image_on_screen(ciyi_path)
        lian_path = 'resources/chuangci/lianxi2.png'  # 替换为你的图标文件路径
        lian_pos = find_image_on_screen(lian_path)
        print(xue_pos)
        print(ciyi_pos)
        print(lian_pos)
        if xue_pos:
            #学习模式
            sleep(1, 5)
            print("学习模式")
            xuexiicon = 'resources/chuangci/zzc.png'  # 替换为你的图标文件路径
            target_positions = find_all_images_on_screen(xuexiicon)
            print(target_positions)  # 打印所有匹配的位置
            for pos in target_positions:
                pyautogui.moveTo(pos)
                pyautogui.click(pos)
                sleep(2, 5)  # 随机等待以模拟真实的用户行为
        if ciyi_pos:
            #练习模式
            sleep(1, 5)
            print("词意模式")
            lianxiicon = 'resources/chuangci/list_bg_0.png'  # 替换为你的图标文件路径
            target_positions = find_all_images_on_screen(lianxiicon)
            print(target_positions)  # 打印所有匹配的位置
            for pos in target_positions:
                pyautogui.moveTo(pos)
                pyautogui.click(pos)
                sleep(0.5, 1.5)  # 随机等待以模拟真实的用户行为
        if lian_pos:
            #练习模式
            sleep(1, 5)
            print("练习模式")
            # 图标文件路径列表
            lian_paths = [
                'resources/chuangci/wordbg_2.png',  # 替换为你的图标文件路径
                'resources/chuangci/wordbg_3.png',  # 替换为你的图标文件路径
                'resources/chuangci/wordbg_4.png'   # 替换为你的图标文件路径
            ]
            all_positions = []  # 存储所有找到的位置
        
            for icon_path in lian_paths:
                target_positions = find_all_images_on_screen(icon_path)
                print(f"Positions for {icon_path}: {target_positions}")  # 打印所有匹配的位置
                all_positions.extend(target_positions)  # 将找到的位置添加到总列表中
            
            for pos in all_positions:
                pyautogui.moveTo(pos)
                pyautogui.click(pos)
                sleep(0.5, 1.5)  # 随机等待以模拟真实的用户行为

# 执行主程序
if __name__ == "__main__":
    main()
