import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, messagebox
from idlelib.tooltip import Hovertip  
import traceback

import Function.MyFunction_JsonData as JsonDataFunction

from Function.Page_SetWeeklyTime import Page_SetWeeklyTime
from Function.Frame_SituationCanvas import Frame_SituationCanvas

from Class.Class_Button import Button

class Page_SetSituationName():
    def __init__(self, root, title:str="Add Situation", confirm_callback=None):
        self.confirm_callback = confirm_callback    

        self.root = root
        height = 150
        width = 350
        self.root.title(f"{title}")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        self.root.resizable(True, True)

        self.load_json_data()
        self.Create_Widgets()

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)

        self.Schedule_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Schedule.json"
        self.Schedule_JsonData = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)

    def Create_Widgets(self):
        self.label_name = ttk.Label(self.root, text="Situation Name :")
        self.entry_name = ttk.Entry(self.root)
        self.button_confirm = Button(self.root, text="Confirm", command=self.Button_Confirm)
        self.button_cancel = Button(self.root, text="Cancel", command=self.root.destroy)

        self.label_name.grid(row=0, column=0, padx=10, pady=(20,0))
        self.entry_name.grid(row=1, column=0, padx=10,  pady=(10,0), sticky="we")
        self.button_confirm.grid(row=2, column=0, padx=(0,125), pady=10, sticky="e")
        self.button_cancel.grid(row=2, column=0, padx=(0,10), pady=10, sticky="e")

        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

    def Button_Confirm(self):
        try:
            situation_name = self.entry_name.get().strip()
            if situation_name == "":
                messagebox.showwarning("Warning", "Situation name cannot be empty.", parent=self.root)
                return
            if situation_name in JsonDataFunction.Get_DictKey(self.Schedule_JsonData):
                messagebox.showwarning("Warning", "Situation name already exists.", parent=self.root)
                return
            
            self.confirm_callback(situation_name)
            self.root.destroy()
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

class Page_AddScript():
    def __init__(self, root, situation:str=None, title:str="Add New Script", confirm_callback=None):
        self.Situation = situation
        self.confirm_callback = confirm_callback

        self.root = root
        height = 150
        width = 350
        self.root.title(f"Add Scripts")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        self.root.resizable(True, True)

        self.load_json_data()
        self.Create_Widgets()
        self.Load_DefaultData()

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)

        self.Schedule_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Schedule.json"
        self.Schedule_JsonData = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)

        self.Script_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Script.json"
        self.Script_JadonData = JsonDataFunction.Get_jsonAllData(self.Script_JsonPath)

    def Create_Widgets(self):
        self.label_name = ttk.Label(self.root, text="Script ID :")
        self.combobox_name = ttk.Combobox(self.root, state="readonly")
        self.button_confirm = Button(self.root, text="Confirm", command=self.Button_Confirm)
        self.button_cancel = Button(self.root, text="Cancel", command=self.root.destroy)

        self.label_name.grid(row=0, column=0, padx=10, pady=(20,0))
        self.combobox_name.grid(row=1, column=0, padx=10,  pady=(10,0), sticky="we")
        self.button_confirm.grid(row=2, column=0, padx=(0,125), pady=10, sticky="e")
        self.button_cancel.grid(row=2, column=0, padx=(0,10), pady=10, sticky="e")

        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
    
    def Load_DefaultData(self):
        script_data:list = self.Script_JadonData["Script"]
        script_ids = [data["ScriptID"] for data in script_data]
        self.combobox_name['values'] = script_ids
        self.combobox_name.current(0) if script_ids else None

    def Button_Confirm(self):
        try:
            ### Get Existed Script ID in the Situation.
            existed_script_ids = []
            for script_data in self.Schedule_JsonData[self.Situation]["Script"]:
                existed_script_ids.append(script_data["ScriptID"])

            ### Get New Script ID.
            script_name = self.combobox_name.get().strip()
            if script_name == "":
                messagebox.showwarning("Warning", "Script ID cannot be empty.", parent=self.root)
                return
            if script_name in existed_script_ids:
                messagebox.showwarning("Warning", "Script ID already exists.", parent=self.root)
                return
            
            self.confirm_callback(script_name)
            self.root.destroy()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

