import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage

import sys
import os
import traceback

from Function.Page_SetEnvironment import Page_SetEnvironment 
from Function.Page_SetBackup import Page_SetBackup

from Function.Frame_ADB import Frame_ADB
from Function.Frame_Client import Frame_Client
from Function.Frame_Wifi import Frame_Wifi
from Function.Frame_Script import Frame_Script
from Function.Frame_Schedule import Frame_Schedule

import Function.MyFunction_JsonData as JsonDataFunction

class MainPage():
    def __init__(self, root=None, version="0.0.0"):
        self.root = root
        self.version = version
        self.jsonpath_environment = "./Parameter/json_PageSetEnvironment.json"
        self.jsonfolder = JsonDataFunction.Get_jsonAllData(self.jsonpath_environment)["JsonFilePath"]
        self.controllerPCIP = JsonDataFunction.Get_jsonAllData(self.jsonpath_environment)["ControllerPCIP"]

        #---------------------------------------------------------------------
        width = 1000
        height = 700
        self.root.title(f"{self.version} MutipleClientsTesting    {self.jsonfolder}   {self.controllerPCIP}")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        self.root.resizable(True,True)
        # icon = PhotoImage(file="./img/television.png")
        # self.root.iconphoto(True, icon)

        self.Create_MenuBar()
        self.Create_NoteBook()
    
    ###=======================================================================================
    ###=======================================================================================
    ### Create the menu bar for the main window.
    def Create_MenuBar(self):
        MenuBar = tk.Menu(self.root)

        ### File Option.
        file_menu = tk.Menu(MenuBar, tearoff=0)
        MenuBar.add_cascade(label="Setting", menu=file_menu)
        file_menu.add_command(label="Environment", command=self.MenuButton_SetEnvironment)
        file_menu.add_command(label="Export JsonData", command=self.MenuButton_Export_JsonData)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        ### About Option.
        about_menu = tk.Menu(MenuBar, tearoff=0)
        MenuBar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="Instruction", command=self.MenuButton_OpenFile_Readme)
        
        self.root.config(menu=MenuBar)

    def MenuButton_SetEnvironment(self):
        def update_title_version():
            self.jsonfolder = JsonDataFunction.Get_jsonAllData(self.jsonpath_environment)["JsonFilePath"]
            self.controllerPCIP = JsonDataFunction.Get_jsonAllData(self.jsonpath_environment)["ControllerPCIP"]
            self.root.title(f"{self.version} MutipleClientsTesting    {self.jsonfolder}   {self.controllerPCIP}")

            self.app_adb.ReloadJsonData()
            self.app_client.ReloadJsonData()
            self.app_wifi.ReloadJsonData()
            self.add_script.ReloadJsonData()

        def on_window_close():
            update_title_version()
        
        try:
            json_frame = tk.Toplevel(self.root)
            json_frame.transient(self.root)  # 設定為主視窗的子視窗
            json_frame.grab_set()           # 設定為模態視窗
            json_frame.protocol("WM_DELETE_WINDOW", json_frame.destroy)
            app = Page_SetEnvironment(json_frame, version=self.version, close_callback=on_window_close)

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}")
            
    def MenuButton_Export_JsonData(self):
        try:
            backup_frame = tk.Toplevel(self.root)
            backup_frame.transient(self.root)
            backup_frame.grab_set()           # 設定為模態視窗
            backup_frame.protocol("WM_DELETE_WINDOW", backup_frame.destroy)
            app = Page_SetBackup(backup_frame, version=self.version)
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}")

    def MenuButton_OpenFile_Readme(self):
        try:
            ### Get current folder path.
            current_path = os.getcwd()
            current_path.replace('\\', '/')

            ### Open PDF File.
            file_path = f"{current_path}/Readme_GUIParameter.pdf" 
            os.startfile(file_path)
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}")

    ###=======================================================================================
    ###=======================================================================================
    ### Create the notebook.
    def Create_NoteBook(self):
        ### Create a style object
        ### Setting the theme to 'clam' for better border control.
        style = ttk.Style()
        style.theme_use('vista')
        style.map('TNotebook.Tab',
                 foreground=[('selected', 'black'),        # 選中時：黑色文字
                           ('active', 'black'),           # 懸停時：黑色文字
                           ('!active', "#9E9D9D")],       # 未選中：灰色文字
                 font=[('selected', ('Arial', 10, 'bold')), # 選中時：放大字體 + 粗體
                      ('!selected', ('Arial', 9))],       # 未選中：正常大小
                 focuscolor=[('selected', ''),             # 選中時：無焦點色
                           ('!selected', '')]             # 未選中：無焦點色
                )
        style.configure('TNotebook',
                       background='#f0f0f0')              # 背景顏色改為淺灰

        #-----------------------------------------------------------------------------------
        Notebook = {}

        ### Create the Notebook of MainPage.
        Notebook["MainPage"] = ttk.Notebook(self.root)
        self.Frame_MainPage = {}
        self.Frame_MainPage["Execution"] = tk.Frame(Notebook["MainPage"])

        self.Frame_MainPage["Schedule"] = tk.Frame(Notebook["MainPage"])
        self.app_schedule = Frame_Schedule(self.Frame_MainPage["Schedule"])

        self.Frame_MainPage["ADB"] = tk.Frame(Notebook["MainPage"])
        self.app_adb = Frame_ADB(self.Frame_MainPage["ADB"])

        self.Frame_MainPage["Setting"] = tk.Frame(Notebook["MainPage"])

        Notebook["MainPage"].add(self.Frame_MainPage["Execution"], text="Execution")
        Notebook["MainPage"].add(self.Frame_MainPage["Schedule"], text="Schedule")
        Notebook["MainPage"].add(self.Frame_MainPage["ADB"], text="ADB")
        Notebook["MainPage"].add(self.Frame_MainPage["Setting"], text="Setting")
        Notebook["MainPage"].pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        ### Create the Notebook of SettingPage.
        Notebook["SettingPage"] = ttk.Notebook(self.Frame_MainPage["Setting"])
        self.Frame_SettingPage = {}
        
        # self.Frame_SettingPage["ADB"] = tk.Frame(Notebook["SettingPage"])
        # self.app_adb = Frame_ADB(self.Frame_SettingPage["ADB"])

        self.Frame_SettingPage["Client"] = tk.Frame(Notebook["SettingPage"])
        self.app_client = Frame_Client(self.Frame_SettingPage["Client"])

        self.Frame_SettingPage["Wifi"] = tk.Frame(Notebook["SettingPage"])
        self.app_wifi = Frame_Wifi(self.Frame_SettingPage["Wifi"])

        self.Frame_SettingPage["Script"] = tk.Frame(Notebook["SettingPage"])
        self.add_script = Frame_Script(self.Frame_SettingPage["Script"])

        # Notebook["SettingPage"].add(self.Frame_SettingPage["ADB"], text="ADB")
        Notebook["SettingPage"].add(self.Frame_SettingPage["Client"], text="Client")
        Notebook["SettingPage"].add(self.Frame_SettingPage["Wifi"], text="Wifi")
        Notebook["SettingPage"].add(self.Frame_SettingPage["Script"], text="Script")

        Notebook["SettingPage"].pack(padx=0, pady=0, fill=tk.BOTH, expand=True)

if __name__ == "__main__":

    VERSION = "V2.0.0"
    root = tk.Tk()
    icon = PhotoImage(file="./img/television.png")
    root.iconphoto(True, icon)
    root.withdraw()  # 先隱藏主視窗

    # Page_SetEnvironment 用 Toplevel
    Page_Environment = tk.Toplevel(root)
    app = Page_SetEnvironment(Page_Environment, version=VERSION)
    Page_Environment.grab_set()
    Page_Environment.wait_window()  # 等待設定視窗關閉

    JsonPath_Environment = "./Parameter/json_PageSetEnvironment.json"
    JsonData_Environment = JsonDataFunction.Get_jsonAllData(JsonPath_Environment)
    
    ###==============================================================
    ### Check if the state is set to "Exit" in the JSON file.
    if JsonData_Environment["ImportCloseState"] == "Exit":
        sys.exit(0)  

    root.deiconify()
    FrameScript = MainPage(root, version=VERSION) 
    root.mainloop()
    

    