import tkinter as tk
from tkinter import ttk, messagebox
from idlelib.tooltip import Hovertip  
import traceback
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from Function.Page_ADBDownload import Page_ADBDownloadLog

import Function.MyFunction_JsonData as JsonDataFunction
from Function.MyFunction_Telnet import TelNet

from Class.Class_Button import Button

class Frame_ADB():
    def __init__(self, root, close_callback=None):
        self.close_callback = close_callback
        self.root = root   
        
        style = ttk.Style()
        style.configure("Title_ADB.TLabel", font=("Segoe UI", 13, "bold"), foreground="blue")
        style.configure("Message1_ADB.TLabel", font=("Segoe UI", 8), foreground="#717171")
        style.configure("Message2_ADB.TLabel", font=("Segoe UI", 8), foreground="Red")
        style.configure("Label_ADB.TLabel", font=("Segoe UI", 10), foreground="black")
        style.configure("Count_ADB.TLabel", font=("Segoe UI", 9), foreground="#6C6C6C")
        style.configure("Log_ADB.TLabel", font=("Segoe UI", 10), foreground="black")

        ### self.Thread_StopEvent is used to stop the thread when the window is closed.
        self.Thread_StopEvent = threading.Event()

        self.load_json_data()
        self.Create_widgets()
        JsonDataFunction.Update_jsonFileData(self.ADBDownload_JsonPath, "Client", [])
  
    def load_json_data(self):
        self.ADBDownload_JsonPath = "./Parameter/json_PageADBDownload.json"
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)
        self.Client_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Client.json"
        self.TreeView_Columns = ["ClientID", "MAC", "EtherIP", "Index"]
        
    def Create_widgets(self):
        def create_main_widgets():
            self.Main_Widget = {}
            self.Main_Widget["Button"] = {}
            self.Main_Widget["Label"] = {}
            self.Main_Widget["Entry"] = {}
            self.Main_Widget["Scrollerbar"] = {}

            ### Create Widgets.
            self.Main_Widget["Title"] = ttk.Label(self.Frame["Main"], text="ADB", style="Title_ADB.TLabel")
            

            self.Main_Widget["Label"]["Search"] = ttk.Label(self.Frame["Main"], text="Search : ",  style="Label_ADB.TLabel")

            self.search_var = tk.StringVar()
            self.Main_Widget["Entry"]["Search"] = ttk.Entry(self.Frame["Main"], textvariable=self.search_var)
            self.search_var.trace_add("write", self.Search_VarFilter)

            self.Main_Widget["Button"]["Download"] = Button(self.Frame["Main"], text="Download", command=self.Button_DownloadLog)
            self.Main_Widget["Button"]["Reload"] = Button(self.Frame["Main"], text="Refresh", command=self.Button_Refresh)
        
            self.Main_Widget["TreeView"] = ttk.Treeview(self.Frame["Main"], columns=self.TreeView_Columns, show="headings", selectmode="extended")
            self.Main_Widget["TreeView"].bind("<ButtonRelease-1>", self.Updating_TreeViewCount)
            self.Main_Widget["Scrollerbar"]["Vertical"] = ttk.Scrollbar(self.Frame["Main"], orient=tk.VERTICAL, command=self.Main_Widget["TreeView"].yview)
            self.Main_Widget["TreeView"].configure(yscrollcommand=self.Main_Widget["Scrollerbar"]["Vertical"].set)
            for i in range(len(self.TreeView_Columns)):
                self.Main_Widget["TreeView"].heading(self.TreeView_Columns[i], 
                                                     text=self.TreeView_Columns[i], 
                                                     anchor="w", 
                                                     command=lambda col=self.TreeView_Columns[i]: sort_by_column(col=col, reverse=False))
                self.Main_Widget["TreeView"].column(self.TreeView_Columns[i], width=50, stretch=True)
            self.Main_Widget["Label"]["Message"] = ttk.Label(self.Frame["Main"], text=f"{self.Client_JsonPath}", style="Message1_ADB.TLabel")
            self.Main_Widget["Label"]["Count"] = ttk.Label(self.Frame["Main"], text="Total : 0/0", style="Count_ADB.TLabel") 

            ### Layout Widgets.
            self.Main_Widget["Title"].grid(row=0, column=0, padx=(5,0), pady=(5,0), sticky="w")            
            self.Main_Widget["Button"]["Download"].grid(row=1, column=1, padx=(0,120), pady=(5,0), sticky="e")
            self.Main_Widget["Button"]["Reload"].grid(row=1, column=1, padx=(0,5), pady=(5,0), sticky="e")
            self.Main_Widget["Label"]["Search"].grid(row=1, column=0, padx=(5,0), pady=(5,0), sticky="w")
            self.Main_Widget["Entry"]["Search"].grid(row=1, column=0, padx=(75,0), pady=(5,0), sticky="w")
            self.Main_Widget["TreeView"].grid(row=2, column=0, columnspan=2, padx=(5,0), pady=(5,0), sticky="nsew")
            self.Main_Widget["Scrollerbar"]["Vertical"].grid(row=2, column=2, padx=(0,0), pady=(5,0), sticky="ns")
            self.Main_Widget["Label"]["Message"].grid(row=3, column=0, padx=(5,0), pady=5, sticky="w")
            self.Main_Widget["Label"]["Count"].grid(row=3, column=1, padx=(5,0), pady=5, sticky="e")

            self.Frame["Main"].grid_rowconfigure(2, weight=1)  # 讓 TreeView 可以自動調整大小
            self.Frame["Main"].grid_columnconfigure(1, weight=1)

            ### Tooltips
            ToolTip = {
                "Button_Edit": Hovertip(self.Main_Widget["Button"]["Download"], text="Download devices log by ADB command.", hover_delay=300),
                "Button_Add": Hovertip(self.Main_Widget["Button"]["Reload"], text="Reload Ether connectable devices.", hover_delay=300),
            }

        def sort_by_column(col:str, reverse:bool):
            data = [(self.Main_Widget["TreeView"].set(item, col), item) for item in self.Main_Widget["TreeView"].get_children('')]
            data.sort(reverse=reverse, key=lambda t: t[0])
            for index, (val, item) in enumerate(data):
                self.Main_Widget["TreeView"].move(item, '', index)
            self.Main_Widget["TreeView"].heading(col, command=lambda: sort_by_column(col=col, reverse=not reverse))

        ### Create Frames.
        self.Frame = {}
        self.Frame["Main"] = tk.Frame(self.root, borderwidth=1, relief="flat", highlightbackground="#a9a7a7", highlightthickness=1)
        self.Frame["Main"].grid(row=0, column=0, padx=5, pady=5, sticky="nsew")  
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        create_main_widgets()

    def Show_MessageBox(self, title:str, message:str):
        messagebox.showwarning(title, message, parent=self.root)

    ###=======================================================================================
    def Updating_TreeViewCount(self, event=None):
        total_num = len(self.Main_Widget["TreeView"].get_children())
        selected_num = len(self.Main_Widget["TreeView"].selection())
        self.Main_Widget["Label"]["Count"].config(text=f"Total : {selected_num}/{total_num}")

    def Button_Refresh(self):
        def check_telnet_connection(host:str, port:int=23):
            try:
                device = TelNet(host, port) 
                return {"Device":host,
                        "Result":device.Check_Connection()[0]}
            except Exception as e:
                error_message = traceback.format_exc()
                self.Show_MessageBox("Error", error_message)
    
        def update_treeveiw(all_client_data:dict, ether_checkresult:dict):
            try:
                ### Clear the TreeView before inserting new data.
                all_rows = []
                for data in all_client_data:
                    if data["EtherIP"] in ether_checkresult["PASS"]:
                        intput_value = list(data.values())[:-1]
                        index = data["EtherIP"].split(".")[-1].zfill(3)
                        intput_value.append(index)
                        self.Main_Widget["TreeView"].insert("", tk.END, values=intput_value)
                        all_rows.append({"ClientID": data.get("ClientID", ""),
                                                    "MAC": data.get("MAC", ""),
                                                    "EtherIP": data.get("EtherIP", ""),
                                                    "Index": index})
                        
                if ether_checkresult["PASS"] == []:
                    self.Show_MessageBox("Error", "No devices found or all devices are offline.")     

                JsonDataFunction.Update_jsonFileData(self.ADBDownload_JsonPath, "Client", all_rows)

            except Exception as e:
                error_message = traceback.format_exc()
                self.Show_MessageBox("Error", error_message)

        def Thread_Function():
            try:
                ### Disable the Reload button to prevent multiple clicks.                       
                self.root.after(0, lambda: self.Main_Widget["Button"]["Reload"].config(state=tk.DISABLED))
                self.root.after(0, lambda: self.Main_Widget["Button"]["Download"].config(state=tk.DISABLED))    
                self.root.after(0, lambda: self.Main_Widget["Label"]["Message"].config(text=f"Checking Clients Connection ...", style="Message2_ADB.TLabel"))      

                ### Execute Thread Pool.
                ### Check the connection status of each device in [client_jsondata["Client"]].
                client_jsondata = JsonDataFunction.Get_jsonAllData(self.Client_JsonPath)
                with ThreadPoolExecutor(max_workers=64, thread_name_prefix="Check_ClientEtherConnection") as executor:
                    futures = []
                    for client_data in client_jsondata["Client"]:
                        if self.Thread_StopEvent.is_set():  break
                        futures.append(executor.submit(check_telnet_connection, client_data["EtherIP"], 23))
                
                    ### Get all result from [futures].
                    total_count = len(futures)
                    completed_count = 0
                    ether_checkresult = {"PASS":[],"FAIL":[]}
                    for future in as_completed(futures):
                        if self.Thread_StopEvent.is_set():  break
                        thread_respone = future.result()
                        ether_checkresult[thread_respone["Result"]].append(thread_respone["Device"])
                        # ether_checkresult["PASS"].append(thread_respone["Device"])

                        completed_count += 1
                        self.root.after(0, lambda completed_count=completed_count, total_count=total_count: 
                                        self.Main_Widget["Label"]["Message"].config(text=f"Processing  {completed_count} / {total_count}  ...", style="Message2_ADB.TLabel"))

                ### Show the connection status in self.Main_Widget["TreeView"].
                if self.Thread_StopEvent.is_set():  return
                self.root.after(0, lambda: update_treeveiw(client_jsondata["Client"], ether_checkresult))
                self.root.after(0, lambda: self.Updating_TreeViewCount())
                self.root.after(0, lambda: self.Search_VarFilter())
                
            except Exception as e:
                error_message = traceback.format_exc()
                self.root.after(0, lambda: self.Show_MessageBox("Error", error_message))

            finally:
                self.root.after(0, lambda: self.Main_Widget["Button"]["Reload"].config(state=tk.NORMAL))
                self.root.after(0, lambda: self.Main_Widget["Button"]["Download"].config(state=tk.NORMAL))
                self.root.after(0, lambda: self.Main_Widget["Label"]["Message"].config(text=f"{self.Client_JsonPath}", style="Message1_ADB.TLabel"))
        
        #===========================================================================================
        try:
            ### Clear the TreeView before inserting new data.
            for item in self.Main_Widget["TreeView"].get_children():
                self.Main_Widget["TreeView"].delete(item)

            self.Thread_StopEvent.clear()
            thread = threading.Thread(target=Thread_Function, daemon=True)
            thread.start()

        except Exception as e:
            error_message = traceback.format_exc()
            self.Show_MessageBox("Error", error_message)
            return

    def Button_DownloadLog(self):
        adb_download_frame = tk.Toplevel(self.root)
        # adb_download_frame.transient(self.root)
        app = Page_ADBDownloadLog(root=adb_download_frame)

    def Search_VarFilter(self, *args):
        ### Delete all rows in TreeView.
        ### filter_data = [] for storing filtered results.
        ### Get the search keyword from [self.Main_Widget["Entry"]["Search"]].
        self.Main_Widget["TreeView"].delete(*self.Main_Widget["TreeView"].get_children())
        filter_data = []
        key_word = self.search_var.get().strip().lower()
        all_rows = JsonDataFunction.Get_jsonAllData(self.ADBDownload_JsonPath)["Client"]

        ### If [key_word] is empty.
        ### Insert [all_rows] into TreeView.
        if not key_word:
            for data in all_rows:
                self.Main_Widget["TreeView"].insert("", tk.END, values=list(data.values()))
            return
        
        ### Filter [all_rows] based on the [key_word].
        ### Store the filtered results in [filter_data].
        for data in all_rows:
            text = f"{data.get('ClientID') or ''} {data.get('MAC')} {data.get('EtherIP') or ''} {data.get('Index') or ''}".lower()
            if key_word in text:
                filter_data.append(data)
        
        ### Insert [filter_data] into TreeView.
        for data in filter_data:
            self.Main_Widget["TreeView"].insert("", tk.END, values=list(data.values()))

        self.Updating_TreeViewCount()

    ###=======================================================================================
    def ReloadJsonData(self):
        self.load_json_data()
        self.Main_Widget["Label"]["Message"].config(text=f"{self.Client_JsonPath}", style="Message1_ADB.TLabel")

    def on_close(self):
        if hasattr(self, 'Thread_StopEvent'):
            self.Thread_StopEvent.set()

if __name__ == "__main__":
    width = 800
    height = 700

    root = tk.Tk()
    root.title("ADB")
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.resizable(True, True)
    app = Frame_ADB(root)     
    root.mainloop()


