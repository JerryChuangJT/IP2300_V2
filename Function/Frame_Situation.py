import tkinter as tk
from tkinter import ttk, messagebox
from idlelib.tooltip import Hovertip  
import os
import traceback
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import Function.MyFunction_JsonData as JsonDataFunction
from Function.MyFunction_Telnet import TelNet

from Class.Class_Button import Button

class Frame_Situation():
    def __init__(self, root=None, runtest_callback=None, stoptest_callback=None):
        self.runtest_callback = runtest_callback
        self.stoptest_callback = stoptest_callback
        self.root = root

        style = ttk.Style()
        style.configure("Title_Situation.TLabel", font=("Segoe UI", 14, "bold"), foreground="blue")
        style.configure("Message1_Situation.TLabel", font=("Segoe UI", 8), foreground="#717171")
        style.configure("Message2_Situation.TLabel", font=("Segoe UI", 8), foreground="Red")
        style.configure("Count_Situation.TLabel", font=("Segoe UI", 9), foreground="#6C6C6C")
        
        ### 設定 Treeview 選擇背景顏色
        style.map("Treeview",
                  background=[('selected', "#c6def4")],
                  foreground=[('selected', 'black')])

        ### Selected Situations Set 
        ### self.Thread_StopEvent is used to stop the thread when the window is closed.
        self.Selected_Situations = set()
        self.Thread_StopEvent = threading.Event()
        
        self.load_json_data()
        self.Create_Widgets()
        self.Load_SituationData()
        self.Updating_TreeViewCount()

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)
        
        self.Schedule_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Schedule.json"
        self.Schedule_JsonData = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)

        self.Client_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Client.json"
        self.Client_JsonData = JsonDataFunction.Get_jsonAllData(self.Client_JsonPath)

        self.SelectedSituation_JsonPath = "./temp/json_SelectedSituaion.json"

    def Create_Widgets(self):
        def on_tree_select(event=None):
            try:
                ### Check click region, column, item, parent
                region = self.Main_Widgets["Treeview"].identify_region(event.x, event.y)
                if region != "cell":
                    return 
                
                column = self.Main_Widgets["Treeview"].identify_column(event.x)
                if column != "#1":
                    return  
                
                item = self.Main_Widgets["Treeview"].identify_row(event.y)
                if not item:
                    return 

                parent = self.Main_Widgets["Treeview"].parent(item)
                if parent != "":
                    return  
                
                ### Execute selection toggle logic
                situation_name = self.Main_Widgets["Treeview"].item(item, "values")[0][1:]  # 去掉前面的勾選框符號
                current_values = self.Main_Widgets["Treeview"].item(item, "values")

                if situation_name in self.Selected_Situations:
                    self.Selected_Situations.remove(situation_name)
                    new_values = (f"☐{situation_name}",) + current_values[1:]
                else:
                    self.Selected_Situations.add(situation_name)
                    new_values = (f"⏹{situation_name}",) + current_values[1:]

                self.Main_Widgets["Treeview"].item(item, values=new_values)
                self.Updating_TreeViewCount()
            
            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showwarning("Error", error_message, parent=self.root)
                return

        def sort_by_column(col:str, reverse:bool):
            try:
                data = [(self.Main_Widgets["Treeview"].set(item, col), item) for item in self.Main_Widgets["Treeview"].get_children('')]
                data.sort(reverse=reverse, key=lambda t: t[0])
                for index, (val, item) in enumerate(data):
                    self.Main_Widgets["Treeview"].move(item, '', index)
                self.Main_Widgets["Treeview"].heading(col, command=lambda: sort_by_column(col=col, reverse=not reverse))

            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showwarning("Error", error_message, parent=self.root)
                return

        ### Create Frames ###
        self.Frame = {}
        self.Frame["Main"] = tk.Frame(self.root, borderwidth=1, relief="flat", highlightbackground="#a9a7a7", highlightthickness=1)

        self.Frame["Main"].grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1), 
        self.root.grid_columnconfigure(0, weight=1)

        ### Create Treeview & Scrollbar ###
        self.Main_Widgets = {}
        treeview_columns = ("Situation", "WifiID", "Script Count", "Client Count")
        self.Main_Widgets["Treeview"] = ttk.Treeview(self.Frame["Main"], 
                                                     columns=treeview_columns, 
                                                     show="tree headings", 
                                                     takefocus=False,
                                                     height=20)
        for i,col in enumerate(treeview_columns):
            self.Main_Widgets["Treeview"].heading(col, text=col, command=lambda col=col: sort_by_column(col=col, reverse=False))

        self.Main_Widgets["Treeview"].column("Situation", width=200, anchor="w")
        self.Main_Widgets["Treeview"].column("WifiID", width=150, anchor="w")
        self.Main_Widgets["Treeview"].column("Script Count", width=100, anchor="center")
        self.Main_Widgets["Treeview"].column("Client Count", width=100, anchor="center")
        self.Main_Widgets["Scrollbar"] = ttk.Scrollbar(self.Frame["Main"], orient=tk.VERTICAL, command=self.Main_Widgets["Treeview"].yview)
        self.Main_Widgets["Treeview"].configure(yscrollcommand=self.Main_Widgets["Scrollbar"].set)
        self.Main_Widgets["Treeview"].bind("<Button-1>", on_tree_select)
        
        # 完全禁用聚焦功能 - 連點擊都不會聚焦
        self.Main_Widgets["Treeview"].focus_set = lambda: None
        self.Main_Widgets["Treeview"].focus = lambda: None

        ### Create Buttons & Labels ###
        self.Main_Widgets["Button"] = {}
        self.Main_Widgets["Label"] = {}
        self.Main_Widgets["Label"]["Title"] = ttk.Label(self.Frame["Main"], text="Situation", style="Title_Situation.TLabel")
        self.Main_Widgets["Button"]["Expand"] = Button(self.Frame["Main"], image_path="./img/expand_data.png", size=(30,30), command=self.Button_ExpandData)
        self.Main_Widgets["Button"]["SelecteAll"] = Button(self.Frame["Main"], image_path="./img/selectall.png", size=(30,30), command=self.Button_SelectAll)
        self.Main_Widgets["Button"]["Reload"] = Button(self.Frame["Main"], image_path="./img/reload.png", size=(30,30), command=self.Button_ReloadData)
        self.Main_Widgets["Button"]["Run"] = Button(self.Frame["Main"], image_path="./img/run.png", size=(30,30), command=self.Button_Run)
        # self.Main_Widgets["Button"]["Stop"] = Button(self.Frame["Main"], image_path="./img/stop.png", size=(30,30), command=self.Button_Stop)
        self.Main_Widgets["Label"]["Message"] = ttk.Label(self.Frame["Main"], text=f"{self.Schedule_JsonPath}", style="Message1_Situation.TLabel")
        self.Main_Widgets["Label"]["Count"] = ttk.Label(self.Frame["Main"], text="Total : 0/0", style="Count_Situation.TLabel")

        ### Layout Widgets ###
        self.Main_Widgets["Label"]["Title"].grid(row=0, column=0, padx=(5,0), pady=(5,0), sticky="nw")
        self.Main_Widgets["Button"]["Expand"].grid(row=1, column=0, padx=(5,0), pady=(5,0), sticky="w")
        self.Main_Widgets["Button"]["SelecteAll"].grid(row=1, column=0, padx=(43,0), pady=(5,0), sticky="w")
        self.Main_Widgets["Button"]["Reload"].grid(row=1, column=0, padx=(85,0), pady=(5,0), sticky="w")
        self.Main_Widgets["Button"]["Run"].grid(row=1, column=0, padx=(0,40), pady=(5,0), sticky="e")
        # self.Main_Widgets["Button"]["Stop"].grid(row=1, column=0, padx=(0,0), pady=(5,0), sticky="e")
        self.Main_Widgets["Treeview"].grid(row=2, column=0, padx=(5,0), pady=(5,0), sticky="nsew")
        self.Main_Widgets["Scrollbar"].grid(row=2, column=1, padx=0, pady=(5,0), sticky="ns")
        self.Main_Widgets["Label"]["Message"].grid(row=3, column=0, padx=(5,0), pady=5, sticky="w")
        self.Main_Widgets["Label"]["Count"].grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.Frame["Main"].grid_rowconfigure(2, weight=1)
        self.Frame["Main"].grid_columnconfigure(0, weight=1)

        Tooltip = {
            "Button_Expand": Hovertip(self.Main_Widgets["Button"]["Expand"], "Expand/Collapse all situations.", hover_delay=300),
            "Button_SelecteAll": Hovertip(self.Main_Widgets["Button"]["SelecteAll"], "Select/Deselect all situations.", hover_delay=300),
            "Button_Reload": Hovertip(self.Main_Widgets["Button"]["Reload"], "Reload the situations.", hover_delay=300),
            "Button_Run": Hovertip(self.Main_Widgets["Button"]["Run"], "Run the selected situations.", hover_delay=300),
            # "Button_Stop": Hovertip(self.Main_Widgets["Button"]["Stop"], "Stop the running situations.", hover_delay=300)
        }

    def Load_SituationData(self):
        try:              
            ### Clear all data in Treeview 
            for item in self.Main_Widgets["Treeview"].get_children():
                self.Main_Widgets["Treeview"].delete(item)
            self.Selected_Situations.clear()


            ### Load Situation Data from JSON 
            def load_situation_data():
                for situation_name, situation_data in self.Schedule_JsonData.items():
                    wifi_id = situation_data['Wifi']['WifiID'] if 'Wifi' in situation_data and 'WifiID' in situation_data['Wifi'] else "N/A"
                    script_count = len(situation_data['Script']) if 'Script' in situation_data else 0
                    client_count = len(situation_data['ClientID']) if 'ClientID' in situation_data else 0
                    root_data = self.Main_Widgets["Treeview"].insert("", 
                                                                    "end", 
                                                                    values=(f"☐{situation_name}", wifi_id, script_count, client_count), 
                                                                    open=False)  
                    if situation_data["ClientID"]:
                        for i, client in enumerate(situation_data['ClientID'], 1):
                            self.Main_Widgets["Treeview"].insert(root_data, 
                                                                "end", values=(f"        ▪ {client}", "", "", ""))
                            
            ### Wait for a moment to allow UI update
            self.root.after(50, load_situation_data)

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

    def Updating_TreeViewCount(self):
        try:
            total_situations = len(self.Schedule_JsonData)
            selected_situations = len(self.Selected_Situations)
            self.Main_Widgets["Label"]["Count"].config(text=f"Total : {selected_situations}/{total_situations}")

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

    ###=============================================================================================
    def Button_ExpandData(self):
        try:
            ### Check any open=True in Treeview.
            if any(self.Main_Widgets["Treeview"].item(item, "open") for item in self.Main_Widgets["Treeview"].get_children()):
                for item in self.Main_Widgets["Treeview"].get_children():
                    self.Main_Widgets["Treeview"].item(item, open=False)
            else:
                for item in self.Main_Widgets["Treeview"].get_children():
                    self.Main_Widgets["Treeview"].item(item, open=True)
                
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return
        
    def Button_SelectAll(self):
        try:
            if self.Selected_Situations == set():
                for item in self.Main_Widgets["Treeview"].get_children():
                    situation_name = self.Main_Widgets["Treeview"].item(item, "values")[0][1:]  # 去掉前面的勾選框符號
                    self.Selected_Situations.add(situation_name)
                    self.Main_Widgets["Treeview"].item(item, values=(f"⏹{situation_name}",) + self.Main_Widgets["Treeview"].item(item, "values")[1:])
            else:
                for situation_name in list(self.Selected_Situations):
                    self.Selected_Situations.remove(situation_name)
                for item in self.Main_Widgets["Treeview"].get_children():
                    situation_name = self.Main_Widgets["Treeview"].item(item, "values")[0][1:]  # 去掉前面的勾選框符號
                    self.Main_Widgets["Treeview"].item(item, values=(f"☐{situation_name}",) + self.Main_Widgets["Treeview"].item(item, "values")[1:])
            
            self.Updating_TreeViewCount()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return
    
    def Button_ReloadData(self):
        try:
            self.load_json_data()
            self.Load_SituationData()
            self.Updating_TreeViewCount()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

    def Button_Run(self):
        ### Check Treeview information is correct before running test.
        def check_treeveiw_information()->bool:
            items = self.Main_Widgets["Treeview"].get_children()
            if len(items) != len(self.Schedule_JsonData):
                messagebox.showwarning("Warning", f"Situation count not match.\nReload the data before running test.", parent=self.root)
                return False
            
            for item in items:
                item_data = self.Main_Widgets["Treeview"].item(item, "values")
                if check_treeveiw_item_data(item_data) is False:
                    messagebox.showwarning("Warning", f"Something wrong in data.\nReload the data before running test.", parent=self.root)
                    return False
            return True
        
        def check_treeveiw_item_data(item_data:list)->bool:
            situation_name = item_data[0][1:]  # 去掉前面的勾選框符號
            wifi_id = item_data[1]
            script_count = item_data[2]
            client_count = item_data[3]

            if situation_name not in self.Schedule_JsonData:
                return False
            if wifi_id != self.Schedule_JsonData[situation_name]["Wifi"]["WifiID"]:
                return False
            if script_count != str(len(self.Schedule_JsonData[situation_name]["Script"])):
                return False
            if client_count != str(len(self.Schedule_JsonData[situation_name]["ClientID"])):
                return False
            return True

        ### Update Selected Situation to JSON File.
        def update_selected_situation_json():
            ### Update Selected Situation to JSON File.
            list_Seleted = list(self.Selected_Situations)
            list_Seleted.sort()
            JsonDataFunction.Update_jsonFileData(self.SelectedSituation_JsonPath, "Situation", list_Seleted)

            ### Update selected clients to JSON File.
            selected_clients = []
            for situation in list_Seleted:
                clients = self.Schedule_JsonData[situation]["ClientID"]
                selected_clients.extend(clients)
            selected_clients.sort()
            JsonDataFunction.Update_jsonFileData(self.SelectedSituation_JsonPath, "ClientID", selected_clients)

        ### Check Telnet Connection.s
        def check_telnet_connection(host:str, port:int=23):
            try:
                device = TelNet(host, port) 
                return {"Device":host,
                        "Result":device.Check_Connection()[0]}
            except Exception as e:
                error_message = traceback.format_exc()
                self.Show_MessageBox("Error", error_message)

        def check_connection_result(ether_checkresult:dict)->bool:
            if len(ether_checkresult["FAIL"]) > 0:
                messagebox.showwarning("Error", f"{len(ether_checkresult['FAIL'])} of device connection fail.\n\n{ether_checkresult['FAIL']}", parent=self.root)   
                return False
            return True

        def Thread_Function():
            def get_client_ip(client_id:str=None)->str:
                for client_data in self.Client_JsonData["Client"]:
                    if client_data["ClientID"] == client_id:
                            return client_data["EtherIP"]
                return None
            
            try:
                ### Disable Run & ReloadData Button.          
                self.root.after(0, lambda: self.Main_Widgets["Button"]["Reload"].config(state=tk.DISABLED))
                self.root.after(0, lambda: self.Main_Widgets["Button"]["Run"].config(state=tk.DISABLED))    

                ### Check the TreeView message is corrent before running test.
                self.Show_Message(text=f"Checking Situation Information ...", color="red")
                if check_treeveiw_information() is False:   
                    self.Stop_Test()
                    return

                ### Update Selected Situation to JSON File.
                update_selected_situation_json()
            
                ### Execute Thread Pool.
                ### Check the connection status of each device in self.SelectedSituation_JsonPath["Client"]
                self.Show_Message(text=f"Checking Clients Connection ...", color="red")
                client_ids = JsonDataFunction.Get_jsonAllData(self.SelectedSituation_JsonPath)["ClientID"]
                with ThreadPoolExecutor(max_workers=64, thread_name_prefix="Check_ClientEtherConnection") as executor:
                    futures = []
                    for client_id in client_ids:
                        if self.Thread_StopEvent.is_set():  break
                        futures.append(executor.submit(check_telnet_connection, get_client_ip(client_id), 23))

                    ### Get all result from [futures].
                    total_count = len(futures)
                    completed_count = 0
                    ether_checkresult = {"PASS":[],"FAIL":[]}
                    for future in as_completed(futures):
                        if self.Thread_StopEvent.is_set():  break
                        thread_respone = future.result()
                        ether_checkresult[thread_respone["Result"]].append(thread_respone["Device"])

                        completed_count += 1
                        self.Show_Message(text=f"Check Connection. Processing  {completed_count} / {total_count}  ...", color="red")
                
                ### Show the connection status in self.Main_Widget["TreeView"].
                if self.Thread_StopEvent.is_set():  return
                if check_connection_result(ether_checkresult) is False:  
                    self.Stop_Test()
                    return

                ### Run Test.
                # self.runtest_callback()
                thread_Runtest = threading.Thread(target=self.runtest_callback, daemon=True)
                thread_Runtest.start()   
                len_selected_situations = len(JsonDataFunction.Get_jsonAllData(self.SelectedSituation_JsonPath)["Situation"])
                len_client_ids = len(JsonDataFunction.Get_jsonAllData(self.SelectedSituation_JsonPath)["ClientID"])
                self.Show_Message(text=f" Test Running - Situations: {len_selected_situations} / Clients : {len_client_ids}", color="red")
                
            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showwarning("Error", error_message, parent=self.root)

                self.root.after(0, lambda: self.Main_Widgets["Button"]["Reload"].config(state=tk.NORMAL))
                self.root.after(0, lambda: self.Main_Widgets["Button"]["Run"].config(state=tk.NORMAL))
                self.Show_Message(text=f"{self.Schedule_JsonPath}", color="gray") 

                return

        ### Reload Json Data.
        ### Check any situation is selected.
        self.load_json_data() 
        if len(self.Selected_Situations) == 0:
            messagebox.showwarning("Warning", f"No situation selected.\nPlease select at least one situation to run test.", parent=self.root)
            return

        ### Start Thread.
        self.Thread_StopEvent.clear()
        thread = threading.Thread(target=Thread_Function, daemon=True)
        thread.start()   

    def Show_Message(self, text:str="", color:str="gray"):
        if color.lower() == "red":
            style = "Message2_Situation.TLabel"
        elif color.lower() == "gray":
            style = "Message1_Situation.TLabel"

        self.root.after(0, lambda: self.Main_Widgets["Label"]["Message"].config(text=text, style=style))
   
    ###=============================================================================================
    def ReloadJsonData(self):
        self.load_json_data()
        self.Load_SituationData()
        self.Updating_TreeViewCount()

    def on_close(self):
        if hasattr(self, 'Thread_StopEvent'):
            self.Thread_StopEvent.set()
    
    def Stop_Test(self):
        self.root.after(0, lambda: self.Main_Widgets["Button"]["Reload"].config(state=tk.NORMAL))
        self.root.after(0, lambda: self.Main_Widgets["Button"]["Run"].config(state=tk.NORMAL))  
        self.Show_Message(text=f"{self.Schedule_JsonPath}", color="gray")



if __name__ == "__main__":
    width = 1000
    height = 800

    root = tk.Tk()
    root.title("Execution")
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.resizable(True, True)
    app = Frame_Situation(root)     
    root.mainloop()

