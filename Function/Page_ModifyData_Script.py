import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip  

import os
import traceback

import Function.MyFunction_JsonData as JsonDataFunction

class Page_ModifyData_Script:
    def __init__(self, root=None, label_title:str=None, default_value:list=None, comfirm_callback=None):
        self.load_json_data()

        self.LabelTitle = label_title
        self.DefaultValue = default_value if default_value is not None else ["TestScriptID_001", "Ping", "Test1", "ipv4", "8.8.8.8", "1200", "60", "10"]
        self.comfirm_callback = comfirm_callback

        ### Initialize the main window.
        width = 750
        height = len(self.TreeView_Columns)*37 + 80
        self.root = root
        self.root.title("Script Setting")
        self.root.minsize(width, height)
        self.root.resizable(True,False)

        ### Initialize settings.
        self.Setting = {
            "Font": {
                "Title": ("Arial", 13, "bold"),
                "Label": ("Arial", 10),
                "Log": ("Arial", 10)
            },
            "Button": {
                "Normal": {
                    "relief": "flat",
                    "overrelief": "raised",
                    "cursor": "hand2",
                    # "activebackground": "lightblue"    # 點擊時背景色
                },
                "Disabled": {
                    # "relief": "flat",
                    "background": "SystemButtonFace",  # 系統按鈕面板色
                    "cursor": "arrow"                  # 禁用時改變游標
                },
            },
            "Entry": {
                "Normal": {
                    "relief": "sunken",
                    "borderwidth": 1,
                    "background": "white",
                    "foreground": "black"
                },
                "Disabled": {
                    "relief": "groove",
                    "borderwidth": 1,
                    "disabledbackground": "SystemButtonFace",
                    "highlightthickness": 1,
                    "highlightbackground": "lightgray",
                    "foreground": "lightgray"
                }
            }
        }

        self.Create_widgets()
        self.Set_Label_Title(script_type=self.DefaultValue[1])
        self.Set_Widget_Status(script_type=self.DefaultValue[1])
        self.Set_ParameterValue(list_value=self.DefaultValue)

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)
        script_json_data = JsonDataFunction.Get_jsonAllData(self.Environment_JsonData["JsonFilePath"] + "./json_Script.json")
        self.TreeView_Columns = JsonDataFunction.Get_DictKey(script_json_data["Script"][0])

    def Create_widgets(self):
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
        self.Main_Widget["Combobox"] = {}
        self.Main_Widget["Separator"] = {}

        self.Image = {}
        self.Image["Button_SelectFolder"] = ImageTk.PhotoImage(Image.open("./Img/add_folder.png").resize((20, 20)))
        self.Image["Button_Comfirm"] = ImageTk.PhotoImage(Image.open("./Img/check.png").resize((40, 40)))
        self.Image["Button_Cancel"] = ImageTk.PhotoImage(Image.open("./Img/cancel.png").resize((40,40)))

        ### Create Elements.
        self.Main_Widget["Label"]["Title"] = tk.Label(self.Frame["Main"], text=self.LabelTitle, font=self.Setting["Font"]["Title"], foreground="blue")
        self.Main_Widget["Separator"]["Top"] = ttk.Separator(self.Frame["Main"], orient='horizontal')

        for column_name in self.TreeView_Columns:
            self.Main_Widget["Label"][column_name] = tk.Label(self.Frame["Main"], text=column_name + ":", font=self.Setting["Font"]["Label"])

        self.Main_Widget["Entry"]["TestScriptID"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["Script"] = ttk.Combobox(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["Script"].bind('<<ComboboxSelected>>', self.Combobox_SelectScriptType)
        self.Main_Widget["Entry"]["Parameter1"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["Parameter2"] = ttk.Combobox(self.Frame["Main"], values=["ipv4", "ipv6"])
        self.Main_Widget["Entry"]["Parameter3"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Entry"]["Parameter4"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["Parameter5"] = ttk.Combobox(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Entry"]["Parameter6"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])

        self.Main_Widget["Separator"]["Low"] = ttk.Separator(self.Frame["Main"], orient='horizontal')
        self.Main_Widget["Button"]["Select_YoutubeFile"] = tk.Button(self.Frame["Main"], image=self.Image["Button_SelectFolder"], command=self.Button_SelectYoutubeFile)
        self.Main_Widget["Button"]["Comfirm"] = tk.Button(self.Frame["Main"], image=self.Image["Button_Comfirm"], **self.Setting["Button"]["Normal"], command=self.Button_Comfirm)
        self.Main_Widget["Button"]["Cancel"] = tk.Button(self.Frame["Main"], image=self.Image["Button_Cancel"], **self.Setting["Button"]["Normal"], command=self.Button_Cancel)

        ### Layout Elements.
        self.Main_Widget["Label"]["Title"].grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.Main_Widget["Separator"]["Top"].grid(row=1, column=0, columnspan=2, padx=5, pady=(0,10), sticky="ew")

        for num, column_name in enumerate(self.TreeView_Columns, start=2):
            self.Main_Widget["Label"][column_name].grid(row=num, column=0, padx=10, pady=5, sticky="w")

        self.Main_Widget["Entry"]["TestScriptID"].grid(row=2, column=1, padx=(0,10), pady=5, sticky="ew")    
        self.Main_Widget["Combobox"]["Script"].grid(row=3, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["Parameter1"].grid(row=4, column=1, padx=(0,40), pady=5, sticky="ew")
        self.Main_Widget["Button"]["Select_YoutubeFile"].grid(row=4, column=1, padx=(0,10), pady=5, sticky="e")
        self.Main_Widget["Combobox"]["Parameter2"].grid(row=5, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["Parameter3"].grid(row=6, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["Parameter4"].grid(row=7, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Combobox"]["Parameter5"].grid(row=8, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["Parameter6"].grid(row=9, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Separator"]["Low"].grid(row=len(self.TreeView_Columns)+2, column=0, columnspan=2, padx=5, pady=(10,0), sticky="ew")
        self.Main_Widget["Button"]["Comfirm"].grid(row=len(self.TreeView_Columns)+3, column=1, columnspan=2, padx=(0,60), pady=(5,5), sticky="e")
        self.Main_Widget["Button"]["Cancel"].grid(row=len(self.TreeView_Columns)+3, column=1, padx=(0,5), pady=(5,5), sticky="e")

        self.Frame["Main"].grid_columnconfigure(1, weight=1)

        Tooltip = {
            "Button_SelectYoutubeFile": Hovertip(self.Main_Widget["Button"]["Select_YoutubeFile"], text='Choose youtubeIRL.txt file path.', hover_delay=300),
            "Button_Comfirm": Hovertip(self.Main_Widget["Button"]["Comfirm"], text='Confirm the settings.', hover_delay=300),
            "Button_Cancel": Hovertip(self.Main_Widget["Button"]["Cancel"], text='Close and Cancel the settings.', hover_delay=300),
        }

    def Set_Label_Title(self, script_type:str=None):
        if script_type == "Ping":
            self.Main_Widget["Label"]["Parameter1"].config(text="P1 (PingName):")
            self.Main_Widget["Label"]["Parameter2"].config(text="P2 (ipv4/ipv6):")
            self.Main_Widget["Label"]["Parameter3"].config(text="P3 (Destination):")
            self.Main_Widget["Label"]["Parameter4"].config(text="P4 (RTT Error Threshold):")
            self.Main_Widget["Label"]["Parameter5"].config(text="P5 (RTT Error Time)(s):")
            self.Main_Widget["Label"]["Parameter6"].config(text="P6 (PingLost Consecutive Number):")
        elif script_type == "Youtube":
            self.Main_Widget["Label"]["Parameter1"].config(text="P1 (Video Url List):")
            self.Main_Widget["Label"]["Parameter2"].config(text="P2 (Time Per Video):")
            self.Main_Widget["Label"]["Parameter3"].config(text="P3 (RXPackets Error Threshold)(3s):")
            self.Main_Widget["Label"]["Parameter4"].config(text="P4 (Error Consecutive Number):")
            self.Main_Widget["Label"]["Parameter5"].config(text="P5 (None):")
            self.Main_Widget["Label"]["Parameter6"].config(text="P6 (None):")

    def Set_Widget_Status(self, script_type:str=None):
        try:
            if script_type == "Ping":
                self.Main_Widget["Entry"]["TestScriptID"].config(state="normal", **self.Setting["Entry"]["Normal"])
                self.Main_Widget["Combobox"]["Script"].config(state="readonly", values=["Ping", "Youtube"])
                self.Main_Widget["Entry"]["Parameter1"].config(state="normal", **self.Setting["Entry"]["Normal"])
                self.Main_Widget["Combobox"]["Parameter2"].config(state="readonly", values=["ipv4", "ipv6"])
                self.Main_Widget["Entry"]["Parameter3"].config(state="normal", **self.Setting["Entry"]["Normal"])
                self.Main_Widget["Entry"]["Parameter4"].config(state="normal", **self.Setting["Entry"]["Normal"])
                self.Main_Widget["Combobox"]["Parameter5"].config(state="readonly", values=["30", "60", "90", "120"])
                self.Main_Widget["Entry"]["Parameter6"].config(state="normal", **self.Setting["Entry"]["Normal"])
                self.Main_Widget["Button"]["Select_YoutubeFile"].config(state="disabled", **self.Setting["Button"]["Disabled"])

                self.Main_Widget["Label"]["Parameter5"].config(foreground="black")
                self.Main_Widget["Label"]["Parameter6"].config(foreground="black")

            elif script_type == "Youtube":
                self.Main_Widget["Entry"]["TestScriptID"].config(state="normal", **self.Setting["Entry"]["Normal"])
                self.Main_Widget["Combobox"]["Script"].config(state="readonly", values=["Ping", "Youtube"])
                self.Main_Widget["Entry"]["Parameter1"].config(state="readonly", readonlybackground="light yellow")
                self.Main_Widget["Combobox"]["Parameter2"].config(state="normal", values=[""])
                self.Main_Widget["Entry"]["Parameter3"].config(state="normal", **self.Setting["Entry"]["Normal"])
                self.Main_Widget["Entry"]["Parameter4"].config(state="normal", **self.Setting["Entry"]["Normal"])
                self.Main_Widget["Combobox"]["Parameter5"].config(state="disabled")
                self.Main_Widget["Entry"]["Parameter6"].config(state="disabled", **self.Setting["Entry"]["Disabled"])
                self.Main_Widget["Button"]["Select_YoutubeFile"].config(state="normal", **self.Setting["Button"]["Normal"])

                self.Main_Widget["Label"]["Parameter5"].config(foreground="#979595")
                self.Main_Widget["Label"]["Parameter6"].config(foreground="#979595")

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)
    
    def Set_ParameterValue(self, list_value=None):
        try:
            ### normal the Entry before set value.
            self.Main_Widget["Entry"]["Parameter1"].config(state="normal")
            self.Main_Widget["Entry"]["Parameter6"].config(state="normal")

            ### Clear all Entry.
            self.Main_Widget["Entry"]["TestScriptID"].delete(0, tk.END)
            self.Main_Widget["Entry"]["Parameter1"].delete(0, tk.END)
            self.Main_Widget["Entry"]["Parameter3"].delete(0, tk.END)
            self.Main_Widget["Entry"]["Parameter4"].delete(0, tk.END)
            self.Main_Widget["Entry"]["Parameter6"].delete(0, tk.END)

            # elif list_value[1] == "Ping":
            if list_value[1] == "Ping":
                self.Main_Widget["Entry"]["TestScriptID"].insert(0, list_value[0])
                self.Main_Widget["Combobox"]["Script"].set(list_value[1])
                self.Main_Widget["Entry"]["Parameter1"].insert(0, list_value[2])
                self.Main_Widget["Combobox"]["Parameter2"].set(list_value[3])
                self.Main_Widget["Entry"]["Parameter3"].insert(0, list_value[4])
                self.Main_Widget["Entry"]["Parameter4"].insert(0, list_value[5])
                self.Main_Widget["Combobox"]["Parameter5"].set(list_value[6])
                self.Main_Widget["Entry"]["Parameter6"].insert(0, list_value[7])

            elif list_value[1] == "Youtube":                
                ### set the default value.
                self.Main_Widget["Entry"]["TestScriptID"].insert(0, list_value[0])
                self.Main_Widget["Combobox"]["Script"].set(list_value[1])
                self.Main_Widget["Entry"]["Parameter1"].insert(0, list_value[2])
                self.Main_Widget["Combobox"]["Parameter2"].set(list_value[3])
                self.Main_Widget["Entry"]["Parameter3"].insert(0, list_value[4])
                self.Main_Widget["Entry"]["Parameter4"].insert(0, list_value[5])
                self.Main_Widget["Combobox"]["Parameter5"].set(list_value[6])
                self.Main_Widget["Entry"]["Parameter6"].insert(0, list_value[7])

                ### disable the Entry after set value.
                self.Main_Widget["Entry"]["Parameter1"].config(state="readonly")
                self.Main_Widget["Entry"]["Parameter6"].config(state="disable")

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)
    
    #===================================================================================================
    def Combobox_SelectScriptType(self, event=None):
        testscript_id = self.Main_Widget["Entry"]["TestScriptID"].get()
        script_type = self.Main_Widget["Combobox"]["Script"].get()
        current_working_dir = os.getcwd().replace("\\", "/") + "/"

        if script_type == "Ping":
            input_value  = [testscript_id, script_type, "Test1", "ipv4", "8.8.8.8", "1200", "60", "10"]
        elif script_type == "Youtube":
            input_value  = [testscript_id, script_type, current_working_dir + "JsonFile/youtubeURL.json", "1", "100", "5", "None", "None"]

        self.Set_Label_Title(script_type=script_type)
        self.Set_Widget_Status(script_type=script_type)
        self.Set_ParameterValue(list_value=input_value)

    def Button_SelectYoutubeFile(self):
        try:
            ### Select File Frame.
            ### Check Youtubue JSON file.
            ### File Youtube JSON file path.
            file_path = filedialog.askopenfilename(title="Select Youtube JSON File", parent=self.root)
            if file_path == "":
                return

            if file_path[-4:] != ".txt":  
                messagebox.showinfo("Error","The file must be xxx.txt file.", parent=self.root)
                self.Button_SelectYoutubeFile()

            if file_path[-4:] == ".txt":  
                file_path = file_path.replace("\\", "/")
                self.Main_Widget["Entry"]["Parameter1"].config(state="normal")
                self.Main_Widget["Entry"]["Parameter1"].delete(0, tk.END)
                self.Main_Widget["Entry"]["Parameter1"].insert(0, file_path)
                self.Main_Widget["Entry"]["Parameter1"].config(state="readonly")
            
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)

    def Button_Comfirm(self):
        try:
            ### Get the values from the Entry and Combobox.
            new_script_value = [
                self.Main_Widget["Entry"]["TestScriptID"].get(),
                self.Main_Widget["Combobox"]["Script"].get(),
                self.Main_Widget["Entry"]["Parameter1"].get(),
                self.Main_Widget["Combobox"]["Parameter2"].get(),
                self.Main_Widget["Entry"]["Parameter3"].get(),
                self.Main_Widget["Entry"]["Parameter4"].get(),
                self.Main_Widget["Combobox"]["Parameter5"].get(),
                self.Main_Widget["Entry"]["Parameter6"].get()
            ]
            
            ### Check new data.
            ### Check testscript_id should be unipue.
            new_testscript_id = new_script_value[0]
            script_json_data:dict = JsonDataFunction.Get_jsonAllData(self.Environment_JsonData["JsonFilePath"] + "./json_Script.json")
            all_script_data:list = script_json_data["Script"]

            ### If editing an existing item, remove it from the check list.
            if "Edit" in self.LabelTitle:
                selected_data = {}
                for i, key in enumerate(self.TreeView_Columns, start=0): 
                    selected_data[key] = str(self.DefaultValue[i])
                all_script_data.remove(selected_data)

            ### Check if the TestScriptID already exists in the list.
            for script_data in all_script_data:
                if new_testscript_id == script_data["TestScriptID"]:
                    messagebox.showerror("Error", f"[TestScriptID] \"{new_testscript_id}\" already exists.", parent=self.root)
                    return False

            ### Check when script_type == "Ping", Parameter1 should be unique.
            new_script_type = new_script_value[1]
            if new_script_type == "Ping":
                new_pingscript_name = new_script_value[2]
                for script_data in all_script_data:
                    if new_pingscript_name == script_data["Parameter1"]:
                        messagebox.showerror("Error", f"PingName(Parameter1) \"{new_pingscript_name}\" already exists.", parent=self.root)
                        return False
            
            ### Check all the fields are not empty.
            ### If the WifiID and BSSID are unique, proceed to add or update the data.
            if ""in new_script_value:
                messagebox.showerror("Error", "All of the fields cannot be empty.", parent=self.root)
                return False
            if self.comfirm_callback:
                self.comfirm_callback(selected_item_value=self.DefaultValue, new_item_value=new_script_value)
                self.root.destroy()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)
            return

    def Button_Cancel(self):
        self.root.destroy()

if __name__ == "__main__":
    # default_value = ["Test", "Ping", "Test1", "ipv6", "7.2.168.0.1", "1200", "60", "10"]
    default_value = ["Test", "Youtube", "D:/Jerry/", "1", "100", "5", "None", "None"]
    root = tk.Tk()
    app = Page_ModifyData_Script(root=root, label_title="Script Add Item", default_value=default_value)
    root.mainloop()

