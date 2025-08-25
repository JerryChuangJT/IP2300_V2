import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class Page_ShowItemDetail():
    def __init__(self, root, item_values:list, treeview_columns:list):
        self.root = root
        self.TreeView_Columns = treeview_columns
        self.item_values = item_values

        #---------------------------------------------------------------------
        width = 450
        height = 450
        self.root.title("Item Details")
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        self.root.resizable(True, True)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_detail_window()

    def create_detail_window(self):
        ### Create ScrollerText.
        text_widget = ScrolledText(self.root, 
                                   font=("Consolas", 10), 
                                   wrap=tk.NONE,
                                   bg="light yellow", 
                                   fg="black")
        text_widget.grid(row=0, column=0, padx=(10,3), pady=10, sticky="nsew")

        ### Define tags for formatting.
        text_widget.tag_configure("index", font=("Consolas", 9), foreground="black")
        text_widget.tag_configure("column_name", font=("Consolas", 11, "bold"), foreground="blue")
        text_widget.tag_configure("label", font=("Consolas", 10, "bold"), foreground="darkred")
        text_widget.tag_configure("value", font=("Consolas", 10, "bold"), foreground="black")
        text_widget.tag_configure("len_count", font=("Consolas", 9), foreground="black")
        text_widget.tag_configure("separator", font=("Consolas", 8), foreground="lightgray")
        
        ### Insert formatted content.
        self.insert_formatted_content(text_widget)
        text_widget.config(state=tk.DISABLED)

    def insert_formatted_content(self, text_widget):
        for i, column_name in enumerate(self.TreeView_Columns):
            if i < len(self.item_values):
                ### Index and column name (bold blue).
                content = f"[{i+1}] "
                text_widget.insert(tk.END, content, "index")

                content = f"{column_name}\n"
                text_widget.insert(tk.END, content, "column_name")
                
                ### label (bold red).
                content = "        value : "
                text_widget.insert(tk.END, content, "label")
                
                # 實際值（綠色背景）
                content = f"'{self.item_values[i]}'\n"
                text_widget.insert(tk.END, content, "value")
                
                # 長度標籤（粗體紅色）
                content = "        length : "
                text_widget.insert(tk.END, content, "label")
                
                # 長度值（灰色）
                content = f"{len(str(self.item_values[i]))}\n"
                text_widget.insert(tk.END, content, "len_count")
                
                # 分隔線
                content = "-" * 40 + "\n"
                text_widget.insert(tk.END, content, "separator")