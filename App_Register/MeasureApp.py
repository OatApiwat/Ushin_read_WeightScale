import tkinter as tk
from tkinter import ttk
import pyodbc
from qr_Tab import QRCodeGeneratorApp
from tools_Tab import ToolsRegisterApp
# from show_Tab import ShowData

class MeasureApp:
    def __init__(self, master):
        self.master = master
        self.connection = pyodbc.connect('DRIVER={SQL Server};'
                    'SERVER=RAY1-W11475\SQLEXPRESS;' \
                        'DATABASE=measurement_db;' \
                        'UID=sa;' \
                        'PWD=sa@admin;')
        self.tools_type = ["Weight","Caliper","PinGate","Micrometer","Torque"]
        self.qr_app = QRCodeGeneratorApp(master,self.connection,self.tools_type)
        self.tools_app = ToolsRegisterApp(master,self.connection,self.tools_type)
        
        # self.shows_app = ShowData(master,self.connection)
        master.title("MIC IoT Measurement Register")
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        self.tools_app.register_tools_frame = ttk.Frame(self.notebook)
        self.qr_app.register_part_frame = ttk.Frame(self.notebook)
        # self.tools_app.show_data_from_database = ttk.Frame(self.notebook)
        self.notebook.add(self.tools_app.register_tools_frame, text='Register Tools')
        self.notebook.add(self.qr_app.register_part_frame, text='Register Parts')
        # self.notebook.add(self.qr_app.show_data_from_database, text='Show Data from Data Base')
        
        
        # ให้เรียกใช้ create_register_tools_page หลังจากที่เพิ่มแท็บ "Register Tools"
        self.qr_app.create_register_part_page()
        self.tools_app.create_register_tools_page()
# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = MeasureApp(root)
    root.mainloop()
