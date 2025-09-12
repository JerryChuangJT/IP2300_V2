import tkinter as tk
from tkinter import ttk, messagebox
from idlelib.tooltip import Hovertip  
import traceback

from Function.Page_ShowItemDetail import Page_ShowItemDetail
from Function.Page_ModifyData_Script import Page_ModifyData_Script

import Function.MyFunction_JsonData as JsonDataFunction

from Class.Class_Button import Button

class Frame_Script():
    def __init__(self, root=None, close_callback=None):
        self.close_callback = close_callback
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
        self.Load_ScriptData()
        self.Updating_TreeViewCount()   

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)
        self.Script_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Script.json"
        self.TreeView_Columns = ["ScriptID", "Type", "Parameter1", "Parameter2", "Parameter3", "Parameter4", "Parameter5", "Parameter6"]

    def Create_widgets(self):
        def create_top_widgets():
            self.Top_Widgets = {}
            self.Top_Widgets["Button"] = {}
            self.Top_Widgets["Label"] = {}
            self.Top_Widgets["Scrollerbar"] = {}

            ### Create Widgets.
            self.Top_Widgets["Title"] = tk.Label(self.Frame["Top"], text="Script Parameters", font=self.Setting["Font"]["Title"], foreground="blue")
            self.Top_Widgets["Button"]["Edit"] = Button(self.Frame["Top"], image_path=self.Image_path["Button_Edit"], size=(30,30), command=self.Button_EditData)
            self.Top_Widgets["Button"]["Add"] = Button(self.Frame["Top"], image_path=self.Image_path["Button_add"], size=(30,30), command=self.Button_AddData)
            self.Top_Widgets["Label"]["Count"] = tk.Label(self.Frame["Top"], text="Count: 0/0", font=("Arial", 11, "bold"))
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
            self.Top_Widgets["Label"]["Count"].grid(row=1, column=1, columnspan=2, padx=(0,5), pady=(7,0), sticky="se")
            self.Top_Widgets["TreeView"].grid(row=2, column=0, columnspan=2, padx=(5,0), pady=(5,5), sticky="nsew")
            self.Top_Widgets["Scrollerbar"]["Vertical"].grid(row=2, column=2, padx=(0,0), pady=(5,5), sticky="ns")

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
 
    def Load_ScriptData(self):
        script_json_data = JsonDataFunction.Get_jsonAllData(self.Script_JsonPath)
        for item in self.Top_Widgets["TreeView"].get_children():
            self.Top_Widgets["TreeView"].delete(item)
        for data in script_json_data["Script"]:
            self.Top_Widgets["TreeView"].insert("", tk.END, values=list(data.values()))
        
    ###=======================================================================================
    def Updating_TreeViewCount(self, event=None):
        total_num = len(self.Top_Widgets["TreeView"].get_children())
        selected_num = len(self.Top_Widgets["TreeView"].selection())
        self.Top_Widgets["Label"]["Count"].config(text=f"Count : {selected_num}/{total_num}")
    
    def Button_EditData(self):
        def edit_itme_script(selected_item_value:list=None, new_item_value:list=None):
            try:
                ### Get original client data list.
                all_script_data = JsonDataFunction.Get_jsonAllData(self.Script_JsonPath)["Script"]

                ### Create the dictionary of the selected item data.
                selected_data = {}
                for i, key in enumerate(self.TreeView_Columns, start=0):
                    selected_data[key] = str(selected_item_value[i])

                ### Find the index of the selected item in the original list.
                index_replace_data = all_script_data.index(selected_data)
                     
                ### Update the item at the [index_replace_data].
                new_value = {}
                for i, key in enumerate(self.TreeView_Columns, start=0):
                    new_value[key] = new_item_value[i]

                ### Update the JSON file with the new data.
                all_script_data[index_replace_data] = new_value
                JsonDataFunction.Update_jsonFileData(self.Script_JsonPath, "Script", all_script_data)

                ### Reload the client data into the TreeView.
                self.Load_ScriptData()

            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showerror("Error", f"{error_message}", parent=self.root)
                return

        try:
            ### Get seleted item value.
            selection = self.Top_Widgets["TreeView"].selection()
            if len(selection) == 0:
                messagebox.showwarning("Warning", "Please select an item to edit.", parent=self.root)
                return
            ### Get the first selected item and its values.
            selected_item = selection[0] if selection else None
            selected_item_values = self.Top_Widgets["TreeView"].item(selected_item)['values'] if selected_item else None

            ### Create a new window for editing the item.
            scriptadd_frame = tk.Toplevel(self.root)
            scriptadd_frame.transient(self.root)
            scriptadd_frame.grab_set()
            scriptadd_frame.protocol("WM_DELETE_WINDOW", scriptadd_frame.destroy)
            app = Page_ModifyData_Script(root=scriptadd_frame,
                                    label_title="Edit Script Item",   
                                    default_value=selected_item_values,
                                    confirm_callback=edit_itme_script
                                    )
        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)
            return

    def Button_AddData(self):
        def treeview_scrollend():
            self.Top_Widgets["TreeView"].yview_moveto(1.0)

        def add_item_script(selected_item_value:list=None, new_item_value:list=None):
            try:
                ### Get original client data list.
                all_script_data = JsonDataFunction.Get_jsonAllData(self.Script_JsonPath)["Script"]

                ### Add new item to the list.
                add_value = {}
                for i, key in enumerate(self.TreeView_Columns, start=0):
                    add_value[key] = new_item_value[i]
                all_script_data.append(add_value)

                ### Update the JSON file with the new data.
                JsonDataFunction.Update_jsonFileData(self.Script_JsonPath, "Script", all_script_data)

                ### Reload the client data into the TreeView.
                self.Load_ScriptData()
                treeview_scrollend()

            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showerror("Error", f"{error_message}", parent=self.root)

        try:
            ### Get seleted item value.
            selection = self.Top_Widgets["TreeView"].selection()
            selected_item = selection[0] if selection else None
            selected_item_values = self.Top_Widgets["TreeView"].item(selected_item)['values'] if selected_item else None

            ### Create a new window for adding the item.
            scriptadd_frame = tk.Toplevel(self.root)
            scriptadd_frame.transient(self.root)
            scriptadd_frame.grab_set()
            scriptadd_frame.protocol("WM_DELETE_WINDOW", scriptadd_frame.destroy)
            app = Page_ModifyData_Script(root=scriptadd_frame,
                                    label_title="Add New Script Item",   
                                    default_value=selected_item_values,
                                    confirm_callback=add_item_script
                                    )

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)
            return

    def Button_DeleteData(self):
        try:
            ### Get original script data list.
            all_script_data = JsonDataFunction.Get_jsonAllData(self.Script_JsonPath)["Script"]

            ### Check if any items are selected.
            selection = self.Top_Widgets["TreeView"].selection()
            if len(selection) == 0:                
                return
            selected_count = len(selection)
            result = messagebox.askyesno("Delete items", f"Are you sure to delete {selected_count} selected item(s)?", parent=self.root)
            if not result:
                return 
            
            ### Get selected items data.
            list_selected_data = []
            for item in selection:
                item_values = self.Top_Widgets["TreeView"].item(item)['values']
                item_data = {key: str(item_values[i]) for i , key in enumerate(self.TreeView_Columns, start=0)}
                list_selected_data.append(item_data)

            ### Remove selected items from [all_client_data].
            for selected_data in list_selected_data:
                if selected_data in all_script_data:
                    all_script_data.remove(selected_data)
                else:
                    messagebox.showerror("Error", "Selected item not found in the data.", parent=self.root)
                    return
                
            ## Update the JSON file with the modified data.
            JsonDataFunction.Update_jsonFileData(self.Script_JsonPath, "Script", all_script_data)

            ### Reload the client data into the TreeView.
            self.Load_ScriptData()

        except Exception as e:
            error_message = traceback.format_exc()
            messagebox.showerror("Error", f"{error_message}", parent=self.root)
            return

    ###=======================================================================================
    def ReloadJsonData(self):
        self.load_json_data()
        self.Load_ScriptData()

if __name__ == "__main__":
    width = 1000
    height = 900

    root = tk.Tk()
    root.title("Script")
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.resizable(True, True)
    app = Frame_Script(root)     
    root.mainloop()

