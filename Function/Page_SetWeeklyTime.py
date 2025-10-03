import tkinter as tk
import tkinter.ttk as ttkconfirm_callback
from tkinter import ttk, messagebox
from idlelib.tooltip import Hovertip  

from Class.Class_Button import Button

class Listener():
    def __init__(self):
        self.container_listeners = []

    def add_listener(self, callback_function):
        if callback_function not in self.container_listeners:
            self.container_listeners.append(callback_function)

    def execute_all_listeners(self):
        for callback_function in self.container_listeners:
            callback_function()

class Frame_SetTimeRange(tk.Frame, Listener):
    def __init__(self, master, default_time_data:tuple=None, **kwargs):
        tk.Frame.__init__(self, master, borderwidth=1, **kwargs)
        Listener.__init__(self)

        style = ttk.Style()
        style.configure("Title_SetTimeRange.TLabel", font=("Segoe UI", 10, "bold"), foreground="Black")

        default_time_data = default_time_data if default_time_data else ("00:00", 1440)
        self.Create_widgets()
        self.Set_DefaultValue(default_time_data)

    def Create_widgets(self):
        def _on_combobox_change(event=None):
            self.execute_all_listeners()

        self.Main_Widget = {}
        self.Main_Widget["Label"] = {}
        self.Main_Widget["Combobox"] = {}
        self.Main_Widget["Button"] = {}

        # 初始化自動通知為啟用
        self._auto_notify_enabled = True

        values_hrs = [f"{i:02d}" for i in range(24)]
        values_mins = [f"{i:02d}" for i in range(60)]
        values_time = [i for i in range(1, 1441)]

        self.Main_Widget["Label"]["Hrs"] = ttk.Label(self, text="Hrs :", style="Title_SetTimeRange.TLabel")
        self.Main_Widget["Combobox"]["Hrs"] = ttk.Combobox(self, width=8, state="readonly", values=values_hrs)
        self.Main_Widget["Combobox"]["Hrs"].bind('<<ComboboxSelected>>', _on_combobox_change)

        self.Main_Widget["Label"]["Mins"] = ttk.Label(self, text="Mins :", style="Title_SetTimeRange.TLabel")
        self.Main_Widget["Combobox"]["Mins"] = ttk.Combobox(self, width=8, state="readonly", values=values_mins)
        self.Main_Widget["Combobox"]["Mins"].bind('<<ComboboxSelected>>', _on_combobox_change)

        self.Main_Widget["Label"]["Time"] = ttk.Label(self, text="Time(min) :", style="Title_SetTimeRange.TLabel")
        self.Main_Widget["Combobox"]["Time"] = ttk.Combobox(self, width=8, state="readonly", values=values_time)
        self.Main_Widget["Combobox"]["Time"].bind('<<ComboboxSelected>>', _on_combobox_change)

        self.Main_Widget["Label"]["Hrs"].grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.Main_Widget["Combobox"]["Hrs"].grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.Main_Widget["Label"]["Mins"].grid(row=0, column=2, padx=5, pady=2, sticky="e")
        self.Main_Widget["Combobox"]["Mins"].grid(row=0, column=3, padx=5, pady=2, sticky="w")
        self.Main_Widget["Label"]["Time"].grid(row=0, column=4, padx=(50,5), pady=2, sticky="e")
        self.Main_Widget["Combobox"]["Time"].grid(row=0, column=5, padx=5, pady=2, sticky="w")

    def Set_DefaultValue(self, default_time_data:tuple=None):
        hrs, mins = default_time_data[0].split(":")
        self.Main_Widget["Combobox"]["Hrs"].set(hrs)
        self.Main_Widget["Combobox"]["Mins"].set(mins)
        self.Main_Widget["Combobox"]["Time"].set(default_time_data[1])

    def Get_SetTimeData(self):
        hrs = self.Main_Widget["Combobox"]["Hrs"].get()
        mins = self.Main_Widget["Combobox"]["Mins"].get()
        time = self.Main_Widget["Combobox"]["Time"].get()
        return (f"{hrs}:{mins}", int(time))

