import tkinter as tk
from tkinter import filedialog, messagebox
from idlelib.tooltip import Hovertip  

import os
import traceback

import Function.MyFunction_JsonData as JsonDataFunction

from Class.Class_Button import Button

class Page_SetEnvironment():
    def __init__(self, root=None, version="V0.0.0", close_callback=None):
        self.JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.close_callback = close_callback  

        ### Initialize the main window.
        self.root = root
        height = 150
        width = 650
        self.root.title(f"{version} Evironment Setting")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        self.root.resizable(True, False)
  
        ### Initialize settings.
        self.Setting = {
            "Font": {
                "Title": ("Arial", 20, "bold"),
                "Label": ("Arial", 10),
                "Log": ("Arial", 10)
            },
            "Entry": {
                "background": "white",
                "readonlybackground": "light yellow"  # 使用淺黃色和淺綠色
            }
        }

        self.Image_path = {
            "Button_SelectFolder": "./Img/add_folder.png",
            "Button_Confirm": "./Img/check.png",
            "Button_Exit": "./Img/exit.png",
        }

        self.Create_Widgets()
        self.Set_DefaultData()

    def Create_Widgets(self):
        ### Create Frames.
        self.Frame = {}
        self.Frame["Main"] = tk.Frame(self.root, borderwidth = 1, relief = "flat", highlightbackground="#a9a7a7", highlightthickness=1)
        self.Frame["Main"].grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)  
        self.root.grid_columnconfigure(0, weight=1) 
    
        ### Initial Widgets.
        self.Main_Widget = {}
        self.Main_Widget["Label"] = {}
        self.Main_Widget["Entry"] = {}
        self.Main_Widget["Button"] = {}

        ### Create Elements.
        self.Main_Widget["Label"]["Title"] = tk.Label(self.Frame["Main"], text="SETTING", font=self.Setting["Font"]["Title"], foreground="blue")
        self.Main_Widget["Button"]["Confirm"] = Button(self.Frame["Main"], image_path=self.Image_path["Button_Confirm"], size=(32,32), command=self.Button_Confirm)
        self.Main_Widget["Button"]["Exit"] = Button(self.Frame["Main"], image_path=self.Image_path["Button_Exit"], size=(32,32), command=self.Button_Exit)
        
        self.Main_Widget["Label"]["JsonFolderPath"] = tk.Label(self.Frame["Main"], text="Json Folder Path :", font=self.Setting["Font"]["Label"] )
        self.Main_Widget["Label"]["ControllerPCIP"] = tk.Label(self.Frame["Main"], text="Controller PC IP :", font=self.Setting["Font"]["Label"] )
        self.Main_Widget["Entry"]["JsonFolderPath"] = tk.Entry(self.Frame["Main"], state="readonly", **self.Setting["Entry"])
        self.Main_Widget["Entry"]["ControllerPCIP"] = tk.Entry(self.Frame["Main"], state="normal", **self.Setting["Entry"])
        self.Main_Widget["Button"]["JsonFolderPath"] = Button(self.Frame["Main"], image_path=self.Image_path["Button_SelectFolder"], size=(20,20), command=self.Button_SelectFolder)


        ### Layout Elements.
        self.Main_Widget["Label"]["Title"].grid(row=0, column=0, padx=(5,3), pady=(5,0), sticky="w")
        self.Main_Widget["Button"]["Confirm"].grid(row=0, column=1, padx=(5, 5), pady=(7,0), sticky="se")
        self.Main_Widget["Button"]["Exit"].grid(row=0, column=2, padx=(0,5), pady=(7,0), sticky="se")

        self.Main_Widget["Label"]["JsonFolderPath"].grid(row=1, column=0, padx=(5,5), pady=(13,0), sticky="w")
        self.Main_Widget["Entry"]["JsonFolderPath"].grid(row=1, column=1, padx=(5,37), pady=(13,0), columnspan=2, sticky="ew")
        self.Main_Widget["Button"]["JsonFolderPath"].grid(row=1, column=2, padx=(0,5), pady=(13,0), sticky="e")  

        self.Main_Widget["Label"]["ControllerPCIP"].grid(row=2, column=0, padx=(5,5), pady=(5,5), sticky="w")
        self.Main_Widget["Entry"]["ControllerPCIP"].grid(row=2, column=1, padx=(5,5), pady=(5,5), columnspan=2, sticky="ew")

        self.Frame["Main"].grid_columnconfigure(1, weight=1) 
        self.Frame["Main"].grid_rowconfigure(2, weight=1) 

        ### Tooltips
        ToolTip = {
            "Button_Confirm": Hovertip(self.Main_Widget["Button"]["Confirm"], text='Confirm the setting.', hover_delay=300),
            "Button_Exit": Hovertip(self.Main_Widget["Button"]["Exit"], text='Exit and cancel the setting.', hover_delay=300),
            "Button_SelectFolder": Hovertip(self.Main_Widget["Button"]["JsonFolderPath"], text='Choose json folder path.', hover_delay=300),
        }
        
    def Set_DefaultData(self):
        jsonData = JsonDataFunction.Get_jsonAllData(self.JsonPath)
        self.FillEntry_Data(self.Main_Widget["Entry"]["JsonFolderPath"], jsonData["JsonFilePath"], "readonly")
        self.FillEntry_Data(self.Main_Widget["Entry"]["ControllerPCIP"], jsonData["ControllerPCIP"], "normal")
        JsonDataFunction.Update_jsonFileData(
            file_path=self.JsonPath,
            key_value="ImportCloseState",
            value="Exit"
        )   
    
    #===================================================================================================
    def Button_Confirm(self):
        ### Check if the folder exists and has content.
        def check_jsonfolder_exists(path:str)-> bool:
            if not path or path.strip() == "":
                messagebox.showerror("Error", "Please select a Json folder path.", parent=self.root)
                return False
            if not os.path.exists(path):
                messagebox.showerror("Error", f"The path does not exist:\n{path}", parent=self.root)
                return False
            return True
        
        ### Check if the folder has all json files.
        def check_jsonfolder_files(folder_path:str)-> bool:
            folder_path = folder_path.rstrip("/\\")
            required_files = [
                "json_Client.json",
                # "json_ManageScript.json", 
                "json_Script.json",
                "json_Wifi.json",
                "json_Schedule.json",
                "youtubeURL.txt"
            ]
            ### Check each file exists.
            for filename in required_files:
                file_path = os.path.join(folder_path, filename)
                if not os.path.isfile(file_path):
                    messagebox.showerror("Error", 
                                         "The JsonFile folder must contain:\n"
                                         "'json_Client.json'\n"
                                         "'json_Script.json'\n"
                                         "'json_Wifi.json'\n"
                                         "'json_ManageScript.json'\n"
                                         "'json_Schedule.json'\n"
                                         "'youtubeURL.txt'\n\n" 
                                         f"'{file_path}' is missing.",
                                         parent=self.root)
                    return False
            return True
        
        ### Check if the json file has all required keys.
        def check_jsonfile_data(folder_path:str)-> bool:
            client_key_data = ["ClientID", "MAC", "EtherIP", "Comment"]
            wifi_key_data = ["WifiID", "PingType", "DUTIP", "SSID", "Security", "Password", "BSSID", "Driver_Band", "Driver_Standard" ,"Driver_Channel", "Driver_Bandwidth"]
            script_key_data = ["ScriptID", "Type", "Parameter1", "Parameter2", "Parameter3", "Parameter4", "Parameter5", "Parameter6"]
            
            client_alldata:list = JsonDataFunction.Get_jsonAllData(folder_path + "json_Client.json")["Client"]
            wifi_alldata:list = JsonDataFunction.Get_jsonAllData(folder_path + "json_Wifi.json")["Wifi"]
            script_alldata:list = JsonDataFunction.Get_jsonAllData(folder_path + "json_Script.json")["Script"]

            for cleint_data in client_alldata:
                for key_data in client_key_data:
                    if key_data not in JsonDataFunction.Get_DictKey(cleint_data):
                        messagebox.showerror("Error", 
                                            f"json_Client.json data {cleint_data} error, Must contain:\n\n"
                                            "ClientID, MAC, EtherIP, Comment\n\n"
                                            f"Missing key '{key_data}'.", 
                                            parent=self.root)
                        return False
            
            for wifi_data in wifi_alldata:
                for key_data in wifi_key_data:
                    if key_data not in JsonDataFunction.Get_DictKey(wifi_data):
                        messagebox.showerror("Error", 
                                            f"json_Wifi.json data {wifi_data} error, Must contain:\n\n"
                                            "WifiID, PingType, DUTIP, SSID, Security, Password, BSSID, Driver_Band, Driver_Standard ,Driver_Channel, Driver_Bandwidth\n\n"
                                            f"Missing key '{key_data}'.", 
                                            parent=self.root)
                        return False
                    
            for script_data in script_alldata:
                for key_data in script_key_data:
                    if key_data not in JsonDataFunction.Get_DictKey(script_data):
                        messagebox.showerror("Error", 
                                            f"json_Script.json data {script_data} error, Must contain:\n\n"
                                            "TestSciptID, Type, Parameter1, Parameter2, Parameter3, Parameter4, Parameter5, Parameter6\n\n"
                                            f"Missing key '{key_data}'.", 
                                            parent=self.root)
                        return False
            
            return True
        
        try:
            ### Check the folder and update the JSON file.
            jsonfolder_path = self.Main_Widget["Entry"]["JsonFolderPath"].get().strip()
            controllerpc_ip = self.Main_Widget["Entry"]["ControllerPCIP"].get().strip()
            
            if check_jsonfolder_exists(jsonfolder_path) and check_jsonfolder_files(jsonfolder_path) and check_jsonfile_data(jsonfolder_path):
                JsonDataFunction.Update_jsonFileData(
                    file_path=self.JsonPath,
                    key_value="JsonFilePath",
                    value=jsonfolder_path
                )
                JsonDataFunction.Update_jsonFileData(
                    file_path=self.JsonPath,
                    key_value="ControllerPCIP",
                    value=controllerpc_ip.strip()
                )   
                JsonDataFunction.Update_jsonFileData(
                    file_path=self.JsonPath,
                    key_value="ImportCloseState",
                    value="Confirm"
                )   
                self.Exit_GUI()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)
            return

    def Button_SelectFolder(self):
        try:
            ### Select File Frame.
            folder_path = filedialog.askdirectory(title="Select Json Folder", parent=self.root)
            if folder_path != "":
                folder_path = folder_path + "/"
                self.FillEntry_Data(self.Main_Widget["Entry"]["JsonFolderPath"], folder_path, "readonly")

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)

    def Button_Exit(self):
        self.Exit_GUI()

    def Exit_GUI(self):
        if self.close_callback:
            self.close_callback()
        self.root.destroy()

    #===================================================================================================
    def FillEntry_Data(self, object_entry:object=None, data:str=None, state:str="readonly"):
        object_entry["state"] = "normal"
        object_entry.delete(0,tk.END)
        object_entry.insert(0, data)

        if state == "readonly":
            object_entry["state"] = "readonly"

if __name__ == "__main__":
    VERSION = "V2.0.0"
    root = tk.Tk()
    app= Page_SetEnvironment(root=root, version=VERSION)
    root.mainloop()