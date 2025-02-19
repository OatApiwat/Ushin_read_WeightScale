import tkinter as tk
from tkinter import ttk
import pyodbc
from Second_Tab import ToolsRegisterApp
from Frist_Tab import QRCodeGeneratorApp

class MeasureApp:
    def __init__(self, master):
        self.master = master
        self.qr_app = QRCodeGeneratorApp(master)
        self.tools_app = ToolsRegisterApp(master)
        self.qr_app.folder_path = None
        self.qr_app.frist = True
        self.qr_app.state_ = "normal"
        
        self.qr_app.max_values = {
            "Weight": [],
            "Caliper": [],
            "Pin Gate": [],
            "Micro Meter": []
        }
        self.qr_app.min_values = {
            "Weight": [],
            "Caliper": [],
            "Pin Gate": [],
            "Micro Meter": []
        }
        
        self.qr_app.connection = pyodbc.connect('DRIVER={SQL Server};'
                                    'SERVER=127.0.0.1;'
                                    'DATABASE=U-shin_db;'
                                    'UID=sa;'
                                    'PWD=sa@admin;')
        self.tools_app.connection = self.qr_app.connection

        
        master.title("MIC QR Code Register")
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)
        self.qr_app.register_part_frame = ttk.Frame(self.notebook)
        self.tools_app.register_tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.qr_app.register_part_frame, text='Register Parts')
        self.notebook.add(self.tools_app.register_tools_frame, text='Register Tools')
        
        # ให้เรียกใช้ create_register_tools_page หลังจากที่เพิ่มแท็บ "Register Tools"
        self.qr_app.create_register_part_page()
        self.tools_app.create_register_tools_page()

        
# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = MeasureApp(root)
    root.mainloop()