#====================================================================================================    
class Frame_SetDay(tk.Frame):
    def __init__(self, master, day:str=None, default_time_data:list=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        style = ttk.Style()
        style.configure("Title_SetDay.TLabel", font=("Segoe UI", 14, "bold"), foreground="Blue")
        style.configure("Message_SetDay.TLabel", font=("Segoe UI", 9), foreground="Gray")
        style.configure("Count_SetDay.TLabel", font=("Segoe UI", 9, "bold"), foreground="Gray")

        self.Image_path = {
            "Button_Add": "./img/add.png",
            "Button_Scroller": "./img/scroller.png",
            "Button_Delete": "./img/trash.png",
        }

        ### State Variable.
        self.Flag = {
            "Update_Message": True,
            "update_Messagetimer": None,
            "update_MessageCount":None,
            "Update_Expand": tk.BooleanVar(value=True),
        }

        self.time_range_frames = []
        self.delete_buttons = []

        self.Day:str = day if day else "Monday"
        default_time_data = default_time_data if default_time_data else []
        self.Create_widgets(default_time_data)
        self.Update_Expand()

    def Create_widgets(self, default_time_data:list):
        ### Initial Widgets.
        self.Main_Widget = {}
        self.Main_Widget["Checkbutton"] = {}
        self.Main_Widget["Label"]= {}
        self.Main_Widget["Button"]= {}
        
        # 為了向後相容，保留這些屬性但指向新的屬性
        self.Main_Widget["TimeRangeFrame"] = self.time_range_frames
        self.Main_Widget["Button"]["Delete_TimeRnage"] = self.delete_buttons

        self.Main_Widget["Label"]["Title"] = ttk.Label(self, text=self.Day, style="Title_SetDay.TLabel")
        self.Main_Widget["Label"]["Message"] = ttk.Label(self, text="Time : ", style="Message_SetDay.TLabel")
        self.Main_Widget["Label"]["Count"] = ttk.Label(self, text="Count : 0", style="Count_SetDay.TLabel")
        self.Main_Widget["Button"]["Add"] = Button(self, image_path=self.Image_path["Button_Add"], size=(20,20), command=lambda: self.Button_AddTimeRange())
        self.Main_Widget["Button"]["Scroller"] = Button(self, image_path=self.Image_path["Button_Scroller"], size=(20,20), command=self.Button_UpdateExpand)

        self.Main_Widget["Label"]["Title"].grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.Main_Widget["Label"]["Message"].grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.Main_Widget["Label"]["Count"].grid(row=0, column=3, padx=5, pady=5, sticky="e")
        self.Main_Widget["Button"]["Add"].grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.Main_Widget["Button"]["Scroller"].grid(row=0, column=5, padx=5, pady=5, sticky="e")

        # 調整列權重以防止 Label 擠壓其他元件
        self.columnconfigure(0, weight=0)  # Title 列不伸縮
        self.columnconfigure(1, weight=0)  # Message 列可伸縮，但有最大寬度
        self.columnconfigure(2, weight=1)  # 
        self.columnconfigure(3, weight=0)  # 
        self.columnconfigure(4, weight=0)  # 

        ToolTip = {
            "Button_Add": Hovertip(self.Main_Widget["Button"]["Add"], text="Add a new time range.", hover_delay=300),
            "Button_Scroller": Hovertip(self.Main_Widget["Button"]["Scroller"], text="Expand or collapse the day.", hover_delay=300),
            "Button_Delete":[]
        }

        ### Create Default TimeRange Frame.
        for data in default_time_data:
            self.Create_TimeRange(data)

    def Create_TimeRange(self, default_time_data:tuple=None):
        def delete_timeframe(frame):
            idx = self.time_range_frames.index(frame)

            ### Delete TimeRange Frame.
            self.time_range_frames.pop(idx)
            frame.grid_forget()
            frame.destroy()

            ### Delete Delete Button.
            btn = self.delete_buttons[idx]
            self.delete_buttons.pop(idx)
            btn.grid_forget()
            btn.destroy()

            self.Update_Message()
            
        ### Create TimeRange Frame.
        time_frame = Frame_SetTimeRange(self, default_time_data=default_time_data, relief="flat")
        time_frame.add_listener(self.Update_Message)
        self.time_range_frames.append(time_frame)

        ### Create Delete Button.
        delete_button = Button(self, image_path=self.Image_path["Button_Delete"], size=(20,20), command=lambda frame=time_frame: delete_timeframe(frame))
        self.delete_buttons.append(delete_button)

        self.Update_Expand()
        self.Update_Message()

    def Update_Expand(self):
        if self.Flag["Update_Expand"].get():
            for i, frame in enumerate(self.time_range_frames):
                frame.grid(row=i+1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
            for i, btn in enumerate(self.delete_buttons):
                btn.grid(row=i+1, column=5, padx=5, pady=5, sticky="e")
        else:
            for frame in self.time_range_frames:
                frame.grid_forget() 
            for btn in self.delete_buttons:
                btn.grid_forget()

    def Update_Message(self, event=None):
        def update_count_message():
            message = "Count : "
            message += str(len(self.time_range_frames))
            self.Main_Widget["Label"]["Count"].config(text=message)

        def update_time_message():
            message = "Time : "
            time_data = self.Get_SetTimeData()
            for data in time_data:
                message += data[0] + "," + str(data[1]) + "/"

            max_display_length = 65  
            if message[-1] == "/": message = message[:-1]
            display_message = message if len(message) <= max_display_length else message[:max_display_length] + "..."
            self.Main_Widget["Label"]["Message"].config(text=display_message)
            ToolTip = Hovertip(self.Main_Widget["Label"]["Message"], text=message, hover_delay=300)
            self.Flag["update_Messagetimer"] = None

        if self.Flag["Update_Message"] == False:
            return
        
        if self.Flag["update_Messagetimer"] is not None:
            self.after_cancel(self.Flag["update_MessageCount"])
            self.after_cancel(self.Flag["update_Messagetimer"])

        self.Flag["update_MessageCount"] = self.after(50, update_count_message)
        self.Flag["update_Messagetimer"] = self.after(50, update_time_message)  
    
    ### ----------------------------------------------
    def Button_AddTimeRange(self, default_time_data:tuple=("00:00", 1440)):
        self.Flag["Update_Message"] = True
        self.Create_TimeRange(default_time_data=default_time_data)
        self.Update_Message()

    def Button_UpdateExpand(self):
        if self.time_range_frames == []:
            return
        
        self.Flag["Update_Expand"].set(not self.Flag["Update_Expand"].get())
        self.Update_Expand()

    ### ----------------------------------------------
    def Get_SetTimeData(self):
        return [frame.Get_SetTimeData() for frame in self.time_range_frames]

### ====================================================================================================    
class Page_SetTime_SelectedDays(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        height = 200
        width = 610
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
        self.resizable(True, True)
        self.title("Add Time Range to Selected Days")
        self.transient(master)
        self.grab_set() 
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.DaysSetTime = {
            "Day":[],
            "SetTime":()
        }
        self.Create_widgets()

    def Create_widgets(self):
        self.time_frame = Frame_SetTimeRange(self, default_time_data=("00:00",1440), relief="flat")
        self.time_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.Checkbuttons = []
        for i, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
            check_var = tk.IntVar(value=True)
            check_button = ttk.Checkbutton(self, text=day, variable=check_var, cursor="hand2")
            check_button.grid(row=i%4+1, column=int(i/4), padx=(20,0), pady=5, sticky="w")
            self.Checkbuttons.append({
                "Checkbutton": check_button,
                "Var": check_var,
                "Day": day
            })
            
        button_confirm = Button(self, text="Confirm", command=self.Button_Confirm)
        button_cancel = Button(self, text="Cancel", command=self.Button_Cancel)
        button_confirm.grid(row=4, column=2, padx=5, pady=5, sticky="e")
        button_cancel.grid(row=4, column=3, padx=(0,20), pady=5, sticky="e")

        self.grid_columnconfigure(2, weight=1)

    ### ----------------------------------------------
    def Button_Confirm(self):
        selected_days = [ checkbutton["Day"] for checkbutton in self.Checkbuttons if checkbutton["Var"].get() == 1]
        self.DaysSetTime = {
            "Day":selected_days,
            "SetTime":self.time_frame.Get_SetTimeData()
        }
        self.destroy()

    def Button_Cancel(self):
        self.DaysSetTime = {
            "Day":[],
            "SetTime":()
        }
        self.destroy()

class Page_SetWeeklyTime():
    def __init__(self, master, title:str="None", time_data:str="1,00:00,1440", confirm_callback=None, **kwargs):
        self.ScheduleData:str = ""
        self.confirm_callback = confirm_callback

        self.root = master
        height = 500
        width = 800
        self.root.title(f"Set {title} Weekly Schedule")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        self.root.resizable(True, True)

        self.Class_DayFrame = []
 
        self.Image_path = {
            "Button_ScrollDown": "./img/arrow_down.png",
            "Button_AddTimeRange": "./img/calendars.png",
            "Button_Confirm": "./img/check.png",
            "Button_Cancel": "./img/cancel.png",
        }
    
        self.Create_widgets()
        self.Set_DefaultValue_CreateDayFrame(time_data)

    def Create_widgets(self):
        def on_canvas_configure(event):
            canvas = event.widget
            canvas.itemconfig(self.widget_id["Canvas"], width=canvas.winfo_width()-3)

        self.Main_Widget = {}
        self.widget_id = {}

        ### Create Canvas and Scrollbar.
        self.Main_Widget["Button_AddTimeRange"] = Button(self.root, image_path=self.Image_path["Button_AddTimeRange"], size=(25,25), command=self.Button_AddTimeRange_AllDay)
        self.Main_Widget["Button_ScrollFrame"] = Button(self.root, image_path=self.Image_path["Button_ScrollDown"], size=(25,25), command=self.Button_ScrollAllFrame)
        self.Main_Widget["Canvas"] = tk.Canvas(self.root, relief="flat", highlightthickness=0)
        self.Main_Widget["ScrollBar"] = ttk.Scrollbar(self.root, orient="vertical", command=self.Main_Widget["Canvas"].yview)
        self.Main_Widget["Canvas"].configure(yscrollcommand=self.Main_Widget["ScrollBar"].set)
        self.Main_Widget["Separator"] = ttk.Separator(self.root, orient='horizontal')
        self.Main_Widget["Button_Confirm"] = Button(self.root, text="Confirm", command=self.Button_Conmfirm)
        self.Main_Widget["Button_Cancel"] = Button(self.root, text="Cancel", command=self.Button_Cancel)

        self.Main_Widget["Button_AddTimeRange"].grid(row=0, column=0, padx=(0,50), pady=(5,0), sticky="e")
        self.Main_Widget["Button_ScrollFrame"].grid(row=0, column=0, padx=(0,10), pady=(5,0), sticky="e")
        self.Main_Widget["Canvas"].grid(row=1, column=0, padx=(5,0), pady=0, sticky="nsew")
        self.Main_Widget["ScrollBar"].grid(row=0, column=1, rowspan=2, padx=(0,5), pady=5, sticky="ns")
        self.Main_Widget["Separator"].grid(row=2, column=0, columnspan=2, padx=5, pady=(10,0), sticky="ew")
        self.Main_Widget["Button_Confirm"].grid(row=3, column=0, columnspan=2, padx=(0,120), pady=10, sticky="e")
        self.Main_Widget["Button_Cancel"].grid(row=3, column=0, columnspan=2, padx=(0,5), pady=10, sticky="e")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        ### Create Day Frame_SetDay.
        self.Main_Widget["Frame"] = tk.Frame(self.Main_Widget["Canvas"])
        self.Main_Widget["Frame"].bind( "<Configure>",lambda e: self.Main_Widget["Canvas"].configure(scrollregion=self.Main_Widget["Canvas"].bbox("all")))
        self.widget_id["Canvas"] = self.Main_Widget["Canvas"].create_window((0, 0), window=self.Main_Widget["Frame"], anchor="nw", )
        self.Main_Widget["Canvas"].bind("<Configure>", on_canvas_configure)

        self.Main_Widget["Frame"].columnconfigure(0, weight=1)
        self.Main_Widget["Canvas"].yview_moveto(0) 

        ToolTip = {
            "Button_ScrollFrame": Hovertip(self.Main_Widget["Button_ScrollFrame"], text="Expand or collapse all of the day.", hover_delay=300),
            "Button_AddTimeRange": Hovertip(self.Main_Widget["Button_AddTimeRange"], text="Add a time range to all of the day.", hover_delay=300),
        }

    def Set_DefaultValue_CreateDayFrame(self, time_data:str):
        def anaylze_timedata(time_data:str)->dict:
            weekly_data = {
                "Monday": [],
                "Tuesday": [],  
                "Wednesday": [],
                "Thursday": [],
                "Friday": [],
                "Saturday": [],
                "Sunday": []
            }
            datas = time_data.split('/')
            for data in datas:
                parts = data.split(',')
                if parts[0] == "1":
                    weekly_data["Monday"].append((parts[1], parts[2]))
                elif parts[0] == "2":
                    weekly_data["Tuesday"].append((parts[1], parts[2]))
                elif parts[0] == "3":
                    weekly_data["Wednesday"].append((parts[1], parts[2]))
                elif parts[0] == "4":
                    weekly_data["Thursday"].append((parts[1], parts[2]))
                elif parts[0] == "5":
                    weekly_data["Friday"].append((parts[1], parts[2]))
                elif parts[0] == "6":
                    weekly_data["Saturday"].append((parts[1], parts[2]))
                elif parts[0] == "0":
                    weekly_data["Sunday"].append((parts[1], parts[2]))

            return weekly_data

        Weekly_Data = anaylze_timedata(time_data)
        ### Add Day Frames.
        for i, day in enumerate(Weekly_Data.keys()):
            frame = Frame_SetDay(self.Main_Widget["Frame"], 
                                 day=day, 
                                 default_time_data=Weekly_Data[day], 
                                 close_callback=None,
                                 relief="solid", 
                                 highlightbackground="#B9BCC2", 
                                 highlightcolor="#B9BCC2", 
                                 highlightthickness=2)
            frame.grid(row=i, column=0, padx=3, pady=(0,10), sticky="ew")
            self.Class_DayFrame.append(frame)

    ### ----------------------------------------------
    def Button_ScrollAllFrame(self):
        expends = [frame.Flag["Update_Expand"].get() for frame in self.Class_DayFrame]
        if True in expends:
            for frame in self.Class_DayFrame:
                frame.Flag["Update_Expand"].set(False)
                frame.Update_Expand()
        else:
            for frame in self.Class_DayFrame:
                frame.Flag["Update_Expand"].set(True)
                frame.Update_Expand()
    
    def Button_AddTimeRange_AllDay(self):
        dialog = Page_SetTime_SelectedDays(self.root)
        self.root.wait_window(dialog)
        
        selected_days = dialog.DaysSetTime["Day"]
        set_time_data = dialog.DaysSetTime["SetTime"]
        
        if not selected_days:   
            return

        for frame in self.Class_DayFrame:
            if frame.Day in selected_days:
                frame.Flag["Update_Message"] = False  
                frame.Button_AddTimeRange(default_time_data=set_time_data)

        for frame in self.Class_DayFrame:
            if frame.Day in selected_days:
                frame.Flag["Update_Message"] = True  
                frame.Update_Message()  
    
    def Button_Conmfirm(self):
        result = ""
        ### Get All Time Data Day by Day.
        for day_frame in self.Class_DayFrame:
            ### Convert Day to Number.
            day_num = {
                "Monday": "1",
                "Tuesday": "2",
                "Wednesday": "3",
                "Thursday": "4",
                "Friday": "5",
                "Saturday": "6",
                "Sunday": "0"
            }.get(day_frame.Day)
            
            ### Get Time Data.
            time_data = day_frame.Get_SetTimeData()
            if time_data != []:
                for data in time_data:
                    result += f"{day_num},{data[0]},{data[1]}/"
        result = result[:-1] if result else result
        self.ScheduleData = result

        if self.ScheduleData == "":
            messagebox.showwarning("Error", "The time setting is empty.", parent=self.root)
        else:
            self.confirm_callback(time_data=self.ScheduleData)
            self.root.destroy()

    def Button_Cancel(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Page_SetWeeklyTime(root, 
                             title="Wifi", 
                             time_data="1,09:00,240/1,13:00,240/2,10:00,120/3,14:00,180/4,08:30,90/5,12:00,60/6,15:00,300/0,11:00,150",
                             confirm_callback=None)
    root.mainloop()

    print(app.ScheduleData)