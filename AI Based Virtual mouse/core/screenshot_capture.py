import pyautogui
import time

def take_screenshot():
    time.sleep(1)  # Thoda time wait karega capture ke liye
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