class Page_AddClient():
    def __init__(self, root, situation:str=None, title:str=None, confirm_callback=None):
        self.Situation = situation
        self.confirm_callback = confirm_callback

        self.root = root
        height = 400
        width = 680
        self.root.title(f"{title}")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        self.root.resizable(True, True)

        ### Initialize settings.
        style = ttk.Style()
        style.configure("Title_AddClient.TLabel", font=("Segoe UI", 10, "bold"), foreground="black")
        style.configure("DataCount_AddClient.TLabel", font=("Segoe UI", 9), foreground="#717171")
        
        self.Image_path = {
            "Button_SelectAll": "./img/selectall.png",
        }

        self.load_json_data()
        self.Create_Widgets()
        self.Set_DefaultData()
        self.Update_Count()

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)

        self.Schedule_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Schedule.json"
        self.Schedule_JsonData = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)

        self.Client_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Client.json"
        self.Client_JadonData = JsonDataFunction.Get_jsonAllData(self.Client_JsonPath)

    def Create_Widgets(self):
        self.label_name = ttk.Label(self.root, text="Client ID :", style="Title_AddClient.TLabel")
        self.label_count = ttk.Label(self.root, text="Total: 0", style="DataCount_AddClient.TLabel")
        self.button_selectall = Button(self.root, image_path=self.Image_path["Button_SelectAll"], command=self.Button_SelectAll)
        self.canvas = tk.Canvas(self.root, relief="flat", highlightthickness=1, highlightbackground="#cccccc")
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.button_confirm = Button(self.root, text="Confirm", command=self.Button_Confirm)
        self.button_cancel = Button(self.root, text="Cancel", command=self.root.destroy)

        self.label_name.grid(row=0, column=0, padx=10, pady=(20,5), sticky="w")
        self.label_count.grid(row=0, column=0, padx=(0, 50), pady=(20,0), sticky="e")
        self.button_selectall.grid(row=0, column=0, padx=0, pady=(20,5), sticky="e")
        self.canvas.grid(row=1, column=0, padx=(10,0), pady=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, padx=(0,10), pady=0, sticky="ns")
        
        self.button_confirm.grid(row=3, column=0, padx=(0,125), pady=10, sticky="e")
        self.button_cancel.grid(row=3, column=0, padx=(0,10), pady=10, sticky="e")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        ### Create CheckButton.
        ### Store CheckButton with dictionary.
        ### self.check_buttons = {
        ###         "CheckButton": check_button,
        ###         "CheckVar": check_var,
        ###         "ClientID": client_id}
        self.frame = tk.Frame(self.canvas, relief="flat")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        all_client_ids = [data["ClientID"] for data in self.Client_JadonData["Client"]]
        all_client_ids.sort()
        self.check_buttons = []
        for i, client_id in enumerate(all_client_ids):
            check_var = tk.IntVar(value=False)
            check_button = ttk.Checkbutton(self.frame, text=client_id, variable=check_var, command=self.Update_Count)
            check_button.grid(row=int(i/5), column=i%5, padx=10, pady=5, sticky="w")
            self.check_buttons.append({"CheckButton": check_button,
                                       "CheckVar": check_var,
                                       "ClientID": client_id})

        ### After all widgets created, update scroll region and move to top.
        self.canvas.yview_moveto(0) 

    def Set_DefaultData(self):
        ### Get Existed Client ID in other Situation.
        exist_client_ids = []
        for situation in self.Schedule_JsonData:
            if situation != self.Situation:
                for client_id in self.Schedule_JsonData[situation]["ClientID"]:
                    exist_client_ids.append(client_id)

        ### Set CheckButton state as disabled if ClientID exists in other Situation.
        for check_button in self.check_buttons:
            if check_button["ClientID"] in exist_client_ids:
                check_button["CheckButton"].config(state="disabled")
            else:
                check_button["CheckButton"].config(state="normal")

        ### Set CheckButton state as selected if ClientID exists in current Situation.
        for check_button in self.check_buttons:
            if check_button["ClientID"] in self.Schedule_JsonData[self.Situation]["ClientID"]:
                check_button["CheckVar"].set(1)
            else:
                check_button["CheckVar"].set(0)
    
    def Button_SelectAll(self):
        try:
            enabled_buttons = [cb for cb in self.check_buttons if str(cb["CheckButton"]["state"]) != "disabled"]
            selected_count = sum(1 for check_button in enabled_buttons if check_button["CheckVar"].get())
            
            ### If all enabled buttons are selected, then unselect all; else select all.
            if selected_count == len(enabled_buttons):
                for check_button in enabled_buttons:
                    check_button["CheckVar"].set(0)
            else:
                for check_button in enabled_buttons:
                    check_button["CheckVar"].set(1)

            self.Update_Count()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)

    def Button_Confirm(self):
        try:
            selected_client_ids = [check_button["ClientID"] for check_button in self.check_buttons if check_button["CheckVar"].get() == 1]
            self.confirm_callback(selected_client_ids)
            self.root.destroy()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return
    
    def Update_Count(self):
        total_clients = sum(1 for check_button in self.check_buttons if check_button["CheckVar"].get() == 1)
        self.label_count.config(text=f"Total: {total_clients}")

