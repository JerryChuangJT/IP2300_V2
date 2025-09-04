from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import ctypes


def get_system_background_color():
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
    img = Image.open(image_path).convert("RGBA").resize(size, Image.LANCZOS)
    background = Image.new("RGBA", img.size, bg_color + (0,))    
    return Image.alpha_composite(background, img)

class Button(ttk.Button):
    _style_inited = False

    def __init__(self, master, image_path:str=None, text:str=None, size:tuple=(30,30), **kwargs):
        if not Button._style_inited:
            style = ttk.Style()
            style.configure("Icon_ClassButton.Toolbutton", padding=3.5, borderwidth=0, relief="flat")
            Button._style_inited = True

        if text:
            super().__init__(master, text=text, cursor="hand2", style="Custom.TButton", takefocus=True, **kwargs)
        else:
            bg_color = get_system_background_color()
            self._images = self.create_hover_images(image_path, size, bg_color, master)
            super().__init__(master, image=self._images['normal'], style="Icon_ClassButton.Toolbutton", cursor="hand2", takefocus=True, **kwargs)
            self.bind_hover_effect()

    @staticmethod
    def create_hover_images(image_path:str, size:tuple, bg_color:tuple, master)->dict:
        normal_img = composite_to_background(image_path, size, bg_color)
        hover_img = composite_to_background(image_path, size, bg_color)
        pressed_img = ImageEnhance.Brightness(normal_img).enhance(1)

        return {'normal': ImageTk.PhotoImage(normal_img, master=master),
                'hover': ImageTk.PhotoImage(hover_img, master=master),
                'pressed': ImageTk.PhotoImage(pressed_img, master=master)}

    def bind_hover_effect(self):
        imgs = self._images
        self.config(image=imgs['normal'])
        self.bind("<Enter>", lambda e: self.config(image=imgs['hover']))
        self.bind("<Leave>", lambda e: self.config(image=imgs['normal']))
        self.bind("<ButtonPress-1>", lambda e: self.config(image=imgs['pressed']))
        self.bind("<ButtonRelease-1>", lambda e: self.config(image=imgs['hover']))
        self.bind("<FocusIn>", lambda e: self.config(image=imgs['hover']))
        self.bind("<FocusOut>", lambda e: self.config(image=imgs['normal']))

if __name__ == "__main__":
    width = 300
    height = 300

    root = tk.Tk()
    root.title("Test")
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.resizable(True, True)

    image_path = r"D:\Jerry\Project\Git\IP2300\V2\img\selectall.png"
    button = Button(root, image_path=image_path, size=(40, 40))
    button.grid(column=0, row=0, padx=90, pady=90)

    root.mainloop()