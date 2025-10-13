import tkinter as tk
from tkinter import ttk, messagebox
from idlelib.tooltip import Hovertip  
import traceback
import time
import os
import json
import re

from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from Function.MyFunction_Telnet import TelNet
from Class.Class_ImageStatus import ImageDisplay

import Function.MyFunction_JsonData as JsonDataFunction
import Function.MyFunction as MyFunction
import Function.MyFunction_WriteLog as WriteLogFunction

from Class.Class_Button import Button

"""
Create two members:
    self.ShellScript_Status & self.Img_Element

1. self.ShellScript_Status: dict
    "ClientID": client_id,
    "EtherIP": client_ip,
    "Wifi": {
        wifi_id: "not_schedule" (normal/error/not_schedule),
    },
    "Script": {
        script_id_1: "not_schedule" (normal/error/not_schedule),
        script_id_2: "not_schedule" (normal/error/not_schedule),
        script_id_3: "not_schedule" (normal/error/not_schedule),
        ...
    }
2. self.Img_Element: dict
    "Wifi": {
        wifi_id: ImageDisplay object,
    },
    "Script": {
        script_id_1: ImageDisplay object,
        script_id_2: ImageDisplay object,
        script_id_3: ImageDisplay object,
        ...
    }
"""
class Frame_ClientStatus():
    def __init__(self, root, client_id:str=None, callback=None):
        self.callback = callback
        self.root = root
        self.client_id = client_id
        
        style = ttk.Style()
        style.configure('ImageLabel_ClientStatus.TLabel', font=("Segoe UI", 6), foreground="black")

        self.Img_Element = {
            "Wifi": {},
            "Script": {}
        }

        self.load_json_data()
        self.Create_Attribution()
        self.Create_Widgets()

    def load_json_data(self):
        self.RunTest_JasonPath = "./temp/json_RunTest.json"
        self.RuTest_JasonData_Client = JsonDataFunction.Get_jsonAllData(self.RunTest_JasonPath)[self.client_id]

    ### Create self.ShellScript_Status dict.
    def Create_Attribution(self):
        ### Get Client ip.
        client_id = self.client_id
        client_ip = self.RuTest_JasonData_Client["EtherIP"]

        ### Get Wifi status dictionary.
        wifi_status = {self.RuTest_JasonData_Client["Wifi"]["WifiID"]: "not_schedule"}

        ### Get Scripts status dictionary.
        script_ids = sorted(list(self.RuTest_JasonData_Client["Script"].keys()))
        script_status = { script_id: "not_schedule" for script_id in script_ids }
 
        ### Create Attribution dictionary.
        self.ShellScript_Status = {
            "ClientID": client_id,
            "EtherIP": client_ip,
            "Wifi": wifi_status,
            "Script": script_status
        }

    ### Create self.Img_Element dict.
    def Create_Widgets(self):
        self.HoverTip = {}

        ### Create Wifi Img.
        wifi_id = list(self.ShellScript_Status["Wifi"].keys())[0]
        wifi_img = ImageDisplay(self.root, image_path="./img/wifi.png", size=(40, 40))
        wifi_img.grid(row=0, column=0, rowspan=2, padx=10, pady=(5,0))
        tooltip_text = (f"Client ID: {self.ShellScript_Status['ClientID']}\n"
                        f"Ether IP: {self.ShellScript_Status['EtherIP']}\n"
                        f"WiFi ID: {wifi_id}\n"
                        f"Status: {self.ShellScript_Status['Wifi'][wifi_id]}")
        self.HoverTip[wifi_id] = Hovertip(wifi_img, tooltip_text, hover_delay=300)
        
        self.Img_Element["Wifi"][wifi_id] = wifi_img

        ### Create Scripts Img.
        for i, script_id in enumerate(self.ShellScript_Status["Script"]):
            script_type = self.RuTest_JasonData_Client["Script"][script_id]["Type"]

            if script_type == "Ping":
                img_path = "./img/ping.png"
            elif script_type == "Youtube":
                img_path = "./img/youtube.png"

            script_img = ImageDisplay(self.root, image_path=img_path, size=(30, 30))
            script_label = ttk.Label(self.root, text=script_id, style='ImageLabel_ClientStatus.TLabel')
            script_img.grid(row=(i//4)*2, column=i%4+1, padx=2, pady=(5,0))
            script_label.grid(row=(i//4)*2+1, column=i%4+1, padx=2, pady=(0,5))

            tooltip_text = (f"Type: {script_type}\n"
                            f"Script ID: {script_id}\n"
                            f"Status: {self.ShellScript_Status['Script'][script_id]}")
            self.HoverTip[script_id] = Hovertip(script_img, tooltip_text, hover_delay=300)
            self.Img_Element["Script"][script_id] = script_img

    ###===================================================================
    def Update_ShellScripte_Status(self, type:str, id:str, status:str):
        try:
            if type == "Wifi":
                self.ShellScript_Status["Wifi"][id] = status
                tooltip_text = (f"Client ID: {self.ShellScript_Status['ClientID']}\n"
                                f"Ether IP: {self.ShellScript_Status['EtherIP']}\n"
                                f"WiFi ID: {id}\n"
                                f"Status: {self.ShellScript_Status['Wifi'][id]}")
                Hovertip(self.Img_Element["Wifi"][id], tooltip_text, hover_delay=300)

            elif type == "Script":
                self.ShellScript_Status["Script"][id] = status
                tooltip_text = (f"Type: {type}\n"
                                f"Script ID: {id}\n"
                                f"Status: {self.ShellScript_Status['Script'][id]}")
                Hovertip(self.Img_Element["Script"][id], tooltip_text, hover_delay=300)

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
    
    def Update_AllImgStatus(self):
        def Update_Tooltip():
            try:
                ### Update Wifi Tooltip.
                wifi_id = list(self.ShellScript_Status["Wifi"].keys())[0]
                tooltip_text = (f"Client ID: {self.ShellScript_Status['ClientID']}\n"
                                f"Ether IP: {self.ShellScript_Status['EtherIP']}\n"
                                f"WiFi ID: {wifi_id}\n"
                                f"Status: {self.ShellScript_Status['Wifi'][wifi_id]}")
                self.HoverTip[wifi_id].text = tooltip_text

                ### Update Script Tooltip.
                for script_id in self.ShellScript_Status["Script"]:
                    script_type = self.RuTest_JasonData_Client["Script"][script_id]["Type"]
                    tooltip_text = (f"Type: {script_type}\n"
                                    f"Script ID: {script_id}\n"
                                    f"Status: {self.ShellScript_Status['Script'][script_id]}")
                    self.HoverTip[script_id].text = tooltip_text

            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showwarning("Error", error_message, parent=self.root)

        try:
            ### Update Wifi Img Status.
            wifi_id = list(self.ShellScript_Status["Wifi"].keys())[0]
            wifi_status = self.ShellScript_Status["Wifi"][wifi_id]

            if wifi_status == "normal":
                self.Img_Element["Wifi"][wifi_id].set_enabled("normal")
            elif wifi_status == "error":
                self.Img_Element["Wifi"][wifi_id].set_enabled("disabled")
            elif wifi_status == "not_schedule":
                self.Img_Element["Wifi"][wifi_id].set_enabled("not_schedule")

            ### Update Script Img Status.
            for script_id in self.ShellScript_Status["Script"]:
                script_status = self.ShellScript_Status["Script"][script_id]
                if script_status == "normal":
                    self.Img_Element["Script"][script_id].set_enabled("normal")
                elif script_status == "error":
                    self.Img_Element["Script"][script_id].set_enabled("disabled")
                elif script_status == "not_schedule":
                    self.Img_Element["Script"][script_id].set_enabled("not_schedule")

            Update_Tooltip()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)

class Frame_Monitor():
    def __init__(self, root, stoptest_callback=None):
        self.stoptest_callback = stoptest_callback
        self.root = root

        style = ttk.Style()
        style.configure('FrameSituation_Monitor.TLabelframe.Label', font=("Segoe UI", 12, "bold"), foreground="blue")
        style.configure('FrameClientNormal_Monitor.TLabelframe.Label', font=("Segoe UI", 10, "bold"), foreground="black")
        style.configure('FrameClientError_Monitor.TLabelframe.Label', font=("Segoe UI", 10, "bold"), foreground="red")
        style.configure("Information_Monitor.TLabel", font=("Segoe UI", 8), foreground="black")

        style.configure("Message1_Monitor.TLabel", font=("Segoe UI", 8), foreground="#717171")
        style.configure("Message2_Monitor.TLabel", font=("Segoe UI", 8), foreground="Red")

        self.Create_Widgets()
        self.LogPath = "./Controller_Log/Monitor"

        self.Flag = {}
        self.Flag["RunTest"] = False

        self.load_json_data()

    def load_json_data(self):
        ### Environment Json Data.
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)

        ### Schedule Json Data.
        self.Schedule_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Schedule.json"
        self.Schedule_JsonData = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)

        ### Client Json Data.
        self.Client_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Client.json"
        self.Client_JsonData = JsonDataFunction.Get_jsonAllData(self.Client_JsonPath)

        ### Script Json Data.
        self.Script_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Script.json"
        self.Script_JsonData = JsonDataFunction.Get_jsonAllData(self.Script_JsonPath)
        
        ### Wifi Json Data.
        self.Wifi_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Wifi.json"
        self.Wifi_JsonData = JsonDataFunction.Get_jsonAllData(self.Wifi_JsonPath)

        ### SelectedSetuation & RunTest Json Path.
        self.SelectedSituation_JsonPath = "./temp/json_SelectedSituaion.json"
        self.RunTest_JsonPath = "./temp/json_RunTest.json"

    def Create_Widgets(self):
        ### Create Frames ###
        self.Frame = {}
        self.Frame["Information"] = tk.Frame(self.root, borderwidth=1, relief="flat", highlightbackground="#cccccc", highlightcolor="#cccccc", highlightthickness=1)
        # self.Frame["Information"] = tk.Frame(self.root)
        self.Frame["Status"] = ttk.Frame(self.root, padding="5")
        self.Frame["Information"].grid(row=0, column=0, sticky="nsew", padx=5, pady=(5,0))
        self.Frame["Status"].grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        ### Create Information Widgets in self.Frame["Information"] ###
        self.Information_Widget = {}
        self.Information_Widget["Label"] = {}
        self.Information_Widget["Button"] = {}
        self.Information_Widget["Tooltip"] = {}

        self.Information_Widget["Label"]["Ether"] = ttk.Label(self.Frame["Information"], text="Ether : 0 \nNormal : 0 \nError : 0", style="Information_Monitor.TLabel")
        self.Information_Widget["Label"]["Wifi"] = ttk.Label(self.Frame["Information"], text="WiFi : 0 \nNormal : 0 \nError : 0 \nWait : 0", style="Information_Monitor.TLabel")
        self.Information_Widget["Label"]["Ping"] = ttk.Label(self.Frame["Information"], text="Ping : 0 \nNormal : 0 \nError : 0 \nWait : 0", style="Information_Monitor.TLabel")
        self.Information_Widget["Label"]["Youtube"] = ttk.Label(self.Frame["Information"], text="Youtube : 0 \nNormal : 0 \nError : 0 \nWait : 0", style="Information_Monitor.TLabel")
        self.Information_Widget["Button"]["Stop"] = Button(self.Frame["Information"], image_path="./img/stop_test.png", size=(45,45), command=self.Button_StopMonitor)

        self.Information_Widget["Label"]["Ether"].grid(row=0, column=0, padx=(5,0), pady=2, sticky="w")
        self.Information_Widget["Label"]["Wifi"].grid(row=0, column=1, padx=(5,0), pady=2, sticky="w")
        self.Information_Widget["Label"]["Ping"].grid(row=0, column=2, padx=(10,0), pady=2, sticky="w")
        self.Information_Widget["Label"]["Youtube"].grid(row=0, column=3, padx=(10,0), pady=2, sticky="w")
        self.Information_Widget["Button"]["Stop"].grid(row=0, column=4, rowspan=2, padx=(0,0), pady=5, sticky="e")
        self.Frame["Information"].grid_columnconfigure(4, weight=1)

        self.Information_Widget["Tooltip"] = {
            "Button_Stop": Hovertip(self.Information_Widget["Button"]["Stop"], "Stop Monitoring.", hover_delay=300)
        }

        ### Create Status Widgets in self.Frame["Status"] ###
        self.Status_Widget = {}
        self.Status_Widget["Scrollbar"] = {}
        self.Status_Widget["Label"] = {}

        self.Status_Widget["Canvas"] = tk.Canvas(self.Frame["Status"], relief="flat", highlightthickness=1, highlightbackground="#cccccc")
        self.Status_Widget["Scrollbar"]["Vertical"] = ttk.Scrollbar(self.Frame["Status"], orient="vertical", command=self.Status_Widget["Canvas"].yview)
        self.Status_Widget["Scrollbar"]["Horizontal"] = ttk.Scrollbar(self.Frame["Status"], orient="horizontal", command=self.Status_Widget["Canvas"].xview)
        self.Status_Widget["Canvas"].configure(yscrollcommand=self.Status_Widget["Scrollbar"]["Vertical"].set)
        self.Status_Widget["Canvas"].configure(xscrollcommand=self.Status_Widget["Scrollbar"]["Horizontal"].set)
        self.Status_Widget["Label"]["Message"] = ttk.Label(self.Frame["Status"], text="Ready", style="Message1_Situation.TLabel")

        self.Status_Widget["Canvas"].grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.Status_Widget["Scrollbar"]["Vertical"].grid(row=1, column=1, padx=0, pady=0, sticky="ns")
        self.Status_Widget["Scrollbar"]["Horizontal"].grid(row=2, column=0, padx=0, pady=0, sticky="ew")
        self.Status_Widget["Label"]["Message"].grid(row=3, column=0, padx=0, pady=0, sticky="sw")

        self.Frame["Status"].grid_rowconfigure(1, weight=1)
        self.Frame["Status"].grid_columnconfigure(0, weight=1)

        #### Create a frame inside the canvas
        self.Status_Widget["Frame"] = ttk.Frame(self.Status_Widget["Canvas"])
        self.Status_Widget["Canvas"].bind("<Configure>",lambda e: self.Status_Widget["Canvas"].configure(scrollregion=self.Status_Widget["Canvas"].bbox("all")))
        self.Status_Widget["Canvas"].create_window((0,0), window=self.Status_Widget["Frame"], anchor="nw")

    def Button_StopMonitor(self):
        if self.Flag["RunTest"] == False:
            # messagebox.showinfo("Info", "No test is running.", parent=self.root)
            return
        else:
            WriteLogFunction.WriteLog(self.LogPath, "[Stop Test]")
            self.Show_Message("Stopping test, wait for it ...", "red")
            self.Flag["RunTest"] = False

    ###===================================================================
    ### Before Creating Client Status Frames, Reload self.RunTest_JsonData, for making sure the data is the latest.
    ### Update json_RunTest.json file.
    ### json_RunTest.json is for recording the test parameters of each client.
    def Update_RunTest_Json(self):
        def clean_jsondata(json_path:str):
            jsondata = JsonDataFunction.Get_jsonAllData(json_path)
            keys = JsonDataFunction.Get_DictKey(jsondata)
            for key in keys:
                JsonDataFunction.Remove_jsonFileKey(json_path, key)
        
        def get_client_ip(client_id:str)->str:
            for client in self.Client_JsonData["Client"]:
                if client["ClientID"] == client_id:
                    return client["EtherIP"]
            return ""
        
        def get_wifi_parameters(wifi_id:str, schedule)->dict:
            for wifi_data in self.Wifi_JsonData["Wifi"]:
                if wifi_data["WifiID"] == wifi_id:
                    data = {
                            "WifiID": wifi_data["WifiID"],
                            "PingType": wifi_data["PingType"],
                            "DUTIP": wifi_data["DUTIP"],
                            "SSID": wifi_data["SSID"],
                            "Security": wifi_data["Security"],
                            "Password": wifi_data["Password"],
                            "BSSID": wifi_data["BSSID"],
                            "Driver_Band": wifi_data["Driver_Band"],
                            "Driver_Standard": wifi_data["Driver_Standard"],
                            "Driver_Channel": wifi_data["Driver_Channel"],
                            "Driver_Bandwidth": wifi_data["Driver_Bandwidth"],
                            "Schedule": schedule
                        }
                    return data
            return {}
        
        def get_script_parameters(script_datas:list)->dict:
            def get_paraameter(script_id:str, schedule)->dict:
                for script_data in self.Script_JsonData["Script"]:
                    if script_data["ScriptID"] == script_id:
                       return {
                            "Type": script_data["Type"],
                            "Parameter1": script_data["Parameter1"],
                            "Parameter2": script_data["Parameter2"],
                            "Parameter3": script_data["Parameter3"],
                            "Parameter4": script_data["Parameter4"],
                            "Parameter5": script_data["Parameter5"],
                            "Parameter6": script_data["Parameter6"],
                            "Schedule": schedule
                        }
                return {}

            data = {}
            for script_data in script_datas:
                script_id = script_data["ScriptID"]
                script_schedule = script_data["Schedule"]
                data[script_id] = get_paraameter(script_id, script_schedule)
            return data
        
        try:
            ### Update Json Data.
            self.load_json_data()

            ### Create json_RunTest.json.
            ### Clean all data in json_RunTest.json.
            JsonDataFunction.Create_JsonFile(self.RunTest_JsonPath)
            clean_jsondata(self.RunTest_JsonPath)

            ### Read Selected Situation Json File.
            situations = JsonDataFunction.Get_jsonAllData(self.SelectedSituation_JsonPath)["Situation"]
            for situation in situations:
                wifi_id = self.Schedule_JsonData[situation]["Wifi"]["WifiID"]
                wifi_schedule = self.Schedule_JsonData[situation]["Wifi"]["Schedule"]
                script_datas = self.Schedule_JsonData[situation]["Script"]

                for client_id in self.Schedule_JsonData[situation]["ClientID"]:
                    data = {
                        "EtherIP": get_client_ip(client_id),
                        "Situation": situation,
                        "Wifi": get_wifi_parameters(wifi_id, wifi_schedule),
                        "Script": get_script_parameters(script_datas)
                    }
                    JsonDataFunction.Update_jsonFileData(self.RunTest_JsonPath, client_id, data)

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)

    """
    self.Frame_Situation: dict
        "Situation1": Frame object,

    self.Frame_ClientID: dict
        "ClientID1": Frame object,

    self.Client_Ether_Status: dict
        "ClientID1": "normal"/"error",

    self.Client_ShellScript_Status: dict
        "ClientID1": Frame_ClientStatus object,
    """
    ### Create Client Status Frames.
    def LoadCreate_ClientStatusFrame(self):
        self.Frame_Situation = {}
        self.Frame_ClientID = {}
        self.Client_Ether_Status = {}
        self.Client_ShellScript_Status = {}

        ### Create Situation Frames.
        ### Update:
        ### self.Frame_Situation
        for situation in JsonDataFunction.Get_jsonAllData(self.SelectedSituation_JsonPath)["Situation"]:
            frame = ttk.LabelFrame(self.Status_Widget["Frame"], text=f"{situation}", padding="5", style='FrameSituation_Monitor.TLabelframe')
            frame.pack(fill="x", padx=5, pady=5)

            self.Frame_Situation[situation] = frame

        ### Create Client Status Frames.
        ### Update:
        ### self.Frame_ClientID 
        ### self.Client_Ether_Status 
        ### self.Client_ShellScript_Status
        RunTest_JsonData = JsonDataFunction.Get_jsonAllData(self.RunTest_JsonPath)
        grid_count = {}
        for k, client_id in enumerate(RunTest_JsonData):
            ### Get Situation for checking if need to change to set grid_count = 0.
            situation = RunTest_JsonData[client_id]["Situation"]
            if situation not in list(grid_count.keys()):
                grid_count[situation] = 0
            else:
                grid_count[situation] += 1
            
            ### Create Client Status Frame.
            frame =  ttk.LabelFrame(self.Frame_Situation[situation], text=f"{client_id}", padding="5", style='FrameClientNormal_Monitor.TLabelframe')
            frame.grid(row=grid_count[situation]//5, column=grid_count[situation]%5, padx=3, pady=5)
            frame_img_status = Frame_ClientStatus(root=frame, client_id=client_id)

            self.Frame_ClientID[client_id] = frame
            self.Client_Ether_Status[client_id] = "error"
            self.Client_ShellScript_Status[client_id] = frame_img_status

        ### Update All Client Img Status.
        for client_id in self.Client_ShellScript_Status:
            self.Client_ShellScript_Status[client_id].Update_AllImgStatus()
    
    def Show_Message(self, text:str="", color:str="gray"):
        if color.lower() == "red":
            style = "Message2_Situation.TLabel"
        elif color.lower() == "gray":
            style = "Message1_Situation.TLabel"

        self.root.after(0, lambda: self.Status_Widget["Label"]["Message"].config(text=text, style=style))

    ###===================================================================
    ### 這邊執行loop function，重複檢查各device狀態，以及更新LabelFrame和client img status.
    ### Step1: Check each client ether status, and update self.Client_Ether_Status.
    ### Step2: Update each client LabelFrame style according to self.Client_Ether_Status.
    ### Step3: Upload all shell scripts into Devices.
    ### Stpe4: Execute all shell scripts in Devices.
    ### Step5: Get each client shell script status, and record in [Frame_ClientStatus.ShellScript_Status].
    ### Step6: Update each client img status. Execute [Frame_ClientStatus.Update_AllImgStatus()].
    ### Step7: Update the Counting of each scripts status number.
    def MainLoop_RunTest(self):
        ### self.Flag["RunTest"] = True before start loop.
        self.Flag["RunTest"] = True
        while True:
            try:
                ### Get json_RuntTest.json data.
                WriteLogFunction.WriteLog(self.LogPath, "[Start Test] Loading json_RunTest.json.")
                self.RunTest_JsonData = JsonDataFunction.Get_jsonAllData(self.RunTest_JsonPath)

                ### Step1: Check each client ether status, and update self.Client_Ether_Status.
                if self.Flag["RunTest"] == False:  break
                WriteLogFunction.WriteLog(self.LogPath, "Checking each client ether connection status...")
                self.Show_Message("Checking each client ether connection status...", "gray")
                self.ThreadPool_Check_EtherConnection()
                WriteLogFunction.WriteLog(self.LogPath, f"  self.Client_Ether_Status: \n{str(json.dumps(self.Client_Ether_Status, indent = 4))}")

                ### Step2: Update each client LabelFrame style according to self.Client_Ether_Status.
                if self.Flag["RunTest"] == False:  break
                self.Update_ClientLabelFrame_Style()

                ### Step3: Upload all shell scripts into Devices.
                if self.Flag["RunTest"] == False:  break
                WriteLogFunction.WriteLog(self.LogPath, "Checking all shell scripts in devices...")
                self.Show_Message("Checking all shell scripts in devices...", "gray")
                self.ThreadPool_UploadShellScripts()

                ### Stpe4: Execute all shell scripts in Devices.
                if self.Flag["RunTest"] == False:  break
                WriteLogFunction.WriteLog(self.LogPath, "Executing all shell scripts in devices...")
                self.Show_Message("Executing all shell scripts in devices...", "gray")
                self.ThreadPool_ExecuteShellScripts()
                
                ### Step5: Get each client shell script status, and record in [Frame_ClientStatus.ShellScript_Status].
                if self.Flag["RunTest"] == False:  break
                WriteLogFunction.WriteLog(self.LogPath, "Getting each client shell script status...")
                self.Show_Message("Getting each client shell script status...", "gray")
                self.ThreadPool_GetShellScriptStatus()
                client_shellscript_result = {client_id: self.Client_ShellScript_Status[client_id].ShellScript_Status for client_id in self.Client_ShellScript_Status}
                WriteLogFunction.WriteLog(self.LogPath, f"  client_shellscript_result: \n{str(json.dumps(client_shellscript_result, indent = 4))}")

                ### Step6 : Update each client img status. Execute [Frame_ClientStatus.Update_AllImgStatus()].
                if self.Flag["RunTest"] == False:  break
                self.Update_ClientImgStatus()

                ### Step7 : Update the Counting of each scripts status number.
                if self.Flag["RunTest"] == False:  break
                self.Update_ScriptStatus_Counting()

                ### Wait for 3 seconds.
                if self.Flag["RunTest"] == False:  break
                self.Show_Message("Wait for 3 seconds...", "gray")
                time.sleep(3)  # 每3秒檢查一次

            except Exception as e:
                error_message = traceback.format_exc()
                result = messagebox.askyesno("Error", 
                                        f"{error_message}"
                                        "------------------------------------------------------------\n\n"
                                        "Do you want to continue the test？", 
                                        parent=self.root)
                if not result:  # 用戶選擇「否」
                    break

        self.Stop_Test()

    ### Step1 : Check each client ether status, and update self.Client_Ether_Status.
    ### Check each client ehter connection status with thread pool.
    ### Update self.Client_Ether_Status.
    def ThreadPool_Check_EtherConnection(self):
        def check_telnet_connection(client_id:str=None, client_ip:str=None, port:int=23)->bool:
            try:
                device = TelNet(client_ip, port) 
                return {"ClientID":client_id,
                        "Result":device.Check_Connection()[0]}
            
            except Exception as e:
                error_message = traceback.format_exc()
                WriteLogFunction.WriteLog(self.LogPath, f"[Error - {client_id}] {error_message}")
                return {"ClientID":client_id,
                        "Result":"FAIL"}
        try:
            with ThreadPoolExecutor(max_workers=64, thread_name_prefix="Check_ClientEtherConnection") as executor:
                ### Check all client ether connection status with thread, and add in [futures].
                futures = []
                for client_id in self.Client_Ether_Status:
                    client_ip = self.RunTest_JsonData[client_id]["EtherIP"]
                    futures.append(executor.submit(check_telnet_connection, client_id, client_ip, 23))

                ### Get all result from [futures].
                ### Update ether connection status in self.Client_Ether_Status.
                for future in as_completed(futures):
                    thread_respone = future.result()
                    if thread_respone["Result"] == "PASS":  
                        self.Client_Ether_Status[thread_respone["ClientID"]] = "normal"
                    else:   
                        self.Client_Ether_Status[thread_respone["ClientID"]] = "error"

        except Exception as e:
            error_message = traceback.format_exc()
            WriteLogFunction.WriteLog(self.LogPath, f"{error_message}")
    
    ### Step2: Update each client LabelFrame style according to self.Client_Ether_Status.
    ### Get self.Client_Ether_Status.
    ### Update self.Frame_ClientID style.
    def Update_ClientLabelFrame_Style(self):
        try:
            for client_id in self.Client_Ether_Status:
                if self.Client_Ether_Status[client_id] == "normal":
                    self.Frame_ClientID[client_id].configure(style='FrameClientNormal_Monitor.TLabelframe')
                else:   
                    self.Frame_ClientID[client_id].configure(style='FrameClientError_Monitor.TLabelframe')

        except Exception as e:
            error_message = traceback.format_exc()
            WriteLogFunction.WriteLog(self.LogPath, f"{error_message}")
    
    ### Step3: Upload all shell scripts into Devices.
    ### Upload all shell scripts into Devices.
    ### Check Wifi & Ping & Youtube shell scripts in device, if not exist, upload to device.
    def ThreadPool_UploadShellScripts(self):
        def check_remote_scriptfile(Telnet_Device, client_ip:str, local_storage:str, remote_storage:str):
            ### Get files in device.
            command = f"ls {remote_storage}"
            exist_files = Telnet_Device.Execute_Command(command)[1]

            ### Upload files to device.
            path = Path(local_storage)
            sh_files = [f.name for f in path.glob("*.sh")]
            for file in sh_files:
                if file not in exist_files:
                    local_path = f"{local_storage}{file}"
                    remote_path = f"{remote_storage}{file}"

                    ### Create remote dir.
                    command = f"adb -s {client_ip}:5555 shell mkdir -p {remote_storage}"
                    result = MyFunction.Run_Subprocess(command)

                    ### Upload file to remote.
                    command = f"adb -s {client_ip}:5555 push {local_path} {remote_path}"
                    result = MyFunction.Run_Subprocess(command)

        def upload_shellscripts(client_ip:str=None, port:int=23)->bool:  
            try:          
                ### Telnet & ADB Coneect.
                Telnet_Device = TelNet(client_ip, port) 
                Telnet_Device.Connect_Devcie()
                time.sleep(1)

                ### ADB Connect.
                adb_connect_command = f"adb connect {client_ip}"
                result = MyFunction.Run_Subprocess(adb_connect_command)
                time.sleep(1)

                ### Upload EtherConnection shell scripts to device.
                check_remote_scriptfile(Telnet_Device, client_ip, local_storage="./ShellScript/EtherConnection/", remote_storage="/storage/emulated/0/Documents/EtherConnection/")

                ### Upload Wifi shell scripts to device.
                check_remote_scriptfile(Telnet_Device, client_ip, local_storage="./ShellScript/Wifi/", remote_storage="/storage/emulated/0/Documents/Wifi/")

                ### Upload Ping shell scripts to device.
                check_remote_scriptfile(Telnet_Device, client_ip, local_storage="./ShellScript/Ping/", remote_storage="/storage/emulated/0/Documents/Ping/")

                ### Upload Youtube shell scripts to device.
                check_remote_scriptfile(Telnet_Device, client_ip, local_storage="./ShellScript/Youtube/", remote_storage="/storage/emulated/0/Documents/Youtube/")

                ### Upload KillProcess shell scripts to device.
                check_remote_scriptfile(Telnet_Device, client_ip, local_storage="./ShellScript/KillProcess/", remote_storage="/storage/emulated/0/Documents/KillProcess/")

                ### Close Connection.
                Telnet_Device.Disconnect_Device()

            except Exception as e:
                error_message = traceback.format_exc()
                WriteLogFunction.WriteLog(self.LogPath, f"[Error - {client_id}] {error_message}")

        try:
            with ThreadPoolExecutor(max_workers=64, thread_name_prefix="Upload_ClientShellScripts") as executor:
                futures = []
                for client_id in self.Client_Ether_Status:
                    if self.Client_Ether_Status[client_id] == "normal":
                        client_ip = self.RunTest_JsonData[client_id]["EtherIP"]
                        futures.append(executor.submit(upload_shellscripts, client_ip, 23))

                for future in as_completed(futures):
                    pass
        
        except:
            error_message = traceback.format_exc()
            WriteLogFunction.WriteLog(self.LogPath, f"{error_message}")

    ### Stpe4: Execute all shell scripts in Devices.
    ### Execute all shell scripts in Devices.
    def ThreadPool_ExecuteShellScripts(self):
        def ether_shellscript_command(Telnet_Device, client_id)->str:
            controller_ip = self.Environment_JsonData["ControllerPCIP"]
            ether_script_process = f"/storage/emulated/0/Documents/EtherConnection/Check_EtherConnection.sh {controller_ip}"
            search_command = f"ps -ef | grep sh"
            search_result = Telnet_Device.Execute_Command(search_command)

            if ether_script_process in search_result[1]:     
                return
            else:
                ether_command = f"sh /storage/emulated/0/Documents/EtherConnection/Check_EtherConnection.sh {controller_ip} &"
                Telnet_Device.Execute_Command(ether_command)
                time.sleep(1)

        def wifi_shellscript_command(Telnet_Device, client_id)->str:
            ### Execute Wifi Set Driver shell script.
            driver_band = self.RunTest_JsonData[client_id]["Wifi"]["Driver_Band"]
            driver_standard = self.RunTest_JsonData[client_id]["Wifi"]["Driver_Standard"]
            driver_channel = self.RunTest_JsonData[client_id]["Wifi"]["Driver_Channel"] 
            driver_bandwidth = self.RunTest_JsonData[client_id]["Wifi"]["Driver_Bandwidth"]
            
            ### Execute Wifi Coneect shell script.
            wifi_ssid = self.RunTest_JsonData[client_id]["Wifi"]["SSID"]
            wifi_auth = self.RunTest_JsonData[client_id]["Wifi"]["Security"]
            wifi_password = self.RunTest_JsonData[client_id]["Wifi"]["Password"]
            wifi_bssid = self.RunTest_JsonData[client_id]["Wifi"]["BSSID"]
            wifi_pingtype = self.RunTest_JsonData[client_id]["Wifi"]["PingType"]
            wifi_dutip = self.RunTest_JsonData[client_id]["Wifi"]["DUTIP"]
            schedule = self.RunTest_JsonData[client_id]["Wifi"]["Schedule"]

            wifi_script_process = f"/storage/emulated/0/Documents/Wifi/ScriptSchedule_Wifi.sh"
            search_command = f"ps -ef | grep sh"
            search_result = Telnet_Device.Execute_Command(search_command)
            
            if wifi_script_process in search_result[1]:     
                return
            else:
                wifi_delete_command = f"sh /storage/emulated/0/Documents/Wifi/Delete_AllWiFiProfile.sh"
                wifi_setdriver_command = f"sh /storage/emulated/0/Documents/Wifi/Script_SetDriver.sh {driver_band} {driver_standard} {driver_channel} {driver_bandwidth}"
                wifi_connect_command = f"sh /storage/emulated/0/Documents/Wifi/ScriptSchedule_Wifi.sh {wifi_ssid} {wifi_auth} {wifi_password} {wifi_bssid} {wifi_pingtype} {wifi_dutip} {schedule} &"
                
                Telnet_Device.Execute_Command(wifi_delete_command)
                time.sleep(1)
                Telnet_Device.Execute_Command(wifi_setdriver_command)
                time.sleep(10)
                Telnet_Device.Execute_Command(wifi_connect_command)
        
        def ping_shellscript_command(Telnet_Device, client_id, script_id)->str:
            ping_name = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter1"]
            ping_type = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter2"]
            ping_destination = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter3"]
            errorresponse_threshold = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter4"]
            errorresponse_consecutivetime = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter5"]
            pinglost_consecutivetime = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter6"]
            schedule = self.RunTest_JsonData[client_id]["Script"][script_id]["Schedule"]

            ping_script_process = f"/storage/emulated/0/Documents/Ping/ScriptSchedule_Ping.sh {ping_name} {ping_type} {ping_destination} {errorresponse_threshold} {errorresponse_consecutivetime} {pinglost_consecutivetime} {schedule}"
            search_command = f"ps -ef | grep sh"
            search_result = Telnet_Device.Execute_Command(search_command)

            if ping_script_process in search_result[1]:
                return
            else:
                ping_command = f"sh /storage/emulated/0/Documents/Ping/ScriptSchedule_Ping.sh {ping_name} {ping_type} {ping_destination} {errorresponse_threshold} {errorresponse_consecutivetime} {pinglost_consecutivetime} {schedule} &"
                Telnet_Device.Execute_Command(ping_command)
                time.sleep(1)

        def youtube_shellscript_command(Telnet_Device, client_id, script_id)->str:
            def get_youtube_liststr(path_txtfile:str)->str:
                list_url = []
                with open(path_txtfile, "r") as file:
                    for line in file:
                        url = line.strip()
                        if url:  
                            list_url.append(url)
                Url_liststr = ""
                for i in range(len(list_url)):
                    if i == 0:
                        Url_liststr = Url_liststr + list_url[i]
                    elif i != 0:
                        Url_liststr = Url_liststr + "," + list_url[i]
                return Url_liststr
                
            youtube_list = get_youtube_liststr(self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter1"])
            youtube_playtime = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter2"]
            eroorpackets_threshold = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter3"]
            errorpackets_consecutivetime = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter4"]
            schedule = self.RunTest_JsonData[client_id]["Script"][script_id]["Schedule"]

            youtube_script_process = f"/storage/emulated/0/Documents/Youtube/ScriptSchedule_Youtube.sh"
            search_command = f"ps -ef | grep sh"
            search_result = Telnet_Device.Execute_Command(search_command)

            if youtube_script_process in search_result[1]:
                return
            else:
                youtube_command = f"sh /storage/emulated/0/Documents/Youtube/ScriptSchedule_Youtube.sh {youtube_list} {youtube_playtime} {eroorpackets_threshold} {errorpackets_consecutivetime} {schedule} &"
                Telnet_Device.Execute_Command(youtube_command)
                time.sleep(1)
          
        def execute_shellscripts(client_id:str=None, port:int=23)->bool:
            try:
                client_ip = self.RunTest_JsonData[client_id]["EtherIP"]
                
                ### Telnet & ADB Coneect.
                Telnet_Device = TelNet(client_ip, port) 
                Telnet_Device.Connect_Devcie()
                time.sleep(1)
                
                ether_shellscript_command(Telnet_Device, client_id)

                wifi_shellscript_command(Telnet_Device, client_id)

                ### Exectue Youtube & Ping Script.
                for script_id in self.RunTest_JsonData[client_id]["Script"]:              
                    script_type = self.RunTest_JsonData[client_id]["Script"][script_id]["Type"]
                    if script_type == "Ping":
                        ping_shellscript_command(Telnet_Device, client_id, script_id)

                    elif script_type == "Youtube":
                        youtube_shellscript_command(Telnet_Device, client_id, script_id)

                Telnet_Device.Disconnect_Device()

            except Exception as e:
                error_message = traceback.format_exc()
                WriteLogFunction.WriteLog(self.LogPath, f"[Error - {client_id}]{error_message}")
                return
            
            
        try:
            with ThreadPoolExecutor(max_workers=64, thread_name_prefix="Execute_ClientShellScripts") as executor:
                futures = []
                for client_id in self.Client_Ether_Status:
                    if self.Client_Ether_Status[client_id] == "normal":
                        futures.append(executor.submit(execute_shellscripts, client_id, 23))

                for future in as_completed(futures):
                    pass
        
        except Exception as e:
            error_message = traceback.format_exc()
            WriteLogFunction.WriteLog(self.LogPath, f"{error_message}")

    ### Step5: Get each client shell script status, and record in [Frame_ClientStatus.ShellScript_Status].
    def ThreadPool_GetShellScriptStatus(self):

        ### Wifi Log Result => "Pass"/"Fail"/"Wait"
        ### Frame_ClientStatus => ShellScript_Status["Wifi"][wifi_id] = "normal"/"error"/"not_schedule"
        def get_wifi_result(Telnet_Device, client_id, wifi_id)->str:
            if self.Client_Ether_Status[client_id] == "error":
                self.Client_ShellScript_Status[client_id].ShellScript_Status["Wifi"][wifi_id] = "error"
                return
            
            ### Get Wifi Log Result.
            result_command = "cat /storage/emulated/0/Documents/Log/Wifi/Wifi_Connection_result.log"
            result_log = Telnet_Device.Execute_Command(result_command)[1]
            result_search = re.search(r"Result\s*:\s*(\w+)", result_log)
            result = result_search.group(1) if result_search else "Fail"

            if result.lower() == "pass":    self.Client_ShellScript_Status[client_id].ShellScript_Status["Wifi"][wifi_id] = "normal"
            elif result.lower() == "wait":  self.Client_ShellScript_Status[client_id].ShellScript_Status["Wifi"][wifi_id] = "not_schedule"
            else:   self.Client_ShellScript_Status[client_id].ShellScript_Status["Wifi"][wifi_id] = "error"

        ### Ping Log Result => "PASS"/"FAIL"/"Wait"
        ### Frame_ClientStatus => ShellScript_Status["Script"][script_id] = "normal"/"error"/"not_schedule"
        def get_ping_result(Telnet_Device, client_id, script_id)->str:
            if self.Client_Ether_Status[client_id] == "error":
                self.Client_ShellScript_Status[client_id].ShellScript_Status["Script"][script_id] = "error"
                return
            
            ### Get Ping Log Result.
            ping_name = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter1"]
            result_command = f"cat /storage/emulated/0/Documents/Log/Ping/{ping_name}_Ping_result.log"
            result_log = Telnet_Device.Execute_Command(result_command)[1]
            result_search = re.search(r"Result\s*:\s*(\w+)", result_log)
            result = result_search.group(1) if result_search else "Fail"

            if result.lower() == "pass":    self.Client_ShellScript_Status[client_id].ShellScript_Status["Script"][script_id] = "normal"
            elif result.lower() == "wait":  self.Client_ShellScript_Status[client_id].ShellScript_Status["Script"][script_id] = "not_schedule"
            else:   self.Client_ShellScript_Status[client_id].ShellScript_Status["Script"][script_id] = "error"
        
        ### Ping Log Result => "PASS"/"FAIL"/"Wait"
        ### Frame_ClientStatus => ShellScript_Status["Script"][script_id] = "normal"/"error"/"not_schedule"
        def get_youtube_result(Telnet_Device, client_id, script_id)->str:
            if self.Client_Ether_Status[client_id] == "error":
                self.Client_ShellScript_Status[client_id].ShellScript_Status["Script"][script_id] = "error"
                return
            
            result_command = f"cat /storage/emulated/0/Documents/Log/Youtube/YoutubePacket_result.log"
            result_log = Telnet_Device.Execute_Command(result_command)[1]
            result_search = re.search(r"Result\s*:\s*(\w+)", result_log)
            result = result_search.group(1) if result_search else "Fail"

            if result.lower() == "pass":    self.Client_ShellScript_Status[client_id].ShellScript_Status["Script"][script_id] = "normal"
            elif result.lower() == "wait":  self.Client_ShellScript_Status[client_id].ShellScript_Status["Script"][script_id] = "not_schedule"
            else:   self.Client_ShellScript_Status[client_id].ShellScript_Status["Script"][script_id] = "error"
        
        def Get_ShellScriptStatus(client_id:str=None, port:int=23)->bool:
            try:
                ### Telnet
                client_ip = self.RunTest_JsonData[client_id]["EtherIP"]
                Telnet_Device = TelNet(client_ip, port) 
                Telnet_Device.Connect_Devcie()

                wifi_id = self.RunTest_JsonData[client_id]["Wifi"]["WifiID"]
                get_wifi_result(Telnet_Device, client_id, wifi_id)

                for script_id in self.RunTest_JsonData[client_id]["Script"]:              
                    script_type = self.RunTest_JsonData[client_id]["Script"][script_id]["Type"]
                    if script_type == "Ping":
                        get_ping_result(Telnet_Device, client_id, script_id)
                    elif script_type == "Youtube":
                        get_youtube_result(Telnet_Device, client_id, script_id)

                ### Close Connection.
                Telnet_Device.Disconnect_Device()
                return
            
            except Exception as e:
                error_message = traceback.format_exc()
                WriteLogFunction.WriteLog(self.LogPath, f"[Error - {client_id}] {error_message}")

        try:
            with ThreadPoolExecutor(max_workers=64, thread_name_prefix="Execute_ClientShellScripts") as executor:
                futures = []
                for client_id in self.RunTest_JsonData:
                    futures.append(executor.submit(Get_ShellScriptStatus, client_id, 23))
                    
                for future in as_completed(futures):
                    pass

        except Exception as e:
            error_message = traceback.format_exc()
            WriteLogFunction.WriteLog(self.LogPath, f"{error_message}")

    ### Step6 : Update each client img status. Execute [Frame_ClientStatus.Update_AllImgStatus()].
    def Update_ClientImgStatus(self):
        try:
            for client_id in self.Client_ShellScript_Status:
                self.Client_ShellScript_Status[client_id].Update_AllImgStatus()

        except Exception as e:
            error_message = traceback.format_exc()
            WriteLogFunction.WriteLog(self.LogPath, f"{error_message}")

    ### Step7 : Update the Counting of each scripts status number.
    def Update_ScriptStatus_Counting(self):
        def get_script_type(script_id:str)->str:
            for script_data in self.Script_JsonData["Script"]:
                if script_data["ScriptID"] == script_id:
                    return script_data["Type"]
            return ""
        
        try:
            wifi = {
                "total": 0,
                "normal": 0,
                "error": 0,
                "not_schedule": 0
            }
            ping = {
                "total": 0,
                "normal": 0,
                "error": 0,
                "not_schedule": 0
            }
            youtube = {
                "total": 0,
                "normal": 0,
                "error": 0,
                "not_schedule": 0
            }
            ether = {
                "total": len(self.Client_Ether_Status),
                "normal": 0,
                "error": 0
            }
            
            for client_id, object_status in self.Client_ShellScript_Status.items():
                ## Count Wifi.
                wifi_status = list(object_status.ShellScript_Status["Wifi"].values())[0]
                wifi["total"] += 1
                if wifi_status == "normal":         
                    wifi["normal"] += 1
                elif wifi_status == "error":        
                    wifi["error"] += 1
                elif wifi_status == "not_schedule": 
                    wifi["not_schedule"] += 1

                ### Count Script.
                for script_id in object_status.ShellScript_Status["Script"]:
                    script_type = get_script_type(script_id)
                    script_status = object_status.ShellScript_Status["Script"][script_id]
                    if script_type == "Ping":
                        ping["total"] += 1
                        if script_status == "normal":         
                            ping["normal"] += 1
                        elif script_status == "error":        
                            ping["error"] += 1
                        elif script_status == "not_schedule": 
                            ping["not_schedule"] += 1
                    elif script_type == "Youtube":
                        youtube["total"] += 1
                        if script_status == "normal":         
                            youtube["normal"] += 1
                        elif script_status == "error":        
                            youtube["error"] += 1
                        elif script_status == "not_schedule": 
                            youtube["not_schedule"] += 1

                ### Count Ether.
                if self.Client_Ether_Status[client_id] == "normal":
                    ether["normal"] += 1
                else:
                    ether["error"] += 1

            ### Update Status_Widget Label.
            self.root.after(0, lambda: self.Information_Widget["Label"]["Ether"].config(text=f'Ether : {ether["total"]}\nNormal : {ether["normal"]}\nError : {ether["error"]}'))
            self.root.after(0, lambda: self.Information_Widget["Label"]["Wifi"].config(text=f'Wifi : {wifi["total"]}\nNormal : {wifi["normal"]}\nError : {wifi["error"]}\nWait : {wifi["not_schedule"]}'))
            self.root.after(0, lambda: self.Information_Widget["Label"]["Ping"].config(text=f'Ping : {ping["total"]}\nNormal : {ping["normal"]}\nError : {ping["error"]}\nWait : {ping["not_schedule"]}'))
            self.root.after(0, lambda: self.Information_Widget["Label"]["Youtube"].config(text=f'Youtube : {youtube["total"]}\nNormal : {youtube["normal"]}\nError : {youtube["error"]}\nWait : {youtube["not_schedule"]}'))

        except Exception as e:
            error_message = traceback.format_exc()
            WriteLogFunction.WriteLog(self.LogPath, f"{error_message}")

    ###===================================================================
    def ReloadJsonData(self):
        self.load_json_data()

    def Stop_Test(self):
        def kill_allprocess(client_id:str=None, port:int=23):
            client_ip = self.RunTest_JsonData[client_id]["EtherIP"]

            ### Telnet & ADB Coneect
            Telnet_Device = TelNet(client_ip, port) 
            Telnet_Device.Connect_Devcie()
            time.sleep(1)

            ### Stop Wifi Scripts.
            wifi_stop_command = f"sh /storage/emulated/0/Documents/Wifi/StopScript_Wifi.sh"
            Telnet_Device.Execute_Command(wifi_stop_command)
            time.sleep(1)
            
            ### Stop Youtube Scripts.
            youtube_stop_command = f"sh /storage/emulated/0/Documents/Youtube/StopScript_Youtube.sh"
            Telnet_Device.Execute_Command(youtube_stop_command)
            time.sleep(1)
            
            ### Stop Ping Scripts.
            for script_id in self.RunTest_JsonData[client_id]["Script"]:
                script_type = self.RunTest_JsonData[client_id]["Script"][script_id]["Type"]
                if script_type == "Ping":
                    ping_name = self.RunTest_JsonData[client_id]["Script"][script_id]["Parameter1"]
                    ping_stop_command = f"sh /storage/emulated/0/Documents/Ping/StopScript_Ping.sh {ping_name}"
                    Telnet_Device.Execute_Command(ping_stop_command)
                    time.sleep(1)

            ### Stop EtherConnection Scripts.
            ether_stop_command = f"sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh ether_check"
            Telnet_Device.Execute_Command(ether_stop_command)
            time.sleep(1)
    
            ## Close Connection.
            Telnet_Device.Disconnect_Device()
            return
        
        try:
            ### Get json_RuntTest.json data.
            ### Stop all shell scripts in each device.
            self.RunTest_JsonData = JsonDataFunction.Get_jsonAllData(self.RunTest_JsonPath)
            with ThreadPoolExecutor(max_workers=64, thread_name_prefix="Stop_ClientShellScripts") as executor:
                futures = []
                for client_id in self.RunTest_JsonData:
                    futures.append(executor.submit(kill_allprocess, client_id))

                ### Get all result from [futures].
                total_count = len(futures)
                completed_count = 0
                for future in as_completed(futures):
                    completed_count += 1
                    self.Show_Message(f"Stop Test. Processing {completed_count}/{total_count} ...", "red")

            ### Remove json_RunTest.json.
            if os.path.exists(self.RunTest_JsonPath):
                os.remove(self.RunTest_JsonPath)

            ### Remove all client status frames.
            for situation in self.Frame_Situation:
                self.Frame_Situation[situation].destroy()
            self.Frame_Situation = {}
            self.Frame_ClientID = {}
            self.Client_Ether_Status = {}
            self.Client_ShellScript_Status = {}

            self.root.after(0, lambda: self.Information_Widget["Label"]["Wifi"].config(text="WiFi : 0 \nNormal : 0 \nError : 0 \nWait : 0"))
            self.root.after(0, lambda: self.Information_Widget["Label"]["Ping"].config(text="Ping : 0 \nNormal : 0 \nError : 0 \nWait : 0"))
            self.root.after(0, lambda: self.Information_Widget["Label"]["Youtube"].config(text=f"Youtube : 0 \nNormal : 0 \nError : 0 \nWait : 0"))

            self.Show_Message(f"Ready", "gray")
            self.stoptest_callback()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            WriteLogFunction.WriteLog(self.LogPath, f"{error_message}")

if __name__ == "__main__":
    width = 800
    height = 600

    root = tk.Tk()
    root.title("Frame Monitor Test")
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.resizable(True, True)
    app = Frame_Monitor(root)  
    app.Update_RunTest_Json()
    app.LoadCreate_ClientStatusFrame()
    root.mainloop()


    