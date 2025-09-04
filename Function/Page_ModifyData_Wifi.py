import tkinter as tk
from tkinter import ttk, messagebox
from idlelib.tooltip import Hovertip  

import traceback

import Function.MyFunction_JsonData as JsonDataFunction

from Class.Class_Button import Button

class Page_ModifyData_Wifi():
    def __init__(self, root=None, label_title:str=None, default_value:list=None, comfirm_callback=None):
        self.load_json_data()

        self.LabelTitle = label_title
        self.DefaultValue = default_value 
        self.comfirm_callback = comfirm_callback

        ### Initialize the main window.
        width = 600
        height = len(self.TreeView_Columns)*37 + 80
        self.root = root
        self.root.title("Wifi Setting")
        self.root.minsize(width, height)
        self.root.resizable(True, False)

        ### Initialize settings.
        self.Setting = {
            "Font": {
                "Title": ("Arial", 13, "bold"),
                "Label": ("Arial", 10),
                "Log": ("Arial", 10)
            }
        }

        self.Create_widgets()
        self.Set_DefaultValue()

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)
        wifi_json_data = JsonDataFunction.Get_jsonAllData(self.Environment_JsonData["JsonFilePath"] + "./json_Wifi.json")
        self.TreeView_Columns = JsonDataFunction.Get_DictKey(wifi_json_data["Wifi"][0])
    
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

        self.Image_path = {
            "Button_Comfirm": "./Img/check.png",
            "Button_Cancel": "./Img/cancel.png",
        }

        ### Create Elements.
        self.Main_Widget["Label"]["Title"] = tk.Label(self.Frame["Main"], text=self.LabelTitle, font=self.Setting["Font"]["Title"], foreground="blue")
        self.Main_Widget["Separator"]["Top"] = ttk.Separator(self.Frame["Main"], orient='horizontal')

        for column_name in self.TreeView_Columns:
            self.Main_Widget["Label"][column_name] = tk.Label(self.Frame["Main"], text=column_name + ":", font=self.Setting["Font"]["Label"])

        self.Main_Widget["Entry"]["WifiID"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["PingType"] = ttk.Combobox(self.Frame["Main"], values=["ipv4", "ipv6"], state="readonly", font=self.Setting["Font"]["Label"])
        self.Main_Widget["Entry"]["DUTIP"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Entry"]["SSID"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["Security"] = ttk.Combobox(self.Frame["Main"], values=["wpa", "wpa2", "wpa3"], state="readonly", font=self.Setting["Font"]["Label"])
        self.Main_Widget["Entry"]["Password"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Entry"]["BSSID"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["Driver_Band"] = ttk.Combobox(self.Frame["Main"], values=["2G", "5G", "Default"], state="readonly", font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["Driver_Standard"] = ttk.Combobox(self.Frame["Main"], values=["Auto", "11a", "11b", "11g", "11n", "11ac", "11ax"], state="readonly", font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["Driver_Channel"] = ttk.Combobox(self.Frame["Main"], values=["Auto", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"], state="readonly", font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["Driver_Bandwidth"] = ttk.Combobox(self.Frame["Main"], values=["Auto", "20", "40", "80"], state="readonly", font=self.Setting["Font"]["Label"])
        self.Main_Widget["Combobox"]["Driver_Band"].bind("<<ComboboxSelected>>", self.Click_ComboBox_DriverBand)
        self.Main_Widget["Combobox"]["Driver_Standard"].bind("<<ComboboxSelected>>", self.Click_ComboBox_DriverStandard)

        self.Main_Widget["Separator"]["Low"] = ttk.Separator(self.Frame["Main"], orient='horizontal')
        self.Main_Widget["Button"]["Comfirm"] = Button(self.Frame["Main"], image_path=self.Image_path["Button_Comfirm"], size=(40,40), command=self.Button_Comfirm)
        self.Main_Widget["Button"]["Cancel"] = Button(self.Frame["Main"], image_path=self.Image_path["Button_Cancel"], size=(40,40), command=self.Button_Cancel)

        ### Layout Elements.
        self.Main_Widget["Label"]["Title"].grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.Main_Widget["Separator"]["Top"].grid(row=1, column=0, columnspan=2, padx=5, pady=(0,10), sticky="ew")

        for num, column_name in enumerate(self.TreeView_Columns, start=2):
            self.Main_Widget["Label"][column_name].grid(row=num, column=0, padx=10, pady=5, sticky="w")

        self.Main_Widget["Entry"]["WifiID"].grid(row=2, column=1, padx=(0,10), pady=5, sticky="ew")    
        self.Main_Widget["Combobox"]["PingType"].grid(row=3, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["DUTIP"].grid(row=4, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["SSID"].grid(row=5, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Combobox"]["Security"].grid(row=6, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["Password"].grid(row=7, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["BSSID"].grid(row=8, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Combobox"]["Driver_Band"].grid(row=9, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Combobox"]["Driver_Standard"].grid(row=10, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Combobox"]["Driver_Channel"].grid(row=11, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Combobox"]["Driver_Bandwidth"].grid(row=12, column=1, padx=(0,10), pady=5, sticky="ew")

        self.Main_Widget["Separator"]["Low"].grid(row=len(self.TreeView_Columns)+2, column=0, columnspan=2, padx=5, pady=(10,0), sticky="ew")
        self.Main_Widget["Button"]["Comfirm"].grid(row=len(self.TreeView_Columns)+3, column=1, columnspan=2, padx=(0,60), pady=(5,5), sticky="e")
        self.Main_Widget["Button"]["Cancel"].grid(row=len(self.TreeView_Columns)+3, column=1, padx=(0,5), pady=(5,5), sticky="e")

        self.Frame["Main"].grid_columnconfigure(1, weight=1)

        Tooltip = {
            "Button_Comfirm": Hovertip(self.Main_Widget["Button"]["Comfirm"], text='Confirm the settings.', hover_delay=300),
            "Button_Cancel": Hovertip(self.Main_Widget["Button"]["Cancel"], text='Close and Cancel the settings.', hover_delay=300),
        }

    def Set_DefaultValue(self):
        try:
            if self.DefaultValue is None:
                self.Main_Widget["Entry"]["WifiID"].insert(0, "WifiID_001")
                self.Main_Widget["Combobox"]["PingType"].set("ipv4")
                self.Main_Widget["Entry"]["DUTIP"].insert(0, "192.168.1.1")
                self.Main_Widget["Entry"]["SSID"].insert(0, "Test_SSID")
                self.Main_Widget["Combobox"]["Security"].set("wpa2")
                self.Main_Widget["Entry"]["Password"].insert(0, "Test_Password")
                self.Main_Widget["Entry"]["BSSID"].insert(0, "00:11:22:33:44:55")
                self.Main_Widget["Combobox"]["Driver_Band"].set("Default")
                self.Main_Widget["Combobox"]["Driver_Standard"].set("Auto")
                self.Main_Widget["Combobox"]["Driver_Channel"].set("Auto")
                self.Main_Widget["Combobox"]["Driver_Bandwidth"].set("Auto")
            else:
                self.Main_Widget["Entry"]["WifiID"].insert(0, self.DefaultValue[0])
                self.Main_Widget["Combobox"]["PingType"].set(self.DefaultValue[1])
                self.Main_Widget["Entry"]["DUTIP"].insert(0, self.DefaultValue[2])
                self.Main_Widget["Entry"]["SSID"].insert(0, self.DefaultValue[3])
                self.Main_Widget["Combobox"]["Security"].set(self.DefaultValue[4])
                self.Main_Widget["Entry"]["Password"].insert(0, self.DefaultValue[5])
                self.Main_Widget["Entry"]["BSSID"].insert(0, self.DefaultValue[6])
                self.Main_Widget["Combobox"]["Driver_Band"].set(self.DefaultValue[7])
                self.Main_Widget["Combobox"]["Driver_Standard"].set(self.DefaultValue[8])
                self.Main_Widget["Combobox"]["Driver_Channel"].set(self.DefaultValue[9])
                self.Main_Widget["Combobox"]["Driver_Bandwidth"].set(self.DefaultValue[10])

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)

    #===================================================================================================
    def Button_Comfirm(self):   
        try:
            ### Get the values from the entries and comboboxes.
            new_wifi_value = [
                str(self.Main_Widget["Entry"]["WifiID"].get()),
                str(self.Main_Widget["Combobox"]["PingType"].get()),
                str(self.Main_Widget["Entry"]["DUTIP"].get()),
                str(self.Main_Widget["Entry"]["SSID"].get()),
                str(self.Main_Widget["Combobox"]["Security"].get()),
                str(self.Main_Widget["Entry"]["Password"].get()),
                str(self.Main_Widget["Entry"]["BSSID"].get()),
                str(self.Main_Widget["Combobox"]["Driver_Band"].get()),
                str(self.Main_Widget["Combobox"]["Driver_Standard"].get()),
                str(self.Main_Widget["Combobox"]["Driver_Channel"].get()),
                str(self.Main_Widget["Combobox"]["Driver_Bandwidth"].get())
            ]

            ### Check new data.
            new_wifi_id:str = new_wifi_value[0]
            new_wifi_bssid:str = new_wifi_value[6]
            wifi_json_data = JsonDataFunction.Get_jsonAllData(self.Environment_JsonData["JsonFilePath"] + "./json_Wifi.json")
            all_wifi_data:list = wifi_json_data["Wifi"]
            
            ### If editing an existing item, remove it from the list first.
            if "Edit" in self.LabelTitle:
                selected_data = {}
                for i, key in enumerate(self.TreeView_Columns, start=0):
                    selected_data[key] = str(self.DefaultValue[i])
                all_wifi_data.remove(selected_data)

            ### Check if the WifiID or BSSID already exists.
            for wifi_data in all_wifi_data:
                if new_wifi_id == wifi_data["WifiID"]:
                    messagebox.showerror("Error", f"[WifiID] \"{new_wifi_id}\" already exists.", parent=self.root)
                    return False

            ### Check if any fields are empty.
            ### If the WifiID and BSSID are unique, proceed to add or update the data.
            if "" in new_wifi_value:
                messagebox.showerror("Error", "All of the fields cannot be empty.", parent=self.root)
                return False
            if self.comfirm_callback:
                self.comfirm_callback(selected_item_value=self.DefaultValue, new_item_value=new_wifi_value)
                self.root.destroy()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)

    def Button_Cancel(self):
        self.root.destroy()

    def Click_ComboBox_DriverBand(self, event):
        DriverBand = self.Main_Widget["Combobox"]["Driver_Band"].get() if self.Main_Widget["Combobox"]["Driver_Band"].get() != "" else "None" 
        ### Set Default Values.
        if DriverBand == "2G" or DriverBand == "5G":
            self.Main_Widget["Combobox"]["Driver_Standard"].set("")
            self.Main_Widget["Combobox"]["Driver_Channel"].set("")
            self.Main_Widget["Combobox"]["Driver_Bandwidth"].set("")
            
        if DriverBand == "Default":
            self.Main_Widget["Combobox"]["Driver_Standard"].set("Default")
            self.Main_Widget["Combobox"]["Driver_Channel"].set("Default")
            self.Main_Widget["Combobox"]["Driver_Bandwidth"].set("Default")

        ### Set ComboBox options.
        if DriverBand == "2G":
            self.Main_Widget["Combobox"]["Driver_Standard"]["values"] = ["Auto", "11b", "11g", "11n", "11ax"]
            self.Main_Widget["Combobox"]["Driver_Channel"]["values"] = ["Auto", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
            self.Main_Widget["Combobox"]["Driver_Bandwidth"]["values"] = ["Auto", "20", "40", "80"]
        elif DriverBand == "5G":
            self.Main_Widget["Combobox"]["Driver_Standard"]["values"] = ["Auto", "11a", "11n", "11ac", "11ax"]
            self.Main_Widget["Combobox"]["Driver_Channel"]["values"] = ["Auto", "36", "40", "44", "48", "52", "56", "60", "64", "100", "104", "108", "112", "116", "120", "124", "128", "132", "136", "140"]
            self.Main_Widget["Combobox"]["Driver_Bandwidth"]["values"] = ["Auto", "20", "40", "80"]
        else:
            self.Main_Widget["Combobox"]["Driver_Standard"]["values"] = ["Default"]
            self.Main_Widget["Combobox"]["Driver_Channel"]["values"] = ["Default"]
            self.Main_Widget["Combobox"]["Driver_Bandwidth"]["values"] = ["Default"]

    def Click_ComboBox_DriverStandard(self, event):
        DriverBand = self.Main_Widget["Combobox"]["Driver_Band"].get() if self.Main_Widget["Combobox"]["Driver_Band"].get() != "" else "None" 
        DriverStandard = self.Main_Widget["Combobox"]["Driver_Standard"].get() if self.Main_Widget["Combobox"]["Driver_Standard"].get() != "" else "None"

        ### Set Default Values.
        self.Main_Widget["Combobox"]["Driver_Channel"].set("")
        self.Main_Widget["Combobox"]["Driver_Bandwidth"].set("")

        ### Set ComboBox options.
        if DriverBand == "2G":
            if DriverStandard in ["11b", "11g"]:
                self.Main_Widget["Combobox"]["Driver_Bandwidth"]["values"] = ["Auto", "20"]

            elif DriverStandard in ["11n", "11ax"]:
                self.Main_Widget["Combobox"]["Driver_Bandwidth"]["values"] = ["Auto", "20", "40"]

            elif DriverStandard in ["Auto"]:
                self.Main_Widget["Combobox"]["Driver_Channel"]["values"] = ["Default"]
                self.Main_Widget["Combobox"]["Driver_Bandwidth"]["values"] = ["Default"]

        elif DriverBand == "5G":
            if DriverBand in ["11a"]:
                self.Main_Widget["Combobox"]["Driver_Bandwidth"]["values"] = ["Auto", "20"]

            elif DriverStandard in ["11n"]:
                self.Main_Widget["Combobox"]["Driver_Bandwidth"]["values"] = ["Auto", "20", "40"]

            elif DriverStandard in ["11ac", "11ax"]:
                self.Main_Widget["Combobox"]["Driver_Bandwidth"]["values"] = ["Auto", "20", "40", "80"]

            elif DriverStandard in ["Auto"]:
                self.Main_Widget["Combobox"]["Driver_Channel"]["values"] = ["Default"]
                self.Main_Widget["Combobox"]["Driver_Bandwidth"]["values"] = ["Default"]

if __name__ == "__main__":
    root = tk.Tk()
    app = Page_ModifyData_Wifi(root=root, label_title="Wifi Add Item")
    root.mainloop()

