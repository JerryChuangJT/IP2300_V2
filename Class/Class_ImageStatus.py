"""
純粹顯示圖片的 Label 元件
支援正常和禁用兩種視覺狀態
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance
import ctypes

def get_system_background_color():
    """獲取系統背景顏色"""
    try:
        COLOR_BUTTONFACE = 15
        col = ctypes.windll.user32.GetSysColor(COLOR_BUTTONFACE)
        r = col & 0xff
        g = (col >> 8) & 0xff
        b = (col >> 16) & 0xff
        return (r, g, b)
    except Exception:
        return (240, 240, 240)

def composite_to_background(image_path, size, bg_color):
    """將圖片合成到背景色上"""
    img = Image.open(image_path).convert("RGBA").resize(size, Image.LANCZOS)
    background = Image.new("RGBA", img.size, bg_color + (0,))    
    return Image.alpha_composite(background, img)

class ImageDisplay(ttk.Label):
    """純粹顯示圖片的元件，支援正常和禁用狀態"""
    
    def __init__(self, master, image_path: str, size: tuple = (30, 30), **kwargs):
        self.image_path = image_path
        self.size = size
        self.bg_color = get_system_background_color()
        self.status = 'not_schedule'
        
        ### 創建兩種狀態的圖片
        self._images = self._create_state_images()
        
        ### 初始化為正常狀態
        super().__init__(master, image=self._images['normal'], **kwargs)
        
        ### 儲存圖片引用避免被垃圾回收
        self.image = self._images['normal']
    
    def _create_state_images(self) -> dict:
        """創建正常和禁用狀態的圖片"""
        ### 正常狀態圖片
        normal_img = composite_to_background(self.image_path, self.size, self.bg_color)
        
        # ### 禁用狀態圖片 - 降低亮度和對比度，增加灰度效果
        # disabled_img = composite_to_background("./img/fail.png", self.size, self.bg_color)
        # disabled_img = ImageEnhance.Brightness(disabled_img).enhance(0.6)  # 降低亮度
        # disabled_img = ImageEnhance.Contrast(disabled_img).enhance(0.6)    # 降低對比度

        ### 禁用狀態圖片 - 降低亮度和對比度，增加灰度效果
        disabled_img = normal_img.copy()
        disabled_img = ImageEnhance.Brightness(disabled_img).enhance(0.6)  # 降低亮度
        disabled_img = ImageEnhance.Contrast(disabled_img).enhance(0.6)    # 降低對比度
        r, g, b, a = disabled_img.split()
        gray = Image.merge('RGB', (r, g, b)).convert('L')
        gray_img = Image.merge('RGBA', (gray, gray, gray, a))  # 保持原始 Alpha
        disabled_img = Image.blend(disabled_img, gray_img, 0.7)

        ### 未在Schedule狀態
        not_schedule_img = composite_to_background("./img/notschedule.png", self.size, self.bg_color)
        not_schedule_img = ImageEnhance.Brightness(not_schedule_img).enhance(3.0)   # 降低亮度
        not_schedule_img = ImageEnhance.Contrast(not_schedule_img).enhance(0.1)     # 降低對比度
        
        # # 方法2: 轉換為灰階然後混合
        # gray_img = disabled_img.convert('L').convert('RGBA')
        # disabled_img = Image.blend(disabled_img, gray_img, 0.8)  # 60% 灰階混合
        
        return {
            'normal': ImageTk.PhotoImage(normal_img),
            'disabled': ImageTk.PhotoImage(disabled_img),
            'not_schedule': ImageTk.PhotoImage(not_schedule_img)
        }
    
    def set_enabled(self, enabled: str):
        """設定元件狀態"""
        self._enabled = enabled
        if enabled == "normal":
            self.config(image=self._images['normal'])
            self.image = self._images['normal']
        elif enabled == "disabled":
            self.config(image=self._images['disabled'])
            self.image = self._images['disabled']
        elif enabled == "not_schedule":
            self.config(image=self._images['not_schedule'])
            self.image = self._images['not_schedule']
    