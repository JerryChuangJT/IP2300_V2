import tkinter as tk
from tkinter import ttk

class SmartTooltip:
    def __init__(self, widget, text, hover_delay=300):
        self.widget = widget
        self.text = text
        self.delay = hover_delay
        self.tooltip_window = None
        self.show_timer = None
        
        # 綁定事件
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)
    
    def on_enter(self, event):
        self.schedule_show()
    
    def on_leave(self, event):
        self.cancel_show()
        self.hide_tooltip()
    
    def on_motion(self, event):
        # 滑鼠移動時重新調度顯示
        self.cancel_show()
        self.schedule_show()
    
    def schedule_show(self):
        self.cancel_show()
        self.show_timer = self.widget.after(self.delay, self.show_tooltip)
    
    def cancel_show(self):
        if self.show_timer:
            self.widget.after_cancel(self.show_timer)
            self.show_timer = None
    
    def show_tooltip(self):
        if self.tooltip_window:
            return
        
        # 獲取滑鼠位置和螢幕尺寸
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty()
        widget_width = self.widget.winfo_width()
        widget_height = self.widget.winfo_height()
        
        # 創建 tooltip 視窗
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_attributes("-topmost", True)
        
        # 創建標籤
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10),
            wraplength=300,  # 自動換行
            justify="left"
        )
        label.pack()
        
        # 更新幾何資訊以獲取 tooltip 尺寸
        self.tooltip_window.update_idletasks()
        tooltip_width = self.tooltip_window.winfo_reqwidth()
        tooltip_height = self.tooltip_window.winfo_reqheight()
        
        # 獲取螢幕尺寸
        screen_width = self.widget.winfo_screenwidth()
        screen_height = self.widget.winfo_screenheight()
        
        # 智能定位邏輯
        # 預設位置：元件右下角
        tooltip_x = x + widget_width 
        tooltip_y = y + widget_height 
        
        # 檢查右邊是否超出螢幕
        if tooltip_x + tooltip_width > screen_width:
            tooltip_x = x - tooltip_width - 5  # 移到左邊
        
        # 檢查下方是否超出螢幕
        if tooltip_y + tooltip_height > screen_height:
            tooltip_y = y - tooltip_height - 5  # 移到上方
        
        # 確保不會超出螢幕邊界
        tooltip_x = max(0, min(tooltip_x, screen_width - tooltip_width))
        tooltip_y = max(0, min(tooltip_y, screen_height - tooltip_height))
        
        # 設置 tooltip 位置
        self.tooltip_window.wm_geometry(f"+{tooltip_x}+{tooltip_y}")
    
    def hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None