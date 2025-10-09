import tkinter as tk
from tkinter import ttk, messagebox
from idlelib.tooltip import Hovertip  
import traceback

from Function.Page_ShowItemDetail import Page_ShowItemDetail
from Function.Page_ModifyData_Client import Page_ModifyData_Client

import Function.MyFunction_JsonData as JsonDataFunction

from Class.Class_Button import Button

class Frame_Client():
    def __init__(self, root=None, update_shedulechart_callback=None):
        self.update_shedulechart_callback = update_shedulechart_callback
        self.root = root

        ### Initialize settings.
        self.Setting = {
            "Font": {
                "Title": ("Arial", 13, "bold"),
                "Label": ("Arial", 10),
                "Log": ("Arial", 10)
            }
        }

        self.Image_path = {
            "Button_Edit": "./img/edit.png",
            "Button_add": "./img/add.png",
            "Button_Delete": "./img/minus.png"
        }

        self.load_json_data()
        self.Create_widgets()
        self.Load_ClientData()
        self.Updating_TreeViewCount()   

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)
        self.Schedule_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Schedule.json"
        self.Client_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Client.json"
        self.TreeView_Columns = ["ClientID", "MAC", "EtherIP", "Comment"]
        self.TreeView_Columns.append("Index")
        
    def Create_widgets(self):
        def create_top_widgets():
            self.Top_Widgets = {}
            self.Top_Widgets["Button"] = {}
            self.Top_Widgets["Label"] = {}
            self.Top_Widgets["Scrollerbar"] = {}

            ### Create Widgets.
            self.Top_Widgets["Title"] = tk.Label(self.Frame["Top"], text="Client Parameters", font=self.Setting["Font"]["Title"], foreground="blue")
            self.Top_Widgets["Button"]["Edit"] = Button(self.Frame["Top"], image_path=self.Image_path["Button_Edit"], size=(30,30), command=self.Button_EditData)
            self.Top_Widgets["Button"]["Add"] = Button(self.Frame["Top"], image_path=self.Image_path["Button_add"], size=(30,30), command=self.Button_AddData)
            self.Top_Widgets["Label"]["Count"] = tk.Label(self.Frame["Top"], text="Total : 0/0", font=("Segoe UI", 9), foreground="#6C6C6C")
            self.Top_Widgets["Button"]["Delete"] = Button(self.Frame["Top"], image_path=self.Image_path["Button_Delete"], size=(30,30), command=self.Button_DeleteData)

            self.Top_Widgets["TreeView"] = ttk.Treeview(self.Frame["Top"], columns=self.TreeView_Columns, show="headings", selectmode="extended")
            self.Top_Widgets["TreeView"].bind("<ButtonRelease-1>", self.Updating_TreeViewCount)
            self.Top_Widgets["TreeView"].bind("<Double-Button-3>", show_item_details)
            for i in range(len(self.TreeView_Columns)):
                self.Top_Widgets["TreeView"].heading(self.TreeView_Columns[i], 
                                                     text=self.TreeView_Columns[i], 
                                                     anchor="w", 
                                                     command=lambda col=self.TreeView_Columns[i]: sort_by_column(col=col, reverse=False))
                self.Top_Widgets["TreeView"].column(self.TreeView_Columns[i], width=50, stretch=True)
  
            self.Top_Widgets["Scrollerbar"]["Vertical"] = ttk.Scrollbar(self.Frame["Top"], orient=tk.VERTICAL, command=self.Top_Widgets["TreeView"].yview)
            self.Top_Widgets["TreeView"].configure(yscrollcommand=self.Top_Widgets["Scrollerbar"]["Vertical"].set)
            
            ### Place Widgets.
            self.Top_Widgets["Title"].grid(row=0, column=0, padx=(5,0), pady=(5,0), sticky="w")
            self.Top_Widgets["Button"]["Edit"].grid(row=1, column=0, padx=(5,0), pady=(7,0), sticky="w")
            self.Top_Widgets["Button"]["Add"].grid(row=1, column=0, padx=(50,0), pady=(7,0), sticky="w")
            self.Top_Widgets["Button"]["Delete"].grid(row=1, column=0, padx=(95,0), pady=(7,0), sticky="w")
            self.Top_Widgets["TreeView"].grid(row=2, column=0, columnspan=2, padx=(5,0), pady=(5,0), sticky="nsew")
            self.Top_Widgets["Scrollerbar"]["Vertical"].grid(row=2, column=2, padx=(0,0), pady=(5,0), sticky="ns")
            self.Top_Widgets["Label"]["Count"].grid(row=3, column=1, padx=0, pady=5, sticky="e")

            self.Frame["Top"].grid_rowconfigure(2, weight=1)  # 讓 TreeView 可以自動調整大小
            self.Frame["Top"].grid_columnconfigure(1, weight=1)

            ### Tooltips
            ToolTip = {
                "Button_Edit": Hovertip(self.Top_Widgets["Button"]["Edit"], text='Edit the selected items.', hover_delay=300),
                "Button_Add": Hovertip(self.Top_Widgets["Button"]["Add"], text='Add a new item.', hover_delay=300),
                "Button_Delete": Hovertip(self.Top_Widgets["Button"]["Delete"], text='Delete the selected items.', hover_delay=300),
            }

        def show_item_details(event=None):
            ### Get All Selected Items.
            selection = self.Top_Widgets["TreeView"].selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select an item to view details.", parent=self.root)
                return
            
            ### Get the first selected item and its values.
            for item in selection:
                item_values = self.Top_Widgets["TreeView"].item(item)['values']
                detail_frame = tk.Toplevel(self.root)
                # detail_frame.transient(self.root)
                app = Page_ShowItemDetail(root=detail_frame, 
                                        item_values=item_values, 
                                        treeview_columns=self.TreeView_Columns)

        def sort_by_column(col:str, reverse:bool):
            data = [(self.Top_Widgets["TreeView"].set(item, col), item) for item in self.Top_Widgets["TreeView"].get_children('')]
            data.sort(reverse=reverse, key=lambda t: t[0])
            for index, (val, item) in enumerate(data):
                self.Top_Widgets["TreeView"].move(item, '', index)
            self.Top_Widgets["TreeView"].heading(col, command=lambda: sort_by_column(col=col, reverse=not reverse))

        ### Create Frames.
        self.Frame = {}
        self.Frame["Top"] = tk.Frame(self.root, borderwidth=1, relief="flat", highlightbackground="#a9a7a7", highlightthickness=1)
        self.Frame["Top"].grid(row=0, column=0, padx=5, pady=5, sticky="nsew")  
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
            
        create_top_widgets()

    def Load_ClientData(self):
        client_jsondata = JsonDataFunction.Get_jsonAllData(self.Client_JsonPath)
        for item in self.Top_Widgets["TreeView"].get_children():
            self.Top_Widgets["TreeView"].delete(item)
        for data in client_jsondata["Client"]:
            intput_value = list(data.values())
            index = data["EtherIP"].split(".")[-1].zfill(3)
            intput_value.append(index)
            self.Top_Widgets["TreeView"].insert("", tk.END, values=intput_value)
        
    ###=======================================================================================
    def Updating_TreeViewCount(self, event=None):
        total_num = len(self.Top_Widgets["TreeView"].get_children())
        selected_num = len(self.Top_Widgets["TreeView"].selection())
        self.Top_Widgets["Label"]["Count"].config(text=f"Total : {selected_num}/{total_num}")

    def Button_EditData(self):
        def update_newclientid_from_schedule(old_client_id:str, new_client_id:str):
            try:
                if old_client_id == new_client_id:  return

                schedule_data = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)

                ### Iterate through each situation and filter out clients to be removed.
                for situation_name, situation_data in schedule_data.items():
                    if old_client_id in situation_data["ClientID"]:
                        situation_data["ClientID"].remove(old_client_id)
                        situation_data["ClientID"].append(new_client_id)
                        schedule_data[situation_name] = situation_data
                        break

                ### Update the JSON file with the modified schedule data.
                JsonDataFunction.Update_Entire_jsonFileData(self.Schedule_JsonPath, schedule_data)

            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showwarning("Error", error_message, parent=self.root)
                return

        def edit_itme_client(selected_item_value:list=None, new_item_value:list=None):
            try:
                ### Get original client data list.
                all_client_data = JsonDataFunction.Get_jsonAllData(self.Client_JsonPath)["Client"]

                ### Create the dictionary of the selected item data.
                ### When Get the data from Treeview, no need to get the "Index" column!! (self.TreeView_Columns[:-1])
                selected_data = {}
                for i, key in enumerate(self.TreeView_Columns[:-1], start=0):
                    selected_data[key] = str(selected_item_value[i])

                ### Find the index of the selected item in the original list.
                index_replace_data = all_client_data.index(selected_data)

                ### Update the item at the [index_replace_data].
                ### When Get the data from Treeview, no need to get the "Index" column!! (self.TreeView_Columns[:-1])
                new_value = {}
                for i, key in enumerate(self.TreeView_Columns[:-1], start=0):
                    new_value[key] = new_item_value[i]

                ### Update the JSON file with the new data.
                all_client_data[index_replace_data] = new_value
                JsonDataFunction.Update_jsonFileData(self.Client_JsonPath, "Client", all_client_data)

                ### Reload the client data into the TreeView.
                self.Load_ClientData()

                ### Update the json_Schedule.json if ClientID is changed.
                update_newclientid_from_schedule(selected_item_value[0], new_item_value[0])
                self.update_shedulechart_callback()

            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showwarning("Error", error_message, parent=self.root)
                return
            
        try:
            ### Get seleted item value.
            selection = self.Top_Widgets["TreeView"].selection()
            if len(selection) == 0:
                messagebox.showwarning("Warning", "Please select an item to edit.", parent=self.root)
                return
            
            ### Get the first selected item and its values.
            selection = self.Top_Widgets["TreeView"].selection()
            selected_item = selection[0] if selection else None
            selected_item_values = self.Top_Widgets["TreeView"].item(selected_item)['values'] if selected_item else None
            selected_item_values = selected_item_values[:-1] if selected_item_values else None  # 去除最後的 "Index" 欄位

            clientedit_frame = tk.Toplevel(self.root)
            clientedit_frame.transient(self.root)  # 設定為主視窗的
            clientedit_frame.grab_set()           # 設定為模態視窗
            clientedit_frame.protocol("WM_DELETE_WINDOW", clientedit_frame.destroy)
            app = Page_ModifyData_Client(clientedit_frame,  
                                    label_title="Edit Client Item",   
                                    default_value=selected_item_values,
                                    confirm_callback=edit_itme_client
                                    )
     
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

    def Button_AddData(self):
        def treeview_scrollend():
            self.Top_Widgets["TreeView"].yview_moveto(1.0)
    
        def add_item_client(selected_item_value:list=None, new_item_value:list=None):
            try:
                ### Get original client data list.
                all_client_data = JsonDataFunction.Get_jsonAllData(self.Client_JsonPath)["Client"]

                ### Add new item to the list.
                ### When Get the data from Treeview, no need to get the "Index" column!! (self.TreeView_Columns[:-1])
                add_value = {}
                for i, key in enumerate(self.TreeView_Columns[:-1], start=0):
                    add_value[key] = new_item_value[i]
                all_client_data.append(add_value)
        
                ### Update the JSON file with the new data.
                JsonDataFunction.Update_jsonFileData(self.Client_JsonPath, "Client", all_client_data)

                ### Reload the client data into the TreeView.
                self.Load_ClientData()
                treeview_scrollend()

            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showwarning("Error", error_message, parent=self.root)
                return
        
        try:
            ### Get seleted item value.
            selection = self.Top_Widgets["TreeView"].selection()
            selected_item = selection[0] if selection else None
            selected_item_values = self.Top_Widgets["TreeView"].item(selected_item)['values'] if selected_item else None
            selected_item_values = selected_item_values[:-1] if selected_item_values else None  # 去除最後的 "Index" 欄位

            clientadd_frame = tk.Toplevel(self.root)
            clientadd_frame.transient(self.root)  # 設定為主視窗的
            clientadd_frame.grab_set()           # 設定為模態視窗
            clientadd_frame.protocol("WM_DELETE_WINDOW", clientadd_frame.destroy)
            app = Page_ModifyData_Client(clientadd_frame,  
                                    label_title="Add New Client Item",   
                                    default_value=selected_item_values,
                                    confirm_callback=add_item_client
                                    )

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

    def Button_DeleteData(self):
        def remove_clients_from_schedule(client_ids_to_remove:list):
            try:
                schedule_data = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)

                ### Iterate through each situation and filter out clients to be removed.
                for situation_name, situation_data in schedule_data.items():
                    original_clients:list = situation_data["ClientID"]

                    filtered_clients = []
                    for client_id in original_clients:
                        if client_id not in client_ids_to_remove:
                            filtered_clients.append(client_id)

                    ### Update the Script list for the situation.
                    schedule_data[situation_name]["ClientID"] = filtered_clients

                ### Update the JSON file with the modified schedule data.
                JsonDataFunction.Update_Entire_jsonFileData(self.Schedule_JsonPath, schedule_data)

            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showwarning("Error", error_message, parent=self.root)
                return
            
        try:
            ### Get original Client data list.
            all_client_data = JsonDataFunction.Get_jsonAllData(self.Client_JsonPath)["Client"]
            
            ### Check if any items are selected.
            selection = self.Top_Widgets["TreeView"].selection()
            if len(selection) == 0:                
                return
            selected_count = len(selection)
            result = messagebox.askyesno("Delete items", f"Are you sure to delete {selected_count} selected item(s)?", parent=self.root)
            if not result:
                return 

            ### Get selected items data.
            ### When Get the data from Treeview, no need to get the "Index" column!! (self.TreeView_Columns[:-1])
            ### ex: [
            ###         ]
            list_selected_data = []
            for item in selection:
                item_values = self.Top_Widgets["TreeView"].item(item)['values']
                item_data = {key: str(item_values[i]) for i , key in enumerate(self.TreeView_Columns[:-1], start=0)}
                list_selected_data.append(item_data) 

            ### Remove selected items from [all_client_data].
            for selected_data in list_selected_data:
                if selected_data in all_client_data:
                    all_client_data.remove(selected_data)
                else:
                    messagebox.showerror("Error", "Selected item not found in the data.", parent=self.root)
                    return

            ## Update the JSON file with the modified data.
            JsonDataFunction.Update_jsonFileData(self.Client_JsonPath, "Client", all_client_data)

            ### Remove Selected items from json_Schedule.json.
            remove_client_ids = [data["ClientID"] for data in list_selected_data]
            remove_clients_from_schedule(remove_client_ids)

            ### Reload the Client data into the TreeView.
            self.Load_ClientData()
            self.update_shedulechart_callback()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showwarning("Error", error_message, parent=self.root)
            return

    ###=======================================================================================
    def ReloadJsonData(self):
        self.load_json_data()
        self.Load_ClientData()


if __name__ == "__main__":
    width = 1000
    height = 900

    root = tk.Tk()
    root.title("Client")
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.resizable(True, True)
    app = Frame_Client(root)     
    root.mainloop()