import tkinter as tk
from tkinter import ttk, messagebox
from idlelib.tooltip import Hovertip  

import traceback

import Function.MyFunction_JsonData as JsonDataFunction

from Class.Class_Button import Button

class Page_ModifyData_Client():
    def __init__(self, root=None, label_title:str=None, default_value:list=None, comfirm_callback=None):

        self.load_json_data()

        self.LabelTitle = label_title
        self.DefaultValue = default_value 
        self.comfirm_callback = comfirm_callback

        ### Initialize the main window.
        width = 600
        height = len(self.TreeView_Columns)*37 + 80
        self.root = root
        self.root.title("Client Setting")
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
        client_json_data = JsonDataFunction.Get_jsonAllData(self.Environment_JsonData["JsonFilePath"] + "./json_Client.json")
        self.TreeView_Columns = JsonDataFunction.Get_DictKey(client_json_data["Client"][0])
    
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

        self.Main_Widget["Entry"]["ClinetID"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Entry"]["MAC"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Entry"]["EtherIP"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])
        self.Main_Widget["Entry"]["Comment"] = tk.Entry(self.Frame["Main"], font=self.Setting["Font"]["Label"])

        self.Main_Widget["Separator"]["Low"] = ttk.Separator(self.Frame["Main"], orient='horizontal')
        self.Main_Widget["Button"]["Comfirm"] = Button(self.Frame["Main"], image_path=self.Image_path["Button_Comfirm"], size=(40,40), command=self.Button_Comfirm)
        self.Main_Widget["Button"]["Cancel"] = Button(self.Frame["Main"], image_path=self.Image_path["Button_Cancel"], size=(40,40), command=self.Button_Cancel)

        ### Layout Elements.
        self.Main_Widget["Label"]["Title"].grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.Main_Widget["Separator"]["Top"].grid(row=1, column=0, columnspan=2, padx=5, pady=(0,10), sticky="ew")

        for num, column_name in enumerate(self.TreeView_Columns, start=2):
            self.Main_Widget["Label"][column_name].grid(row=num, column=0, padx=10, pady=5, sticky="w")

        self.Main_Widget["Entry"]["ClinetID"].grid(row=2, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["MAC"].grid(row=3, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["EtherIP"].grid(row=4, column=1, padx=(0,10), pady=5, sticky="ew")
        self.Main_Widget["Entry"]["Comment"].grid(row=5, column=1, padx=(0,10), pady=5, sticky="ew")

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
                self.Main_Widget["Entry"]["ClinetID"].insert(0, "ClinetID_001")
                self.Main_Widget["Entry"]["MAC"].insert(0, "FF:FF:FF:FF:FF:FF")
                self.Main_Widget["Entry"]["EtherIP"].insert(0, "0.0.0.0")
                self.Main_Widget["Entry"]["Comment"].insert(0, "Comment_001")

            else:
                self.Main_Widget["Entry"]["ClinetID"].insert(0, self.DefaultValue[0])
                self.Main_Widget["Entry"]["MAC"].insert(0, self.DefaultValue[1])
                self.Main_Widget["Entry"]["EtherIP"].insert(0, self.DefaultValue[2])
                self.Main_Widget["Entry"]["Comment"].insert(0, self.DefaultValue[3])
                
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)

    #===================================================================================================
    def Button_Comfirm(self):
        try:
            ### Get the values from the entries and comboboxes.
            new_client_value = [
                str(self.Main_Widget["Entry"]["ClinetID"].get()),
                str(self.Main_Widget["Entry"]["MAC"].get()),
                str(self.Main_Widget["Entry"]["EtherIP"].get()),
                str(self.Main_Widget["Entry"]["Comment"].get()),
            ]

            ### Check new data.
            new_client_id:str = new_client_value[0]
            new_mac = new_client_value[1]
            new_ether_ip = new_client_value[2]
            client_json_data = JsonDataFunction.Get_jsonAllData(self.Environment_JsonData["JsonFilePath"] + "./json_Client.json")
            all_client_data:list = client_json_data["Client"]

            ### If editing an existing item, remove it from the list first.
            if "Edit" in self.LabelTitle:
                selected_data = {}
                for i, key in enumerate(self.TreeView_Columns, start=0):
                    selected_data[key] = str(self.DefaultValue[i])
                all_client_data.remove(selected_data)

            ### Check if the ClientID or MAC already exists.
            for client_data in all_client_data:
                if new_client_id == client_data["ClientID"]:
                    messagebox.showerror("Error", f"[ClientID] \"{new_client_id}\" already exists.", parent=self.root)
                    return False
                if new_mac == client_data["MAC"]:
                    messagebox.showerror("Error", f"[MAC] \"{new_mac}\" already exists.", parent=self.root)
                    return False
                if new_ether_ip == client_data["EtherIP"]:
                    messagebox.showerror("Error", f"[EtherIP] \"{new_ether_ip}\" already exists.", parent=self.root)
                    return False

            ### Check if any of the fields are empty.
            ### If the ClientID and BSSID are unique, proceed to add or update the data.
            if new_client_id == "" or new_mac == "" or new_ether_ip == "":
                messagebox.showerror("Error", "[ClientID], [MAC], and [EtherIP] cannot be empty.", parent=self.root)
                return False
            new_client_value[3] = new_client_value[3] if new_client_value[3] != "" else "None" 
            if self.comfirm_callback:
                self.comfirm_callback(selected_item_value=self.DefaultValue, new_item_value=new_client_value)
                self.root.destroy()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)
            return

    def Button_Cancel(self):
        self.root.destroy()

if __name__ == "__main__":
    default_value = ["Jerry1123", "FF:FF:FF:FF:FF:FF", "0.0.0.0", "Comment_001"]
    root = tk.Tk()
    app = Page_ModifyData_Client(root=root, label_title="Client Add Item")
    root.mainloop()