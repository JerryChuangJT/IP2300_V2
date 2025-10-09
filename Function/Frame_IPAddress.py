import tkinter as tk
from tkinter import ttk, messagebox
import traceback
import threading
import os
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import Function.MyFunction_JsonData as JsonDataFunction
from Function.MyFunction_Telnet import TelNet

from Class.Class_Button import Button
from Class.Class_Tooltip import SmartTooltip

class Frame_IPAddress:
    def __init__(self, root, close_callback=None):
        self.root = root
        self.close_callback = close_callback
        style = ttk.Style()
        style.configure("Title_IPAddress.TLabel", font=("Segoe UI", 13, "bold"), foreground="blue")
        style.configure("Count_IPAddress.TLabel", font=("Segoe UI", 9), foreground="#717171")
        style.configure("Message1_IPAddress.TLabel", font=("Segoe UI", 8), foreground="#717171")
        style.configure("Message2_IPAddress.TLabel", font=("Segoe UI", 8), foreground="Red")


        self.Client_IPAddress_Data = {}

        self.load_json_data()
        self.Create_Widget()

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)
        
        self.SelectedSituation_JsonPath = "./temp/json_SelectedSituaion.json"
        self.Client_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Client.json"

        self.TreeView_Column = ["ClinetID", "MAC", "EtherIP", "WifiIPv4", "WifiIPv6"]

    def Create_Widget(self):
        def sort_by_column(col:str, reverse:bool):
            data = [(self.Main_Widget["TreeView"].set(item, col), item) for item in self.Main_Widget["TreeView"].get_children('')]
            data.sort(reverse=reverse, key=lambda t: t[0])
            for index, (val, item) in enumerate(data):
                self.Main_Widget["TreeView"].move(item, '', index)
            self.Main_Widget["TreeView"].heading(col, command=lambda: sort_by_column(col=col, reverse=not reverse))

        ### Create Frames.
        self.Frame = {}
        self.Frame["Main"] = ttk.Frame(self.root, borderwidth=1, relief="flat")
        self.Frame["Main"].grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        ### Create Widgets.
        self.Main_Widget = {}
        self.Main_Widget["Button"] = {}
        self.Main_Widget["Label"] = {}
        self.Main_Widget["Entry"] = {}
        self.Main_Widget["Scrollerbar"] = {}

        self.Main_Widget["Title"] = ttk.Label(self.Frame["Main"], text="IPAddress", style="Title_IPAddress.TLabel")
        self.Main_Widget["Button"]["Refresh"] = Button(self.Frame["Main"], text="Refresh", command=self.Button_Refresh)
        self.Main_Widget["TreeView"] = ttk.Treeview(self.Frame["Main"], columns=self.TreeView_Column, show="headings", selectmode="extended")
        self.Main_Widget["Scrollerbar"]["Vertical"] = ttk.Scrollbar(self.Frame["Main"], orient=tk.VERTICAL, command=self.Main_Widget["TreeView"].yview)
        self.Main_Widget["TreeView"].configure(yscrollcommand=self.Main_Widget["Scrollerbar"]["Vertical"].set)
        for i in range(len(self.TreeView_Column)):
            self.Main_Widget["TreeView"].heading(self.TreeView_Column[i], 
                                                    text=self.TreeView_Column[i], 
                                                    anchor="w", 
                                                    command=lambda col=self.TreeView_Column[i]: sort_by_column(col=col, reverse=False))
            self.Main_Widget["TreeView"].column(self.TreeView_Column[i], width=50, stretch=True)
        self.Main_Widget["Label"]["Message"] = ttk.Label(self.Frame["Main"], text="Ready", style="Message1_IPAddress.TLabel")
        self.Main_Widget["Label"]["Count"] = ttk.Label(self.Frame["Main"], text="Total : 0", style="Count_IPAddress.TLabel")
        self.Main_Widget["TreeView"].tag_configure("red", foreground="red")
        self.Main_Widget["TreeView"].tag_configure("black", foreground="black")

        ### Place Widgets.
        self.Main_Widget["Title"].grid(row=0, column=0, padx=5, pady=(5,0), sticky="w")
        self.Main_Widget["Button"]["Refresh"].grid(row=0, column=0, padx=5, pady=(5,0), sticky="se")
        self.Main_Widget["TreeView"].grid(row=1, column=0, padx=(5,0), pady=5, sticky="nsew")
        self.Main_Widget["Scrollerbar"]["Vertical"].grid(row=1, column=1, padx=0, pady=5, sticky="ns")
        self.Main_Widget["Label"]["Message"].grid(row=2, column=0, padx=5, pady=0, sticky="w")
        self.Main_Widget["Label"]["Count"].grid(row=2, column=0, padx=5, pady=0, sticky="e")
        self.Frame["Main"].grid_rowconfigure(1, weight=1)
        self.Frame["Main"].grid_columnconfigure(0, weight=1)

        self.Main_Widget["Tooltip"] = {
            "Button_Refresh": SmartTooltip(self.Main_Widget["Button"]["Refresh"], text="Refresh IPAddress of selected clients.", hover_delay=300),
        }

    def Button_Refresh(self):
        def get_client_etherip(client_id:str):
            for client_data in self.Client_JsonData["Client"]:
                if client_data["ClientID"] == client_id:
                        return client_data["EtherIP"]
            return None
        
        def get_client_mac(client_id:str):
            for client_data in self.Client_JsonData["Client"]:
                if client_data["ClientID"] == client_id:
                        return client_data["MAC"]
            return None
        
        def get_wifi_ip(client_id:str, port:int=23):
            data = {
                "ClientID": client_id,
                "MAC": get_client_mac(client_id),
                "EtherIP": get_client_etherip(client_id),
                "WifiIPv4": "Ether Error",
                "WifiIPv6": "Ether Error"
            }

            Telnet_Device = TelNet(host=data["EtherIP"], port=port)
            Telnet_Device.Connect_Devcie()
            time.sleep(1)

            ### Get Wifi_IP_result.log.
            get_wifiip_command = "cat /storage/emulated/0/Documents/Log/Wifi/Wifi_IP_result.log"
            wifi_ip_log = Telnet_Device.Execute_Command(get_wifiip_command)
            
            ### result_log[0] == "FAIL", means ether connetion Fail. 
            ### Wifi_IP_result.log the result => Pass / Fail
            if wifi_ip_log[0] == "PASS":
                result_search = re.search(r"Result\s*:\s*(\w+)", wifi_ip_log[1])
                result = result_search.group(1) if result_search else "Log Error"

                if result.lower() == "pass":
                    ipv4_search = re.search(r"IPv4\s*:\s*([\d\.]+)", wifi_ip_log[1])
                    ipv6_search = re.search(r"IPv6\s*:\s*([\w:]+)", wifi_ip_log[1])
                    ipv4 = ipv4_search.group(1)
                    ipv6 = ipv6_search.group(1)
                    data["WifiIPv4"] = ipv4
                    data["WifiIPv6"] = ipv6

                elif result.lower() == "fail":
                    data["WifiIPv4"] = "None"
                    data["WifiIPv6"] = "None"
                else:
                    data["WifiIPv4"] = "Log Error"
                    data["WifiIPv6"] = "Log Error"

            Telnet_Device.Disconnect_Device()
            self.Client_IPAddress_Data[client_id] = data
        
        ### Update TreeView with self.Client_IPAddress_Data.
        def update_treeview():
            exist_ipv4 = set()
            exist_ipv6 = set()
            for client_id, data in self.Client_IPAddress_Data.items():
                ipv4 = data["WifiIPv4"]
                ipv6 = data["WifiIPv6"]
                
                text_color = "black"
                if ipv4 in exist_ipv4 or \
                    ipv6 in exist_ipv6 or \
                    ipv4 == "None" or \
                    ipv6 == "None" or \
                    ipv4 == "Log Error" or \
                    ipv6 == "Log Error" or \
                    ipv4 == "Ether Error" or \
                    ipv6 == "Ether Error":
                    text_color = "red"

                exist_ipv4.add(ipv4)
                exist_ipv6.add(ipv6)

                self.AddTreeViewItem(list(data.values()), text_color)

        def Thread_Function():
            try:
                ### Disable the Refresh button during processing.
                self.Show_Message(text=f"Getting IPAddress...", color="red")
                self.Main_Widget["Button"]["Refresh"].config(state=tk.DISABLED)
                self.Client_IPAddress_Data = {}

                ### Get Selected CliendIDs from SelectedSituation_JsonPath.
                self.Client_JsonData = JsonDataFunction.Get_jsonAllData(self.Client_JsonPath)
                client_ids = JsonDataFunction.Get_jsonAllData(self.SelectedSituation_JsonPath)["ClientID"]

                ### Use ThreadPoolExecutor to process multiple clients concurrently.
                with ThreadPoolExecutor(max_workers=64, thread_name_prefix="Check_GetIPAddress") as executor:
                    futures = []
                    for client_id in client_ids:
                        futures.append(executor.submit(get_wifi_ip, client_id, 23))

                    total_futures = len(futures)
                    count = 0
                    for future in as_completed(futures):
                        count += 1
                        self.Show_Message(text=f"Processing {count} / {total_futures}", color="red")

                ### Update TreeView with self.Client_IPAddress_Data.
                update_treeview()

            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showerror("Error", f"An error occurred:\n{error_message}", parent=self.root)
                return

            finally:
                self.Show_Message(text="Ready", color="gray")
                self.Main_Widget["Label"]["Count"].config(text=f"Total : {len(self.Client_IPAddress_Data)}")
                self.Main_Widget["Button"]["Refresh"].config(state=tk.NORMAL)

        try:
            ### Clear the TreeView before inserting new data.
            for item in self.Main_Widget["TreeView"].get_children():
                self.Main_Widget["TreeView"].delete(item)
            
            if os.path.exists(self.SelectedSituation_JsonPath) is False:
                messagebox.showwarning("Warning", f"Run the Test before Refreshing the IPAddress.", parent=self.root)
                return
            
            thread = threading.Thread(target=Thread_Function, daemon=True)
            thread.start()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}")

    def AddTreeViewItem(self, values:list=None, tag_color:str="black"):
        new_item = self.Main_Widget["TreeView"].insert("", tk.END, values=values)
        self.Main_Widget["TreeView"].see(new_item)
        self.Main_Widget["TreeView"].item(new_item, tags=(tag_color, ))

    def Show_Message(self, text:str="", color:str="gray"):
        if color.lower() == "red":
            style = "Message2_IPAddress.TLabel"
        elif color.lower() == "gray":
            style = "Message1_IPAddress.TLabel"

        self.root.after(0, lambda: self.Main_Widget["Label"]["Message"].config(text=text, style=style))

    ### ===================================================================================================
    def ReloadJsonData(self):
        self.load_json_data()


if __name__ == "__main__":
    width = 800
    height = 700

    root = tk.Tk()
    root.title("IPAddress")
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.resizable(True, True)
    app = Frame_IPAddress(root)     
    root.mainloop()