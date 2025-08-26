import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from tkinter import PhotoImage
from idlelib.tooltip import Hovertip  

import traceback
import time
from pathlib import Path
import shutil

import Function.MyFunction_JsonData as JsonDataFunction

from Class.Class_Button import Button

class Page_SetBackup():
    def __init__(self, root=None, version:str="V0.0.0", close_callback=None):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.SetBackup_JsonPath = "./Parameter/json_PageSetBackup.json"
        self.close_callback = close_callback  # 儲存關閉回調函數

        ### Initialize the main window.
        self.root = root
        height = 110
        width = 650
        self.root.title(f"{version} Json Path Exporter")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        self.root.resizable(True, False)

        ### Initialize settings.
        self.Setting = {
            "Font": {
                "Title": ("Arial", 20, "bold"),
                "Label": ("Arial", 10),
                "Log": ("Arial", 10)
            }
        }

        self.Image_path = {
            "Button_Export": "./Img/download.png",
            "Button_Exit": "./Img/exit.png",
            "Button_SelectFolder": "./Img/add_folder.png",
        }

        self.Create_Widgets()
        self.Set_DefaultData()

    def Create_Widgets(self):
        ### Create Frames.
        self.Frame = {}
        self.Frame["Main"] = tk.Frame(self.root, borderwidth=1, relief="flat", highlightbackground="#a9a7a7", highlightthickness=1)
        self.Frame["Main"].grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)  
        self.root.grid_columnconfigure(0, weight=1) 

        ### Initial Widgets.
        self.Main_Widget = {}
        self.Main_Widget["Label"] = {}
        self.Main_Widget["Entry"] = {}
        self.Main_Widget["Button"] = {}

        ### Create Elements.
        self.Main_Widget["Label"]["Title"] = tk.Label(self.Frame["Main"], text="BACKUP", font=self.Setting["Font"]["Title"], foreground="blue")
        self.Main_Widget["Button"]["Export"] = Button(self.Frame["Main"], image_path=self.Image_path["Button_Export"], size=(30,30), command=self.Button_Export)
        self.Main_Widget["Button"]["Exit"] = Button(self.Frame["Main"], image_path=self.Image_path["Button_Exit"], size=(30,30), command=self.Button_Exit)
    
        self.Main_Widget["Label"]["BackupFolderPath"] = tk.Label(self.Frame["Main"], text="Backup Folder Path:", font=self.Setting["Font"]["Label"])
        self.Main_Widget["Entry"]["BackupFolderPath"] = tk.Entry(self.Frame["Main"], state="readonly", readonlybackground="light yellow")
        self.Main_Widget["Button"]["BackupFolderPath"] = Button(self.Frame["Main"], image_path=self.Image_path["Button_SelectFolder"], size=(30,30), command=self.Button_SelectBackupFolder)
        
        ### Layout the Elements.
        self.Main_Widget["Label"]["Title"].grid(row=0, column=0, padx=(5,3), pady=(5,0), sticky="w")
        self.Main_Widget["Button"]["Export"].grid(row=0, column=1, padx=(5,5), pady=(7,0), sticky="se")
        self.Main_Widget["Button"]["Exit"].grid(row=0, column=2, padx=(0,5), pady=(7,0), sticky="se")
    
        self.Main_Widget["Label"]["BackupFolderPath"].grid(row=1, column=0, padx=(5,5), pady=(5,0), sticky="w")
        self.Main_Widget["Entry"]["BackupFolderPath"].grid(row=1, column=1, padx=(5,5), pady=(5,0), sticky="ew")
        self.Main_Widget["Button"]["BackupFolderPath"].grid(row=1, column=2, padx=(0,5), pady=(5,0), sticky="e")  

        self.Frame["Main"].grid_columnconfigure(1, weight=1) 

        ### Tooltips
        ToolTip = {
            "Button_Export": Hovertip(self.Main_Widget["Button"]["Export"], text='Download json datas to the backup folder.', hover_delay=300),
            "Button_Exit": Hovertip(self.Main_Widget["Button"]["Exit"], text='Exit and cancel the action.', hover_delay=300),
            "Button_SelectFolder": Hovertip(self.Main_Widget["Button"]["BackupFolderPath"], text='Choose backup folder path.', hover_delay=300),
        }

    def Set_DefaultData(self):
        jsonData = JsonDataFunction.Get_jsonAllData(self.SetBackup_JsonPath)
        self.FillEntry_Data(self.Main_Widget["Entry"]["BackupFolderPath"], jsonData["BackupPath"], "readonly")

    #===================================================================================================
    def Button_Export(self):
        try:
            jsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)
            jsonfolder_path = Path(jsonData["JsonFilePath"])
            destination_folder = Path(self.Main_Widget["Entry"]["BackupFolderPath"].get())
            
            ### Create Folder & File Name.
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_folder_name = f"JsonData_Backup_{timestamp}"
            backup_folder_path = destination_folder / backup_folder_name
            
            ### Create the backup folder if it doesn't exist
            backup_folder_path.mkdir(parents=True, exist_ok=True)
            
            ### Copy all JSON files from the jsonfolder_path to the backup_folder_path
            all_files = [f for f in jsonfolder_path.iterdir() if f.is_file()]
            for file in all_files:
                shutil.copy(file, backup_folder_path)
            
            messagebox.showinfo("Success", f"Backup Done. \n{backup_folder_path}", parent=self.root)
            
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"Backup Failed. \n{error_message}", parent=self.root)

    def Button_Exit(self):
        def Exit_GUI():
            if self.close_callback:
                self.close_callback()
            self.root.destroy()

        Exit_GUI()

    def Button_SelectBackupFolder(self):
        try:
            ### Select File Frame.
            folder_path = filedialog.askdirectory(title="Select Backup Folder", parent=self.root)
            if folder_path != "":
                folder_path = folder_path + "/"
                self.FillEntry_Data(self.Main_Widget["Entry"]["BackupFolderPath"], folder_path, "readonly")
                JsonDataFunction.Update_jsonFileData(
                    file_path=self.SetBackup_JsonPath,
                    key_value="BackupPath",
                    value=folder_path
                )
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)

    #===================================================================================================
    def FillEntry_Data(self, object_entry:object=None, data:str=None, state:str="readonly"):
        object_entry["state"] = "normal"
        object_entry.delete(0,tk.END)
        object_entry.insert(0, data)

        if state == "readonly":
            object_entry["state"] = "readonly"

if __name__ == "__main__":
    VERSION = "2.0.0"
    root = tk.Tk()
    app = JsonPathExporter(root, version=VERSION)
    root.mainloop()