###==============================================================================
class Frame_Schedule():
    def __init__(self, root, close_callback=None):
        self.close_callback = close_callback
        self.root = root

        ### Initialize settings.
        style = ttk.Style()
        style.configure("Title_Schedule.TLabel", font=("Segoe UI", 14, "bold"), foreground="blue")
        style.configure("FrameTitle_Schedule.TLabelframe.Label", font=("Segoe UI", 10, "bold"),  foreground="black")
        style.configure("Content_Schedule.TLabel", font=("Segoe UI", 9), foreground="black")
        style.configure("WifiSchedule_Schedule.TLabel", font=("Segoe UI", 8), foreground="#717171")
        style.configure("DataCount_Schedule.TLabel", font=("Segoe UI", 9), foreground="#717171")

        self.load_json_data()
        self.Create_Widgets()
        self.Load_ScheduleData()

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)

        self.Schedule_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Schedule.json"
        self.Client_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Client.json"
        self.Wifi_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Wifi.json"
        self.Script_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Script.json"

    def Create_Widgets(self):
        def create_widgets_situation():
            def update_situation_count():
                total_situations = self.Situation_Widget["Listbox"].size()
                self.Situation_Widget["Label"]["Count"].config(text=f"Total: {total_situations}")
                
            self.Situation_Widget = {}
            self.Situation_Widget["Button"] = {}
            self.Situation_Widget["Label"] = {}

            self.Situation_Widget["Button"]["Add"] = Button(self.Frame["Situation"], text="Add", width=10, command=self.Button_Situation_Add)
            self.Situation_Widget["Button"]["Delete"] = Button(self.Frame["Situation"], text="Delete", width=10, command=self.Button_Situation_Delete)
            self.Situation_Widget["Button"]["Copy"] = Button(self.Frame["Situation"], text="Copy", width=10, command=self.Button_Situation_Copy)
            self.Situation_Widget["Listbox"] = tk.Listbox(
                self.Frame["Situation"], 
                activestyle="dotbox", 
                font=("Segoe UI", 9),
                selectbackground="#bed9f3",  # 自訂選中時的背景色
                selectforeground="#2C67DE",     # 自訂選中時的文字色
                highlightthickness=0,        # 移除聚焦邊框
                takefocus=False,             # 不參與Tab鍵聚焦循環
                exportselection=False        # 關鍵：防止選取狀態被其他元件影響
            )
            
            self.Situation_Widget["Listbox"].bind('<<ListboxSelect>>', self.Show_SituationData)
            self.Situation_Widget["Scrollbar"] = ttk.Scrollbar(self.Frame["Situation"], orient=tk.VERTICAL, command=self.Situation_Widget["Listbox"].yview)
            self.Situation_Widget["Listbox"].configure(yscrollcommand=self.Situation_Widget["Scrollbar"].set)
            self.Situation_Widget["Label"]["Count"] = ttk.Label(self.Frame["Situation"], text="Total: 0", style="DataCount_Schedule.TLabel")

            self.Situation_Widget["Button"]["Add"].grid(row=0, column=0, padx=(5,0), pady=(5,0), sticky="w")
            self.Situation_Widget["Button"]["Delete"].grid(row=0, column=1, padx=(5,0), pady=(5,0), sticky="w")
            self.Situation_Widget["Button"]["Copy"].grid(row=0, column=2, padx=5, pady=(5,0), sticky="w")
            self.Situation_Widget["Listbox"].grid(row=1, column=0, columnspan=3, padx=(5,0), pady=5, sticky="nsew")
            self.Situation_Widget["Scrollbar"].grid(row=1, column=3, padx=(0,5), pady=5, sticky="ns")
            self.Situation_Widget["Label"]["Count"].grid(row=2, column=2, columnspan=2, padx=(0,5), pady=(0.5), sticky="e")
            
            self.Frame["Situation"].grid_rowconfigure(1, weight=1)
            self.Frame["Situation"].grid_columnconfigure(2, weight=1)

            self.Situation_Widget["Label"]["Count"].bind("<<Update_ScheduleCount>>", lambda e: update_situation_count())

            Tooltip = {
                "Button_Add": Hovertip(self.Situation_Widget["Button"]["Add"], "Add a new schedule item.", hover_delay=300),
                "Button_Delete": Hovertip(self.Situation_Widget["Button"]["Delete"], "Delete the selected schedule item.", hover_delay=300),
                "Button_Copy": Hovertip(self.Situation_Widget["Button"]["Copy"], "Copy the selected schedule item.", hover_delay=300),
            }

        def create_widgets_wifi():
            def click_combobox(event=None):
                try:
                    wifi_data:list = JsonDataFunction.Get_jsonAllData(self.Wifi_JsonPath)["Wifi"]
                    wifi_ids = [data["WifiID"] for data in wifi_data]
                    self.Wifi_Widget["Combobox"]["values"] = wifi_ids
                except Exception as e:
                    error_message = traceback.format_exc()
                    messagebox.showwarning("Error", error_message, parent=self.root)
                    return
            
            def selected_wifi_combobox(event=None):
                try:
                    ### Get situation & Get situation json data.
                    situation_selection = self.Situation_Widget["Listbox"].curselection()
                    situation = self.Situation_Widget["Listbox"].get(situation_selection[0])
                    situation_jsondata = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)[situation]

                    ### Get selected wifi id & update json data.
                    selected_wifi_id = self.Wifi_Widget["Combobox"].get()
                    situation_jsondata["Wifi"]["WifiID"] = selected_wifi_id

                    ### Update json file.
                    JsonDataFunction.Update_jsonFileData(self.Schedule_JsonPath, situation, situation_jsondata)
                    self.Show_SituationData()

                except Exception as e:
                    error_message = traceback.format_exc()
                    messagebox.showwarning("Error", error_message, parent=self.root)
                    return

            self.Wifi_Widget = {}   
            self.Wifi_Widget["Label"] = {}
            self.Wifi_Widget["Button"] = {}
            self.Wifi_Widget["Label"]["WifiID"] = ttk.Label(self.Frame["Wifi"], text="WifiID : ", style="Content_Schedule.TLabel")
            self.Wifi_Widget["Combobox"] = ttk.Combobox(self.Frame["Wifi"], state="readonly", width=30)
            self.Wifi_Widget["Combobox"].bind("<Button-1>", click_combobox)
            self.Wifi_Widget["Combobox"].bind("<<ComboboxSelected>>", selected_wifi_combobox)
            self.Wifi_Widget["Label"]["Schedule"] = ttk.Label(self.Frame["Wifi"], text="Schedule : ", style="WifiSchedule_Schedule.TLabel")
            self.Wifi_Widget["Button"]["SetSchedule"] = Button(self.Frame["Wifi"], text="Schedule", width=10, command=self.Button_Wifi_SetSchedule)

            self.Wifi_Widget["Label"]["WifiID"].grid(row=0, column=0, padx=(5,0), pady=(5,0), sticky="w")
            self.Wifi_Widget["Combobox"].grid(row=0, column=1, padx=5, pady=(5,0), sticky="we")
            self.Wifi_Widget["Label"]["Schedule"].grid(row=1, column=0, columnspan=2, padx=5, pady=(5,0), sticky="w")
            self.Wifi_Widget["Button"]["SetSchedule"].grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
            self.Frame["Wifi"].grid_columnconfigure(1, weight=1)

            Tooltip = {
                "Button_SetSchedule": Hovertip(self.Wifi_Widget["Button"]["SetSchedule"], "Set the schedule for the selected Wifi ID.", hover_delay=300),
            }

        def create_widgets_script():
            def sort_by_column(col:str, reverse:bool):
                data = [(self.Script_Widget["TreeView"].set(item, col), item) for item in self.Script_Widget["TreeView"].get_children('')]
                data.sort(reverse=reverse, key=lambda t: t[0])
                for index, (val, item) in enumerate(data):
                    self.Script_Widget["TreeView"].move(item, '', index)
                self.Script_Widget["TreeView"].heading(col, command=lambda: sort_by_column(col=col, reverse=not reverse))
            
            def update_script_count(event=None):
                    total_scripts = len(self.Script_Widget["TreeView"].get_children())
                    self.Script_Widget["Label"]["Count"].config(text=f"Total: {total_scripts}")

            self.Script_Widget = {}
            self.Script_Widget["Label"] = {}
            self.Script_Widget["Button"] = {}

            self.Script_Widget["TreeView"] = ttk.Treeview(self.Frame["Script"], columns=("ScriptID", "Schedule"), height=6, show="headings", selectmode="extended")
            self.Script_Widget["Scrollerbar"] = ttk.Scrollbar(self.Frame["Script"], orient=tk.VERTICAL, command=self.Script_Widget["TreeView"].yview)
            self.Script_Widget["TreeView"].configure(yscrollcommand=self.Script_Widget["Scrollerbar"].set)
            for i, column_name in enumerate(["ScriptID", "Schedule"]):
                self.Script_Widget["TreeView"].heading(column_name, anchor="w", text=column_name, 
                                                       command=lambda col=column_name: sort_by_column(col=col, reverse=False))
                self.Script_Widget["TreeView"].column(column_name, anchor="w", minwidth=150)
            self.Script_Widget["Button"]["Add"] = Button(self.Frame["Script"], text="Add", width=10, command=self.Button_Script_Add)
            self.Script_Widget["Button"]["Delete"] = Button(self.Frame["Script"], text="Delete", width=10, command=self.Button_Script_Delete)
            self.Script_Widget["Button"]["SetSchedule"] = Button(self.Frame["Script"], text="Schedule", width=10, command=self.Button_Script_SetSchedule)
            self.Script_Widget["Label"]["Count"] = ttk.Label(self.Frame["Script"], text="Total: 0", style="DataCount_Schedule.TLabel")

            self.Script_Widget["TreeView"].grid(row=0, column=0, columnspan=4, padx=(5,0), pady=(5,0), sticky="nsew")
            self.Script_Widget["Scrollerbar"].grid(row=0, column=4, padx=(0,5), pady=5, sticky="ns")
            self.Script_Widget["Button"]["Add"].grid(row=1, column=0, padx=(5,0), pady=5, sticky="w")
            self.Script_Widget["Button"]["Delete"].grid(row=1, column=1, padx=(5,0), pady=5, sticky="w")
            self.Script_Widget["Button"]["SetSchedule"].grid(row=1, column=2, padx =5, pady=5, sticky="w")
            self.Script_Widget["Label"]["Count"].grid(row=1, column=3, columnspan=2, padx=(0,5), pady=5, sticky="e")

            self.Frame["Script"].grid_rowconfigure(0, weight=1) 
            self.Frame["Script"].grid_columnconfigure(3, weight=1)  

            self.Script_Widget["Label"]["Count"].bind("<<Update_ScriptCount>>", lambda e: update_script_count())

            Tooltip = {
                "Button_Add": Hovertip(self.Script_Widget["Button"]["Add"], "Add a new script schedule.", hover_delay=300),
                "Button_Delete": Hovertip(self.Script_Widget["Button"]["Delete"], "Delete the selected script schedule.", hover_delay=300),
                "Button_Edit": Hovertip(self.Script_Widget["Button"]["SetSchedule"], "Edit the selected script schedule.", hover_delay=300),
            }

        def create_widgets_client():
            def update_client_count(event=None):
                count = self.Client_Widget["Listbox"].size()
                self.Client_Widget["Label"]["Count"].config(text=f"Total: {count}")

            self.Client_Widget = {}
            self.Client_Widget["Label"] = {}
            self.Client_Widget["Button"] = {}

            self.Client_Widget["Listbox"] = tk.Listbox(self.Frame["Client"], 
                                                       selectmode=tk.EXTENDED, 
                                                       activestyle="dotbox", 
                                                       selectbackground="#c6def4",
                                                       selectforeground="black",
                                                       font=("Segoe UI", 9))
            self.Client_Widget["Scrollbar"] = ttk.Scrollbar(self.Frame["Client"], orient=tk.VERTICAL, command=self.Client_Widget["Listbox"].yview)
            self.Client_Widget["Listbox"].configure(yscrollcommand=self.Client_Widget["Scrollbar"].set)
            self.Client_Widget["Button"]["Add"] = Button(self.Frame["Client"], text="Add", width=10, command=self.Button_Client_Add)
            self.Client_Widget["Button"]["Delete"] = Button(self.Frame["Client"], text="Delete", width=10, command=self.Button_Client_Delete)
            self.Client_Widget["Label"]["Count"] = ttk.Label(self.Frame["Client"], text="Total: 0", style="DataCount_Schedule.TLabel")

            self.Client_Widget["Listbox"].grid(row=0, column=0, columnspan=3, padx=(5,0), pady=(5,0), sticky="nsew")
            self.Client_Widget["Scrollbar"].grid(row=0, column=3, padx=0, pady=(5,0), sticky="ns")
            self.Client_Widget["Button"]["Add"].grid(row=1, column=0, padx=(5,0), pady=5, sticky="w")
            self.Client_Widget["Button"]["Delete"].grid(row=1, column=1, padx=(5,0), pady=5, sticky="w")
            self.Client_Widget["Label"]["Count"].grid(row=1, column=2, columnspan=3, padx=(0,5), pady=5, sticky="e")
            self.Frame["Client"].grid_rowconfigure(0, weight=1)
            self.Frame["Client"].grid_columnconfigure(2, weight=1)
            
            self.Client_Widget["Label"]["Count"].bind("<<Update_ClientCount>>", lambda e: update_client_count())

            Tooltip = {
                "Button_Add": Hovertip(self.Client_Widget["Button"]["Add"], "Add a new client.", hover_delay=300),
                "Button_Delete": Hovertip(self.Client_Widget["Button"]["Delete"], "Delete the selected client.", hover_delay=300),
            }   

        ### Main Frame
        self.Frame = {}
        self.Frame["Main"] = tk.Frame(self.root, borderwidth=1, relief="flat", highlightbackground="#a9a7a7", highlightthickness=1)
        self.Frame["Main"].grid(row=0, column=0, padx=5, pady=5, sticky="nsew")  
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        ### Create Each Frames ( Situation & Wifi & PanedWindow & Canvas ).
        self.Title = {}
        self.Title["SetSchedule"] = ttk.Label(self.Frame["Main"], text="Schedule Setting", style="Title_Schedule.TLabel")
        self.Frame["Situation"] = ttk.LabelFrame(self.Frame["Main"], text="Situation", borderwidth=1, relief="flat", style="FrameTitle_Schedule.TLabelframe")
        self.Frame["Wifi"] = ttk.LabelFrame(self.Frame["Main"],  text="Wifi", borderwidth=1, relief="flat", style="FrameTitle_Schedule.TLabelframe", width=300)
        self.Title["Canvas"] = ttk.Label(self.Frame["Main"], text="Situation Chart", style="Title_Schedule.TLabel")
        self.Frame["PanedWindow"] = tk.PanedWindow(self.Frame["Main"], orient=tk.VERTICAL, sashwidth=5)
        self.Frame["SituationCanvas"] = ttk.Frame(self.Frame["Main"], borderwidth=1, relief="flat", width=1500)
        # Create Situation Canvas.
        self.SituationCanvas = Frame_SituationCanvas(self.Frame["SituationCanvas"])

        # self.Title["SetSchedule"].grid(row=0, column=0, padx=5, pady=(5,0), sticky="w")
        self.Frame["Situation"].grid(row=1, column=0, rowspan=2, padx=(5,0), pady=5, sticky="nsew")
        self.Frame["Wifi"].grid(row=1, column=1, padx=5, pady=(5,0), sticky="nsew")
        self.Frame["PanedWindow"].grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        self.Frame["SituationCanvas"].grid(row=1, column=2, rowspan=2, padx=(0,5), pady=5, sticky="nsew")

        ### Create Script & Client Frame in PanedWindow.
        self.Frame["Script"] = ttk.LabelFrame(self.Frame["PanedWindow"],  text="Script", borderwidth=1, relief="flat", style="FrameTitle_Schedule.TLabelframe")
        self.Frame["Client"] = ttk.LabelFrame(self.Frame["PanedWindow"],  text="Client", borderwidth=1, relief="flat", style="FrameTitle_Schedule.TLabelframe")
        self.Frame["PanedWindow"].add(self.Frame["Script"], minsize=150)
        self.Frame["PanedWindow"].add(self.Frame["Client"], minsize=150)

        self.Frame["Main"].grid_rowconfigure(2, weight=1)  
        self.Frame["Main"].grid_columnconfigure(2, weight=1)

        create_widgets_situation()
        create_widgets_wifi()
        create_widgets_script()
        create_widgets_client()

    def Load_ScheduleData(self):
        ScheduleData = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)
        situations = JsonDataFunction.Get_DictKey(ScheduleData)

        self.Situation_Widget["Listbox"].delete(0, tk.END)
        for situation in situations:
            self.Situation_Widget["Listbox"].insert(tk.END, situation)

        self.Situation_Widget["Listbox"].selection_set(0)
        self.Show_SituationData()

    def Show_SituationData(self, event=None):
        try:
            ### Get Selected Item.
            ### return when no item is selected.
            selection = self.Situation_Widget["Listbox"].curselection()
            if selection == ():     return
            
            ### Get json Data.
            situation = self.Situation_Widget["Listbox"].get(selection[0])
            ScheduleData = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)
            wifi_data:dict = ScheduleData[situation]["Wifi"]
            script_data:list = ScheduleData[situation]["Script"]
            client_data:list = ScheduleData[situation]["ClientID"]

            ### Set Wifi data.
            self.Wifi_Widget["Combobox"].set(wifi_data["WifiID"])
            wifi_schedule = wifi_data["Schedule"]
            if len(wifi_schedule) >=40:
                wifi_schedule = wifi_schedule[:37] + "..."
            self.Wifi_Widget["Label"]["Schedule"].config(text=f"Schedule : {wifi_schedule}")

            ### Set Script data.
            self.Script_Widget["TreeView"].delete(*self.Script_Widget["TreeView"].get_children())
            for script in script_data:
                self.Script_Widget["TreeView"].insert("", tk.END, values=(script["ScriptID"], script["Schedule"]))  

            ### Set Client data.
            self.Client_Widget["Listbox"].delete(0, tk.END)
            for client in client_data:
                self.Client_Widget["Listbox"].insert(tk.END, client)
            
            ### Update Count.
            ### Update Canvas.
            self.Update_Count()
            self.SituationCanvas.Draw_Everything(situation=situation)

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return
        
    ###================================================================================
    ### Button for Situation.
    def Button_Situation_Add(self):
        def add_situation(situation_name:str):
            ### Get Sehdule json data.
            ### Get Wifi json data.
            schedule_jsondata = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)
            wifi_jsondata = JsonDataFunction.Get_jsonAllData(self.Wifi_JsonPath)

            ### Update situation in json file & Update GUI.
            new_schedule_data = {"Wifi": {
                                            "WifiID": wifi_jsondata["Wifi"][0]["WifiID"],
                                            "Schedule": "1,00:00,1440" 
                                        },
                                    "Script": [],
                                    "ClientID": []
                                }
            
            ### Update json file & Update GUI.
            ### Insert new situation to self.Situation_Widget["Listbox"]
            JsonDataFunction.Update_jsonFileData(self.Schedule_JsonPath, situation_name, new_schedule_data)
            self.Situation_Widget["Listbox"].insert(tk.END, situation_name)
            self.Situation_Widget["Listbox"].selection_clear(0, tk.END)
            self.Situation_Widget["Listbox"].selection_set(tk.END)
            self.Show_SituationData()

        try:
            situationname_frame = tk.Toplevel(self.root)
            situationname_frame.transient(self.root)  # Set to be on top of the main window
            situationname_frame.grab_set()
            situationname_frame.protocol("WM_DELETE_WINDOW", situationname_frame.destroy)  # Disable the close button
            app = Page_SetSituationName(situationname_frame, 
                                        title="Add New Situation", 
                                        confirm_callback=add_situation)
            
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

    def Button_Situation_Delete(self):
        try:
            ### Get Situation size.
            size = self.Situation_Widget["Listbox"].size()

            ### Delete Selected Item.
            selected_item = self.Situation_Widget["Listbox"].curselection()[0]
            selected_name = self.Situation_Widget["Listbox"].get(selected_item)
            
            ### Set New Selection.
            self.Situation_Widget["Listbox"].delete(selected_item)
            if selected_item == size-1 and selected_item != 0:
                self.Situation_Widget["Listbox"].selection_set(selected_item-1)
            else:
                self.Situation_Widget["Listbox"].selection_set(selected_item)

            ### Delete Selected Item from JSON.
            JsonDataFunction.Remove_jsonFileKey(self.Schedule_JsonPath, selected_name)
            self.Show_SituationData()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

    def Button_Situation_Copy(self):
        def copy_situation(situation_name):
            ### Get Sehdule json data.
            schedule_jsondata = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)

            ### Get Selected Situation Name.
            ### Get Selected Situation json data.
            situation_selection = self.Situation_Widget["Listbox"].curselection()
            situation = self.Situation_Widget["Listbox"].get(situation_selection[0])
            schedule_jsondata[situation]["ClientID"] = []
            selected_situation_jsondata = schedule_jsondata[situation]

            ### Update situation in json file & Update GUI.
            JsonDataFunction.Update_jsonFileData(self.Schedule_JsonPath, situation_name, selected_situation_jsondata)
            self.Situation_Widget["Listbox"].insert(tk.END, situation_name)
            self.Situation_Widget["Listbox"].selection_clear(0, tk.END)
            self.Situation_Widget["Listbox"].selection_set(tk.END)
            self.Show_SituationData()

        try:
            ### Get Selected Situation Name.
            situation_selection = self.Situation_Widget["Listbox"].curselection()
            situation = self.Situation_Widget["Listbox"].get(situation_selection[0])

            situationname_frame = tk.Toplevel(self.root)
            situationname_frame.transient(self.root)  # Set to be on top of the main window
            situationname_frame.grab_set()
            situationname_frame.protocol("WM_DELETE_WINDOW", situationname_frame.destroy)  # Disable the close button
            app = Page_SetSituationName(situationname_frame, 
                                        title=f"Copy Situation [{situation}]", 
                                        confirm_callback=copy_situation)
            
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

    ### Button for Wifi.
    def Button_Wifi_SetSchedule(self):
        def set_wifi_schedule(time_data):
            ### Get situation & Get situation json data.
            situation_selection = self.Situation_Widget["Listbox"].curselection()
            situation = self.Situation_Widget["Listbox"].get(situation_selection[0])
            situation_jsondata = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)[situation]

            ### Update situation wifi schedule in json file & Update GUI.
            situation_jsondata["Wifi"]["Schedule"] = time_data
            JsonDataFunction.Update_jsonFileData(self.Schedule_JsonPath, situation, situation_jsondata)
            self.Show_SituationData()   
            
        try:
            ### Get situation.
            situation_selection = self.Situation_Widget["Listbox"].curselection()
            situation = self.Situation_Widget["Listbox"].get(situation_selection[0])
            time_data = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)[situation]["Wifi"]["Schedule"]

            ### Open Set Schedule Window.
            setschedule_frame = tk.Toplevel(self.root)
            setschedule_frame.transient(self.root)  # Set to be on top of the main window
            setschedule_frame.grab_set()
            setschedule_frame.protocol("WM_DELETE_WINDOW", setschedule_frame.destroy)  # Disable the close button
            app = Page_SetWeeklyTime(setschedule_frame, 
                                    title="Wifi", 
                                    time_data=time_data,
                                    confirm_callback=set_wifi_schedule)

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return
    
    ### Button for Script.
    def Button_Script_Add(self):
        def add_script_name(script_name:str):
            ### Get situation & Get situation json data.
            situation_selection = self.Situation_Widget["Listbox"].curselection()
            situation = self.Situation_Widget["Listbox"].get(situation_selection[0])
            situation_jsondata = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)[situation]

            ### Update situation script in json file & Update GUI.
            situation_jsondata["Script"].append({"ScriptID": script_name, "Schedule": "1,00:00,1440"})
            JsonDataFunction.Update_jsonFileData(self.Schedule_JsonPath, situation, situation_jsondata)
            self.Show_SituationData() 

        try:
            situation = self.Situation_Widget["Listbox"].get(self.Situation_Widget["Listbox"].curselection()[0])
                                                             
            scriptname_frame = tk.Toplevel(self.root)
            scriptname_frame.transient(self.root)  # Set to be on top of the main window
            scriptname_frame.grab_set()
            scriptname_frame.protocol("WM_DELETE_WINDOW", scriptname_frame.destroy)  # Disable the close button
            app = Page_AddScript(scriptname_frame, 
                                title="Add New Situation", 
                                situation=situation,
                                confirm_callback=add_script_name)
            
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return
    
    def Button_Script_Delete(self):
        try:
            ### Get Selected Item.
            selection = self.Script_Widget["TreeView"].selection()
            if selection == ():
                messagebox.showwarning("Warning", "No script selected.", parent=self.root)
                return

            ### Get situation & Get situation json data.
            situation_selection = self.Situation_Widget["Listbox"].curselection()
            situation = self.Situation_Widget["Listbox"].get(situation_selection[0])
            situation_jsondata = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)[situation]

            ### Remove Selected Item from GUI & JSON.
            for item in selection:
                selected_script = self.Script_Widget["TreeView"].item(item, "values")
                script_data = {"ScriptID": selected_script[0], "Schedule": selected_script[1]}
                situation_jsondata["Script"].remove(script_data)

            ### Update situation script in json file & Update GUI.
            JsonDataFunction.Update_jsonFileData(self.Schedule_JsonPath, situation, situation_jsondata)
            self.Show_SituationData()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

    def Button_Script_SetSchedule(self):
        def set_script_schedule(time_data):
            ### Get situation & Get situation json data.
            situation_selection = self.Situation_Widget["Listbox"].curselection()
            situation = self.Situation_Widget["Listbox"].get(situation_selection[0])
            situation_jsondata = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)[situation]

            ### Get Selected Script ID.
            ### Update situation script schedule in json data.
            script_selection = self.Script_Widget["TreeView"].selection()
            for item in script_selection:
                script_id = self.Script_Widget["TreeView"].item(item)["values"][0]
                for script in situation_jsondata["Script"]:
                    if script["ScriptID"] == script_id:
                        script["Schedule"] = time_data
                        break

            ### Update situation script in json file & Update GUI.
            JsonDataFunction.Update_jsonFileData(self.Schedule_JsonPath, situation, situation_jsondata)
            self.Show_SituationData()

        ### Get Selected Item.
        selection = self.Script_Widget["TreeView"].selection()
        if selection == ():
            messagebox.showwarning("Warning", "No script selected.", parent=self.root)
            return
        
        ### Get script time_data.
        item_data = self.Script_Widget["TreeView"].item(selection[0])["values"]
        time_data = item_data[1]

        ### Open Set Schedule Window.
        setschedule_frame = tk.Toplevel(self.root)
        setschedule_frame.transient(self.root)  # Set to be on top of the main window
        setschedule_frame.grab_set()
        setschedule_frame.protocol("WM_DELETE_WINDOW", setschedule_frame.destroy)  # Disable the close button
        app = Page_SetWeeklyTime(setschedule_frame, 
                                title="Script", 
                                time_data=time_data,
                                confirm_callback=set_script_schedule)
        
    ### Button for Client.
    def Button_Client_Add(self):
        def add_client_id(client_ids:list):
            ### Get situation & Get situation json data.
            situation_selection = self.Situation_Widget["Listbox"].curselection()
            situation = self.Situation_Widget["Listbox"].get(situation_selection[0])
            situation_jsondata = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)[situation]

            ### Update situation client in json file & Update GUI.
            situation_jsondata["ClientID"] = client_ids

            ### Update situation script in json file & Update GUI.
            JsonDataFunction.Update_jsonFileData(self.Schedule_JsonPath, situation, situation_jsondata)
            self.Show_SituationData()

        try:
            situation = self.Situation_Widget["Listbox"].get(self.Situation_Widget["Listbox"].curselection()[0])
                                                             
            clientid_frame = tk.Toplevel(self.root)
            clientid_frame.transient(self.root)  # Set to be on top of the main window
            clientid_frame.grab_set()
            clientid_frame.protocol("WM_DELETE_WINDOW", clientid_frame.destroy)  # Disable the close button
            app = Page_AddClient(clientid_frame, 
                                title="Select Client IDs", 
                                situation=situation,
                                confirm_callback=add_client_id)
            
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return
    
    def Button_Client_Delete(self):
        try:
            ### Get Selected Item.
            selection = self.Client_Widget["Listbox"].curselection()
            if selection == ():
                messagebox.showwarning("Warning", "No client selected.", parent=self.root)
                return

            ### Get situation & Get situation json data.
            situation_selection = self.Situation_Widget["Listbox"].curselection()
            situation = self.Situation_Widget["Listbox"].get(situation_selection[0])
            situation_jsondata = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)[situation]

            ### Remove Selected Item from GUI & JSON.
            for index in reversed(selection):
                selected_client = self.Client_Widget["Listbox"].get(index)
                situation_jsondata["ClientID"].remove(selected_client)

            ### Update situation script in json file & Update GUI.
            JsonDataFunction.Update_jsonFileData(self.Schedule_JsonPath, situation, situation_jsondata)
            self.Show_SituationData()
            

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return
    
    ###================================================================================
    ### Update Count for Situation, Script, Client.
    def Update_Count(self):
        self.Situation_Widget["Label"]["Count"].event_generate("<<Update_ScheduleCount>>")
        self.Script_Widget["Label"]["Count"].event_generate("<<Update_ScriptCount>>")
        self.Client_Widget["Label"]["Count"].event_generate("<<Update_ClientCount>>")

    def Reload_JsonData(self):
        self.load_json_data()
        self.Load_ScheduleData()

if __name__ == "__main__":
    height = 600
    width = 800
    root = tk.Tk()
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.resizable(True, True)
    root.title("Schedule")
    app = Frame_Schedule(root)
    root.mainloop()