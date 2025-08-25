import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip  
from PIL import ImageEnhance, ImageOps, ImageFilter

import os
import shutil
from datetime import datetime
import traceback
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import Function.MyFunction_JsonData as JsonDataFunction
import Function.MyFunction as MyFunction
from Function.MyFunction_Telnet import TelNet

class Page_ADBDownloadLog():
    def __init__(self, root):

        self.root = root
        height = 300
        width = 830
        self.root.title("ADB Download Log")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        self.root.resizable(True, True)

        style = ttk.Style()
        # style.theme_use('clam')
        style.configure("Title.TLabel", font=("Segoe UI", 13, "bold"), foreground="blue")
        style.configure("Label.TLabel", font=("Segoe UI", 10), foreground="black")
        style.configure("Count.TLabel", font=("Segoe UI", 11, "bold"), foreground="black")
        style.configure("Message.TLabel", font=("Segoe UI", 8), foreground="Red")
        style.configure("Icon.Toolbutton", padding=0, borderwidth=0, relief="flat")
        style.configure("TEntry", font=("Segoe UI", 8))


        self.load_json_data()
        self.Create_widgets()
        self.Updating_SelectedCount()
        self.Set_DefaultData()

        ### self.Thread_StopEvent is used to stop the thread when the window is closed.
        self.Thread_StopEvent = threading.Event()
        self.ThreadPool_CurrentExecutor = None

    def load_json_data(self):
        self.JsonPath = "./Parameter/json_PageADBDownload.json"
        self.JsonData = JsonDataFunction.Get_jsonAllData(self.JsonPath)["Client"]
        self.JsonData.sort(key=lambda x: x["Index"])

    def Create_widgets(self):
        self.Image = {}
        self.Image["Button_SelectFolder"] = ImageTk.PhotoImage(Image.open("./img/add_folder.png").resize((20,20)))
        self.Image["Button_SelectAll"] = ImageTk.PhotoImage(Image.open("./img/selectall.png").resize((30, 30)))
        self.Image["Button_DownloadLog"] = ImageTk.PhotoImage(Image.open("./img/download.png").resize((30,30)))
        self.Image["Button_StopThread"] = ImageTk.PhotoImage(Image.open("./img/stop.png").resize((30,30)))

        self.Frame = {}
        self.Frame["Main"] = tk.Frame(self.root, borderwidth=1, relief="flat", highlightbackground="#a9a7a7", highlightthickness=1)
        self.Frame["Main"].grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        ### Create Cancas.
        self.Main_Widget = {}
        self.Main_Widget["Button"] = {}
        self.Main_Widget["Label"] = {}
        self.Main_Widget["Entry"] = {}

        self.Main_Widget["Title"] = ttk.Label(self.Frame["Main"], text="Download Logs from Devices.", style="Title.TLabel")
        self.Main_Widget["Label"]["Count"] = ttk.Label(self.Frame["Main"], text="Count : 0/0", style="Count.TLabel")
        self.Main_Widget["Label"]["DownloadPath"] = ttk.Label(self.Frame["Main"], text="Download Path :", style="Label.TLabel")
        self.Main_Widget["Entry"]["DownloadPath"] = ttk.Entry(self.Frame["Main"], width=50, state="readonly", style="TEntry")

        self.Main_Widget["Button"]["SelectFolder"] = ttk.Button(self.Frame["Main"], image=self.Image["Button_SelectFolder"], cursor="hand2", command=self.Button_SelectFolder)

        self.Main_Widget["Button"]["SelectAll"] = ttk.Button(self.Frame["Main"], image=self.Image["Button_SelectAll"], cursor="hand2", command=self.Button_SelectAll)
        self.Main_Widget["Button"]["Download"] = ttk.Button(self.Frame["Main"], image=self.Image["Button_DownloadLog"], cursor="hand2", command=self.Button_DownloadLogs)
        self.Main_Widget["Button"]["StopThread"] = ttk.Button(self.Frame["Main"], image=self.Image["Button_StopThread"], cursor="hand2", command=self.Button_StopThread)
        self.Main_Widget["Canvas"] = tk.Canvas(self.Frame["Main"], relief="flat", highlightthickness=1, highlightbackground="#cccccc")
        self.Main_Widget["ScrollBar"] = ttk.Scrollbar(self.Frame["Main"], orient="vertical", command=self.Main_Widget["Canvas"].yview)
        self.Main_Widget["Canvas"].configure(yscrollcommand=self.Main_Widget["ScrollBar"].set)
        self.Main_Widget["Label"]["Message"] = ttk.Label(self.Frame["Main"], text="Ready", style="Message.TLabel")

        self.Main_Widget["Title"].grid(row=0, column=0, columnspan=2, padx=5, pady=(10, 0), sticky="w")
        self.Main_Widget["Label"]["Count"].grid(row=0, column=2, columnspan=4, padx=(0, 0), pady=(10, 0), sticky="se")
        self.Main_Widget["Label"]["DownloadPath"].grid(row=1, column=0, padx=(5, 0), pady=(5, 0), sticky="w")
        self.Main_Widget["Entry"]["DownloadPath"].grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="w")
        self.Main_Widget["Button"]["SelectFolder"].grid(row=1, column=2, padx=(5,0), pady=(5, 0), sticky="w")
        self.Main_Widget["Button"]["SelectAll"].grid(row=1, column=3, columnspan=3, padx=(0, 86), pady=(5, 0), sticky="e")
        self.Main_Widget["Button"]["Download"].grid(row=1, column=4, columnspan=2, padx=(0, 43), pady=(5, 0), sticky="e")
        self.Main_Widget["Button"]["StopThread"].grid(row=1, column=5, padx=(3, 0), pady=(5, 0), sticky="e")
        self.Main_Widget["Canvas"].grid(row=2, column=0, columnspan=6, padx=(5,0), pady=(5, 5), sticky="nsew")
        self.Main_Widget["ScrollBar"].grid(row=2, column=6, padx=(0, 0), pady=(0, 5), sticky="ns")
        self.Main_Widget["Label"]["Message"].grid(row=3, column=0, columnspan=7, padx=(0,5), pady=(0, 5), sticky="e")
        self.Frame["Main"].grid_rowconfigure(2, weight=1)
        self.Frame["Main"].grid_columnconfigure(4, weight=1)

        ### Create CheckButton.
        ### Store CheckButton with dictionary.
        ### self.Main_Widget["CheckButton"] = {
        ###         "CheckButton": check_button,
        ###         "CheckVar": check_var,
        ###         "EtherIP": client_data["EtherIP"]}
        self.Frame["Canvas"] = ttk.Frame(self.Main_Widget["Canvas"])
        self.Frame["Canvas"].bind( "<Configure>",lambda e: self.Main_Widget["Canvas"].configure(scrollregion=self.Main_Widget["Canvas"].bbox("all")))
        self.Main_Widget["Canvas"].create_window((0, 0), window=self.Frame["Canvas"], anchor="nw")

        self.Main_Widget["CheckButton"] = []
        for i, client_data in enumerate(self.JsonData):
            check_var = tk.IntVar(value=False)  # 明確指定預設為未勾選
            check_button = tk.Checkbutton(self.Frame["Canvas"], text=client_data["EtherIP"], variable=check_var, command=self.Updating_SelectedCount)
            check_button.grid(row=int(i/5), column=i%5, padx=10, pady=5, sticky="w")
            self.Main_Widget["CheckButton"].append({"CheckButton": check_button,
                                                    "CheckVar": check_var,
                                                    "EtherIP": client_data["EtherIP"]})

        ### After all widgets created, update scroll region and move to top.
        self.Main_Widget["Canvas"].yview_moveto(0) 

        Tooltip = {
            "Button_SelectFolder": Hovertip(self.Main_Widget["Button"]["SelectFolder"], "Select the Folder where Logs will be saved.", hover_delay=300),
            "Button_SelectAll": Hovertip(self.Main_Widget["Button"]["SelectAll"], "Select or Deselect All Devices.", hover_delay=300),
            "Button_Download": Hovertip(self.Main_Widget["Button"]["Download"], "Download Logs from Selected Devices.", hover_delay=300),
            "Button_Download": Hovertip(self.Main_Widget["Button"]["StopThread"], "Stop Downloading the Logs.", hover_delay=300)
        }
    
    def Set_DefaultData(self):
        download_path = JsonDataFunction.Get_jsonAllData(self.JsonPath)["DownloadPath"]
        self.Main_Widget["Entry"]["DownloadPath"]["state"] = "normal"
        self.Main_Widget["Entry"]["DownloadPath"].delete(0,tk.END)
        self.Main_Widget["Entry"]["DownloadPath"].insert(0, download_path)
        self.Main_Widget["Entry"]["DownloadPath"]["state"] = "readonly"
        
    ###====================================================================
    def Updating_SelectedCount(self, *args):
        selected_num = 0
        total_num = len(self.Main_Widget["CheckButton"])
        for check_button in self.Main_Widget["CheckButton"]:
            if check_button["CheckVar"].get():
                selected_num += 1

        self.Main_Widget["Label"]["Count"].config(text=f"Count : {selected_num}/{total_num}")

    def Button_SelectFolder(self):
        try:
            ### Select File Frame.
            folder_path = filedialog.askdirectory(title="Select Json Folder", parent=self.root)
            if folder_path != "":
                folder_path = folder_path + "/"
                self.Main_Widget["Entry"]["DownloadPath"]["state"] = "normal"
                self.Main_Widget["Entry"]["DownloadPath"].delete(0,tk.END)
                self.Main_Widget["Entry"]["DownloadPath"].insert(0, folder_path)
                self.Main_Widget["Entry"]["DownloadPath"]["state"] = "readonly"
                JsonDataFunction.Update_jsonFileData(
                    file_path=self.JsonPath,
                    key_value="DownloadPath",
                    value=folder_path
                )

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
    
    def Button_SelectAll(self):
        try:
            selected_count = sum(1 for check_button in self.Main_Widget["CheckButton"] if check_button["CheckVar"].get())
            if selected_count == len(self.Main_Widget["CheckButton"]):
                for check_button in self.Main_Widget["CheckButton"]:
                    check_button["CheckVar"].set(0)
            else:
                for check_button in self.Main_Widget["CheckButton"]:
                    check_button["CheckVar"].set(1)

            self.Updating_SelectedCount()
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)

    '''
    After Download Log from Devices, renamed xxx.log to 20250819_171032_xxx.log,
    and moved to new folder with date name.
    --------------------------------------------------------
    Folder Structure
    ├── 158--
    │   ├── Log (ori_folder_path)
    │   │   ├── Ping (ori_folder_script)
    │   │   |   |──xxx.log (ori_file_path) -> 20250819_171032_xxx.log (ori_file_path_rename)
    │   │   ├── Wifi
    │   │   |   |──xxx.log
    │   │   ├── Youtube
    │   │   |   |──xxx.log
    │   ├── 20250821 (new_folder_path)
    │   │   ├── Ping (new_folder_script)
    │   │   |   |──20250819_171032_xxx.log (new_file_path)
    │   │   ├── Wifi
    │   │   |   |──20250819_171032_xxx.log
    │   │   ├── Youtube
    │   │   |   |──20250819_171032_xxx.log
    '''
    def Button_DownloadLogs(self):

        def threadpool_check_telnet_connection(selected_devices:list)->bool:
            def check_telnet_connection(host:str, port:int=23)-> dict:
                try:
                    device = TelNet(host, port) 
                    return {"Device":host, "Result":device.Check_Connection()[0]}
                except Exception as e:
                    error_message = traceback.format_exc()
                    messagebox.showwarning("Error", error_message, parent=self.root)
                    return {"Device":host, "Result":"FAIL"}

            ### Use ThreadPoolExecutor to check telnet connection for each device.
            completed_count = 0
            total_count = len(selected_devices)
            futures = []
            self.ThreadPool_CurrentExecutor = ThreadPoolExecutor(max_workers=64, thread_name_prefix="Check_ClientEtherConnection")
            for device_ip in selected_devices:
                if self.ThreadPool_CurrentExecutor is None:     break
                completed_count += 1
                self.root.after(0, lambda completed_count=completed_count, total_count=total_count: 
                                self.Main_Widget["Label"]["Message"].config(text=f"Checking Telnet Connection {completed_count} / {total_count}  ..."))
                futures.append(self.ThreadPool_CurrentExecutor.submit(check_telnet_connection, device_ip, 23))

            ether_checkresult = {"PASS":[],"FAIL":[]}
            for future in as_completed(futures):
                if self.ThreadPool_CurrentExecutor is None:
                    for remaining_future in futures:
                        remaining_future.cancel()
                    break  
                thread_respone = future.result()  
                ether_checkresult[thread_respone["Result"]].append(thread_respone["Device"])

            ### Check the result of telnet connection.
            if ether_checkresult["FAIL"] != [] and self.ThreadPool_CurrentExecutor is not None:
                fail_count = len(ether_checkresult["FAIL"])
                messagebox.showwarning("Error", f"{fail_count} of Devices Ether Connection Failed:\n\n {', '.join(ether_checkresult['FAIL'])}.", parent=self.root)
                self.ThreadPool_CurrentExecutor.shutdown(wait=True)
                self.ThreadPool_CurrentExecutor = None
                return False
            
            ### Return True and False.
            if self.ThreadPool_CurrentExecutor is None:
                return False
            self.ThreadPool_CurrentExecutor.shutdown(wait=True)
            self.ThreadPool_CurrentExecutor = None
            return True

        def threadpool_check_adb_connection(selected_devices:list):
            # ### [adb kill-server]
            # self.root.after(0, lambda: self.Main_Widget["Label"]["Message"].config(text=f"adb kill-server ..."))
            # MyFunction.Run_Subprocess("adb kill-server")
            # time.sleep(2)

            ### [adb connect {device_ip}] - Connect to each device.
            ### Use ThreadPoolExecutor to check ADB connection for each device.
            completed_count = 0
            total_count = len(selected_devices)
            futures = []
            self.ThreadPool_CurrentExecutor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="ADB_Connect")
            for device_ip in selected_devices:
                if self.ThreadPool_CurrentExecutor is None:     break
                completed_count += 1
                self.root.after(0, lambda completed_count=completed_count, total_count=total_count: 
                                    self.Main_Widget["Label"]["Message"].config(text=f"{device_ip} ADB Connecting {completed_count} / {total_count}  ..."))      
                futures.append(self.ThreadPool_CurrentExecutor.submit(MyFunction.Run_Subprocess, f"adb connect {device_ip}"))

            for future in as_completed(futures):
                if self.ThreadPool_CurrentExecutor is None:
                    for remaining_future in futures:
                        remaining_future.cancel()
                    break
          
            ### [adb devices] - Check connection status of devices.
            ### Get "adb devices" result, and check if each device_ip is in the result.
            connection_result:dict = {"PASS":set(),"FAIL":set()}
            result = MyFunction.Run_Subprocess("adb devices")
            for device_ip in selected_devices:
                if device_ip in result[1]:
                    connection_result["PASS"].add(device_ip)
                else:
                    connection_result["FAIL"].add(device_ip)

            if connection_result["FAIL"] != set() and self.ThreadPool_CurrentExecutor is not None:
                fail_count = len(connection_result["FAIL"])
                messagebox.showwarning("Error", f"{fail_count} of Devices ADB Connection Failed:\n\n {', '.join(connection_result['FAIL'])}.", parent=self.root)
                self.ThreadPool_CurrentExecutor.shutdown(wait=True)
                self.ThreadPool_CurrentExecutor = None
                return False
            
            ### Return True and False.
            if self.ThreadPool_CurrentExecutor is None:
                return False
            self.ThreadPool_CurrentExecutor.shutdown(wait=True)
            self.ThreadPool_CurrentExecutor = None
            return True
        
        def threadpool_download_logs(selected_devices:list):
            def download_log_files(device_ip:str, destination_folder:str)-> None:
                command = f"adb -s {device_ip}:5555 pull /storage/emulated/0/Documents/Log/ {destination_folder}"
                result = MyFunction.Run_Subprocess(command)
            
            ### [adb pull /storage/emulated/0/Documents/Log/ {destination_folder}] 
            ### Use ThreadPoolExecutor to download logs for each device.
            completed_count = 0
            total_count = len(selected_devices)
            download_path = self.Main_Widget["Entry"]["DownloadPath"].get() + "MultiClient_Log/"
            futures = []
            self.ThreadPool_CurrentExecutor = ThreadPoolExecutor(max_workers=64, thread_name_prefix="Download_Logs")
            for device_ip in selected_devices:
                if self.ThreadPool_CurrentExecutor is None:     break
                completed_count += 1
                self.root.after(0, lambda completed_count=completed_count, total_count=total_count: 
                                    self.Main_Widget["Label"]["Message"].config(text=f"{device_ip} Log Downloading {completed_count} / {total_count}  ..."))  
                folder = download_path + device_ip.split(".")[-1]
                MyFunction.Create_Folder(folder)
                futures.append(self.ThreadPool_CurrentExecutor.submit(download_log_files, device_ip, folder))

            for future in as_completed(futures):
                if self.ThreadPool_CurrentExecutor is None:
                    for remaining_future in futures:
                        remaining_future.cancel()
                    break  
            
            ### Return True and False.
            if self.ThreadPool_CurrentExecutor is None:
                return False
            self.ThreadPool_CurrentExecutor.shutdown(wait=True)
            self.ThreadPool_CurrentExecutor = None
            return True

        def threadpool_check_downloadfolder(selected_devices:list):
            def check_download_folder(device_ip:str, destination_folder:str)-> dict:
                folder = destination_folder + device_ip.split(".")[-1] + "/Log"
                if not os.path.exists(folder):
                    return {"Device": device_ip, "Result": "FAIL"}
                return {"Device": device_ip, "Result": "PASS"}

            ### Check if the download folder exists for each device.
            download_path = self.Main_Widget["Entry"]["DownloadPath"].get() + "MultiClient_Log/"
            completed_count = 0
            total_count = len(selected_devices)
            futures = []
            self.ThreadPool_CurrentExecutor = ThreadPoolExecutor(max_workers=64, thread_name_prefix="Download_Logs")
            for device_ip in selected_devices:
                if self.ThreadPool_CurrentExecutor is None:     break
                completed_count += 1
                self.root.after(0, lambda completed_count=completed_count, total_count=total_count: 
                                    self.Main_Widget["Label"]["Message"].config(text=f"{device_ip} Checking Download Folder {completed_count} / {total_count}  ..."))  
                futures.append(self.ThreadPool_CurrentExecutor.submit(check_download_folder, device_ip, download_path))

            check_result = {"PASS":set(),"FAIL":set()}   
            for future in as_completed(futures):
                if self.ThreadPool_CurrentExecutor is None:
                    for remaining_future in futures:
                        remaining_future.cancel()
                    break 
                result = future.result()
                check_result[result["Result"]].add(result["Device"])
            
            ### Check the result of download folder check.
            if check_result["FAIL"] != set() and self.ThreadPool_CurrentExecutor is not None:
                fail_count = len(check_result["FAIL"])
                messagebox.showwarning("Error", f"{fail_count} of Devices Download Folder Check Failed:\n\n {', '.join(check_result['FAIL'])}.", parent=self.root)
                self.ThreadPool_CurrentExecutor.shutdown(wait=True)
                self.ThreadPool_CurrentExecutor = None
                return False

            ### Return True and False.
            if self.ThreadPool_CurrentExecutor is None:
                return False
            self.ThreadPool_CurrentExecutor.shutdown(wait=True)
            self.ThreadPool_CurrentExecutor = None
            return True
        
        def threadpool_rename_folderfiles(selected_devices:list):
            def rename_download_folderfile(device_ip:str, download_folder_path:str, formatted_time:str)-> None:
                formatted_time = formatted_time
                formatted_date = formatted_time.split("_")[0]

                ### Current log folder path and New log folder path.
                ori_folder_path = download_folder_path + device_ip.split(".")[-1] + "/Log"
                new_folder_path = download_folder_path + device_ip.split(".")[-1] + f"/{formatted_date}"

                ### Check if the original folder exists.
                if os.path.exists(ori_folder_path):
                    for scripttype in os.listdir(ori_folder_path):
                        ori_folder_script = os.path.join(ori_folder_path, scripttype)
                        for filename in os.listdir(ori_folder_script):
                            ### Step1:
                            ### Rename file in current downloading folder with adding time stamp.
                            ori_file_path = os.path.join(ori_folder_script, filename)
                            ori_file_path_rename = os.path.join(ori_folder_script, f"{formatted_time}_{filename}")
                            
                            ### Step2:
                            ### Create new folder with date name if not exist.
                            new_folder_script = os.path.join(new_folder_path, scripttype)
                            new_file_path = os.path.join(new_folder_script, f"{formatted_time}_{filename}")
                            MyFunction.Create_Folder(new_folder_script)
                            MyFunction.Rename_file(ori_file_path, ori_file_path_rename)

                            ### Step3:
                            ### Move renamed file to new folder.
                            shutil.move(ori_file_path_rename, new_file_path)

                    ### Step4:
                    ### Remove old downloading folder.
                    shutil.rmtree(ori_folder_path)

            formatted_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            download_path = self.Main_Widget["Entry"]["DownloadPath"].get() + "MultiClient_Log/"
            completed_count = 0
            total_count = len(selected_devices)
            futures = []
            self.ThreadPool_CurrentExecutor = ThreadPoolExecutor(max_workers=64, thread_name_prefix="Rename_FolderFiles")
            for device_ip in selected_devices:
                if self.ThreadPool_CurrentExecutor is None:     break
                completed_count += 1
                self.root.after(0, lambda completed_count=completed_count, total_count=total_count: 
                                    self.Main_Widget["Label"]["Message"].config(text=f"{device_ip} Processing Download Folder {completed_count} / {total_count}  ...")) 
                futures.append(self.ThreadPool_CurrentExecutor.submit(rename_download_folderfile, device_ip, download_path, formatted_time)) 
                
            for future in as_completed(futures):
                if self.ThreadPool_CurrentExecutor is None:
                    for remaining_future in futures:
                        remaining_future.cancel()
                    break 

            ### Return True and False.
            if self.ThreadPool_CurrentExecutor is None:
                return False
            self.ThreadPool_CurrentExecutor.shutdown(wait=True)
            self.ThreadPool_CurrentExecutor = None
            return True
        
        def thread_function(selected_devices:list):
            try:
                ### Disable the SelectFolder, SelectAll, and Download buttons to prevent multiple clicks.
                self.root.after(0, lambda: self.Main_Widget["Button"]["SelectFolder"].config(state=tk.DISABLED))
                self.root.after(0, lambda: self.Main_Widget["Button"]["SelectAll"].config(state=tk.DISABLED))    
                self.root.after(0, lambda: self.Main_Widget["Button"]["Download"].config(state=tk.DISABLED))  
                self.root.after(0, self.Main_Widget["Label"]["Message"].config(text=f"Checking Clients Connection ..."))  

                if not threadpool_check_telnet_connection(selected_devices):    return
                if not threadpool_check_adb_connection(selected_devices):    return
                if not threadpool_download_logs(selected_devices):   return
                threadpool_check_downloadfolder(selected_devices)
                threadpool_rename_folderfiles(selected_devices)

            except Exception as e:
                error_message = traceback.format_exc()
                self.root.after(0, lambda: messagebox.showwarning("Error", error_message, parent=self.root))
                return
            
            finally:
                ### Enable the SelectFolder, SelectAll, and Download buttons after the operation is done.
                self.root.after(0, lambda: self.Main_Widget["Button"]["SelectFolder"].config(state=tk.NORMAL))
                self.root.after(0, lambda: self.Main_Widget["Button"]["SelectAll"].config(state=tk.NORMAL))    
                self.root.after(0, lambda: self.Main_Widget["Button"]["Download"].config(state=tk.NORMAL))  
                self.root.after(0, self.Main_Widget["Label"]["Message"].config(text=f"Ready"))   

        try:
            selected_devices = [ check_button["EtherIP"] for check_button in self.Main_Widget["CheckButton"] if check_button["CheckVar"].get()]
            if not selected_devices:
                messagebox.showwarning("Warning", "Please select at least one device.", parent=self.root)
                return
            
            selected_count = len(selected_devices)
            result = messagebox.askyesno("Download Logs", f"Are you sure to download {selected_count} devices of logs?", parent=self.root)
            if not result:
                return 
            
            thread = threading.Thread(target=thread_function, args=(selected_devices, ), daemon=True)
            thread.start()
            
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return 

    def Button_StopThread(self):
        if self.ThreadPool_CurrentExecutor is not None:
            self.ThreadPool_CurrentExecutor.shutdown(wait=False)
            self.ThreadPool_CurrentExecutor = None
            self.Main_Widget["Label"]["Message"].config(text="Stop Downloading Logs ...")
                    
if __name__ == "__main__":
    root = tk.Tk()
    app = Page_ADBDownloadLog(root)
    root.mainloop()


