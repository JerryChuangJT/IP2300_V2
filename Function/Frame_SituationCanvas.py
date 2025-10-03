import tkinter as tk
import json

import Function.MyFunction_JsonData as JsonDataFunction

class Frame_SituationCanvas():
    def __init__(self, root, situation:str="Execution_1"):
        self.root = root        
        self.Situation = situation
        
        ### Define colors for different elements.
        self.colors = {
            'wifi': "#F18A8A",
            'script1': '#4ECDC4',
            'script2': '#45B7D1', 
            'script3': '#96CEB4',
            'script4': '#FFEAA7',
            'script5': '#D4A5A5',
            'script6': '#C3B1E1',
            'script7': '#FFA07A',
            'script8': '#A0C8F0',
            'script9': '#F7A072',
            'script10': '#B0E57C',
            'background': '#F8F9FA',
            'grid': '#E9ECEF',
            'text': "#61605F",
            'border': '#DEE2E6'
        }
        
        self.load_json_data()
        self.Create_UI()

        ### Bind resize event to redraw everything.
        self.Canvas.bind("<Motion>", self.on_mouse_move)
        self.Canvas.bind("<Configure>", self.on_canvas_resize)

    def load_json_data(self):
        self.Environment_JsonPath = "./Parameter/json_PageSetEnvironment.json"
        self.Environment_JsonData = JsonDataFunction.Get_jsonAllData(self.Environment_JsonPath)

        self.Schedule_JsonPath = self.Environment_JsonData["JsonFilePath"] + "json_Schedule.json"
        self.Schedule_JsonData = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)

    def Create_UI(self):
        Frame_Main = tk.Frame(self.root, bg=self.colors['background'])
        Frame_Main.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10,0))
        
        ### Create Title & Info & Canvas.
        self.Label_Title = tk.Label(Frame_Main, text=f"{self.Situation}", 
                           font=("Arial Black", 14, "bold"), 
                           bg=self.colors['background'], 
                           fg="#465FEC")
        frame_info = tk.Frame(Frame_Main, bg=self.colors['background'])
        self.Canvas = tk.Canvas(Frame_Main, bg=self.colors['background'], 
                           highlightthickness=1, highlightbackground=self.colors['border'])
       
        self.Label_Title.pack(padx=5, pady=(10,0), anchor='sw')
        frame_info.pack(padx=5, pady=(0, 10),  anchor='w')
        self.Canvas.pack(padx=0, fill=tk.BOTH, expand=True)
        
        ### Create Info Label.
        self.Label_Info = tk.Label(frame_info, text="Loading ...", 
                                font=("Calibri", 11), 
                                bg=self.colors['background'], 
                                fg=self.colors['text'])
        self.Label_Info.pack(side=tk.LEFT)

    ### ========================================================================
    ### ========================================================================
    ### Execute all drawing functions.
    def Draw_Everything(self, situation:str=None):
        ### Update situation if provided.
        ### Update Schedule Json Data.
        if situation:
            self.Situation = situation
        self.Schedule_JsonData = JsonDataFunction.Get_jsonAllData(self.Schedule_JsonPath)

        ### Delete previous drawings.
        ### Get the new canvas size.
        self.Canvas.delete("all")
        canvas_width = self.Canvas.winfo_width() or 900
        canvas_height = self.Canvas.winfo_height() or 500
        
        margin_left = 80
        # margin_top = 75
        margin_top = 50

        margin_right = 50
        margin_bottom = 80
        
        chart_width = canvas_width - margin_left - margin_right
        chart_height = canvas_height - margin_top - margin_bottom
        
        ### Update canvas size.
        self.Canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))
        
        ### Draw components.
        self.draw_grid(margin_left, margin_top, chart_width, chart_height)
        self.draw_labels(margin_left, margin_top, chart_width, chart_height)
        self.draw_legend(margin_left, canvas_height - margin_bottom + 20)
        
        ### Draw Wifi and Script bars.
        situation_data = self.Schedule_JsonData.get(self.Situation, {})
        wifi_data = situation_data.get('Wifi', {})
        if wifi_data:
            self.draw_wifi_bars(wifi_data, margin_left, margin_top, chart_width, chart_height)
        
        script_data = situation_data.get('Script', [])
        if script_data:
            self.draw_script_bars(script_data, margin_left, margin_top, chart_width, chart_height)

        ### Update Info Label
        wifi_count = 1 if situation_data.get('Wifi') else 0
        script_count = len(situation_data.get('Script', []))
        client_count = len(situation_data.get('Client', []))

        self.Label_Title.config(text=f"{self.Situation}")
        self.Label_Info.config(text=f"Wifi: {wifi_count} | Scripts: {script_count} | Clients: {client_count}")


    ### Draw Grid.
    def draw_grid(self, margin_left, margin_top, chart_width, chart_height):
        ### Draw vertical lines (hours)
        for hour in range(25):
            x = margin_left + (hour * chart_width / 24)
            self.Canvas.create_line(x, margin_top, 
                                    x, margin_top + chart_height, 
                                    fill=self.colors['grid'], 
                                    width=1)
        
        ### Draw horizontal lines (days)
        for day in range(8):
            y = margin_top + (day * chart_height / 7)
            self.Canvas.create_line(margin_left, y, 
                                    margin_left + chart_width, y, 
                                    fill=self.colors['grid'], width=1)
   
    ### Draw Labels.
    def draw_labels(self, margin_left, margin_top, chart_width, chart_height):
        ### Create time labels.
        for hour in range(0, 25, 2):
            x = margin_left + (hour * chart_width / 24)
            self.Canvas.create_text(x, margin_top - 20, 
                                    text=f"{hour:02d}:00", 
                                    font=("Arial", 10), 
                                    fill=self.colors['text'])
        
        ### Create day labels.
        for day in range(7):
            y = margin_top + (day * chart_height / 7) + (chart_height / 7 / 2)
            self.Canvas.create_text(margin_left - 30, y, 
                                    text=['Sun', 'Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat'][day], 
                                    font=("Microsoft JhengHei", 10, "bold"), 
                                    fill=self.colors['text'])
        
        # ### Create title label.
        # self.Canvas.create_text(margin_left + chart_width / 2, margin_top - 45, 
        #                         text="Time (24-hour)", 
        #                         font=("Calibri", 12, "bold"), 
        #                         fill=self.colors['text'])

    ### Draw Legend.
    def draw_legend(self, start_x, start_y):
        ### Wifi legend.
        self.Canvas.create_rectangle(start_x, start_y, 
                                    start_x + 20, start_y + 15, 
                                    fill=self.colors['wifi'], 
                                    outline=self.colors['wifi'])
        self.Canvas.create_text(start_x + 25, start_y + 7, 
                                text="Wifi", anchor='w',    
                                font=("Calibri", 11, "bold"), 
                                fill=self.colors['text'])
        
        ### Script
        ### Estimate widths to avoid overlap.
        ### English letters ~8px, Chinese characters ~12px.
        script_colors = ['script1', 'script2', 'script3', 'script4', 'script5', 'script6', 'script7', 'script8', 'script9', 'script10']
        script_ids = [ data["ScriptID"] for data in self.Schedule_JsonData[self.Situation]["Script"]]
        legend_item_widths = []
        for name in script_ids:
            text_width = len(name) * 8  
            item_width = 20 + 10 + text_width + 20  # Blocks + spacing + text + margin
            legend_item_widths.append(item_width)
        
        ### Create Script legend items after Wifi legend.
        current_x = start_x + 80  
        for i, (color_key, name) in enumerate(zip(script_colors, script_ids)):
            self.Canvas.create_rectangle(current_x, start_y + ((i//5) * 30) + 6, 
                                         current_x + 20, start_y + ((i//5) * 30) + 10,
                                        fill=self.colors[color_key], 
                                        outline=self.colors[color_key])
            self.Canvas.create_text(current_x + 25, start_y + ((i//5) * 30) + 7, 
                                    text=name, anchor='w',
                                    font=("Calibri", 11, "bold"), 
                                    fill=self.colors['text'])
            current_x += legend_item_widths[i]
            if (i + 1) % 5 == 0:
                current_x = start_x + 80          
    
    ### Parse schedule string into time slots.
    def parse_schedule(self, schedule_str):
        ### Check empty string.
        if not schedule_str:
            return []

        ### Parse schedule string.
        time_slots = []
        segments = schedule_str.split('/')
        for segment in segments:
            parts = segment.split(',')
            if len(parts) == 3:
                try:
                    weekday = int(parts[0])
                    start_time = parts[1]
                    duration = int(parts[2])
                    
                    hour, minute = map(int, start_time.split(':'))
                    start_minutes = hour * 60 + minute
                    end_minutes = min(start_minutes + duration, 24 * 60)
                    
                    time_slots.append({'weekday': weekday,
                                        'start_minutes': start_minutes,
                                        'end_minutes': end_minutes,
                                        'start_time': start_time,
                                        'duration': duration})
                except:
                    continue
        
        return time_slots

    ### Draw Wifi bars.
    def draw_wifi_bars(self, wifi_data, margin_left, margin_top, chart_width, chart_height):
        wifi_id = wifi_data.get('WifiID', 'Unknown')
        schedule = wifi_data.get('Schedule', '')
        time_slots = self.parse_schedule(schedule)
        
        for slot in time_slots:
            weekday = slot['weekday']
            start_minutes = slot['start_minutes']
            end_minutes = slot['end_minutes']
            
            x1 = margin_left + (start_minutes / (24 * 60)) * chart_width
            x2 = margin_left + (end_minutes / (24 * 60)) * chart_width
            
            day_height = chart_height / 7
            y1 = margin_top + (weekday * day_height) + 10
            y2 = margin_top + (weekday * day_height) + (day_height / 2) - 22
        
            self.Canvas.create_rectangle(x1, y1, 
                                         x2, y2, 
                                        fill=self.colors['wifi'], 
                                        outline=self.colors['wifi'],
                                        width=2)

    ### Draw Script bars.
    def draw_script_bars(self, script_data, margin_left, margin_top, chart_width, chart_height):
        script_colors = ['script1', 'script2', 'script3', 'script4', 'script5', 'script6', 'script7','script8', 'script9', 'script10']
        
        for script_index, script in enumerate(script_data):
            script_id = script.get('ScriptID', 'Unknown')
            schedule = script.get('Schedule', '')
            color_key = script_colors[script_index % len(script_colors)]
            
            time_slots = self.parse_schedule(schedule)
            
            for slot in time_slots:
                weekday = slot['weekday']
                start_minutes = slot['start_minutes']
                end_minutes = slot['end_minutes']
                
                x1 = margin_left + (start_minutes / (24 * 60)) * chart_width
                x2 = margin_left + (end_minutes / (24 * 60)) * chart_width
                
                day_height = chart_height / 7
                script_layer_height = (day_height / 2 + 7) / len(script_colors)
                
                y1 = margin_top + (weekday * day_height) + (day_height / 2) - 10 + (script_index * script_layer_height)
                y2 = y1 + script_layer_height - 2
                
                self.Canvas.create_rectangle(x1, y1, 
                                            x2, y2, 
                                            fill=self.colors[color_key], 
                                            outline=self.colors[color_key], width=1)


    def on_canvas_resize(self, event):
        self.Draw_Everything()

    def on_mouse_move(self, event):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = Frame_SituationCanvas(root)
    root.mainloop()
