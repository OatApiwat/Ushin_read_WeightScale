import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import pyodbc
from datetime import datetime
from tkinter import messagebox
class ToolsRegisterApp:
    def __init__(self, master):
        self.master = master
        self.frist_add = True
        self.frist_remove = True
        self.auto_show = 0
        # self.connection = pyodbc.connect('DRIVER={SQL Server};'
        #                     'SERVER=127.0.0.1;'
        #                     'DATABASE=U-shin_db;'
        #                     'UID=sa;'
        #                     'PWD=sa@admin;')
        ##remove
        # master.title("MIC QR Code Register")
        # self.notebook = ttk.Notebook(master)
        # self.notebook.pack(fill='both', expand=True)
        # self.register_tools_frame = ttk.Frame(self.notebook)
        # self.notebook.add(self.register_tools_frame, text='Register Tools')
        # self.create_register_tools_page()
        ############
    def create_register_tools_page(self):
        # Add content to the register_tools_frame
        self.add_label = tk.Label(self.register_tools_frame, text="Add Tools", font=("Arial", 10, "bold"))
        self.add_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.refresh_button = tk.Button(self.register_tools_frame, text="Clear Data", command=self.clear_data)
        self.refresh_button.grid(row=0, column=5, rowspan=1, columnspan=1, padx=5, pady=5, sticky="e")
        
        self.type_label = tk.Label(self.register_tools_frame, text="Type:", font=("Arial", 10, "bold"))
        self.type_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.tools_id_label = tk.Label(self.register_tools_frame, text="ID No:", font=("Arial", 10, "bold"))
        self.tools_id_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        self.calibrate_date_label = tk.Label(self.register_tools_frame, text="Calibrate Date:", font=("Arial", 10, "bold"))
        self.calibrate_date_label.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        self.expiration_date_label = tk.Label(self.register_tools_frame, text="Expiration Date:", font=("Arial", 10, "bold"))
        self.expiration_date_label.grid(row=1, column=4, padx=5, pady=5, sticky="w")
        
        
        self.add_type_combobox = ttk.Combobox(self.register_tools_frame, values=["weight","caliper","pin_gate","micro_meter"], width=10)
        self.add_type_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        self.tools_id_entry = tk.Entry(self.register_tools_frame)
        self.tools_id_entry.grid(row=2, column=2, padx=5, pady=5)
        
        self.calibrate_date_entry = DateEntry(self.register_tools_frame, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        self.calibrate_date_entry.delete(0, tk.END)  # ลบค่าทั้งหมดที่มีอยู่ใน DateEntry
        self.calibrate_date_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        
        self.expiration_date_entry = DateEntry(self.register_tools_frame, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        self.expiration_date_entry.delete(0, tk.END)  # ลบค่าทั้งหมดที่มีอยู่ใน DateEntry
        self.expiration_date_entry.grid(row=2, column=4, padx=5, pady=5, sticky="w")
        
        self.add_button = tk.Button(self.register_tools_frame, text="Add", command=self.add_data, font=("Arial", 10, "bold"), width=6)
        self.add_button.grid(row=2, column=5, rowspan=1, columnspan=1, padx=5, pady=5, sticky="w")
        ##For remove
        self.remove_label = tk.Label(self.register_tools_frame, text="Remove Tools", font=("Arial", 10, "bold"))
        self.remove_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.add_type_remove_combobox = ttk.Combobox(self.register_tools_frame, values=["weight","caliper","pin_gate","micro_meter"], width=10)
        self.add_type_remove_combobox.grid(row=4, column=1, padx=5, pady=5)
        
        
        self.tools_id_remove_combobox = ttk.Combobox(self.register_tools_frame, values=[], width=15)
        self.tools_id_remove_combobox.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.add_type_remove_combobox.bind("<<ComboboxSelected>>", self.on_add_type_remove_change)
        
        self.calibrate_date_label_text = tk.Label(self.register_tools_frame, text="xx-xx-xxxx", font=("Arial", 10))
        self.calibrate_date_label_text.grid(row=4, column=3, columnspan=1, padx=5, pady=5)
        
        self.expiration_date_label_text = tk.Label(self.register_tools_frame, text="xx-xx-xxxx", font=("Arial", 10))
        self.expiration_date_label_text.grid(row=4, column=4, columnspan=1, padx=5, pady=5)
        
        self.remove_button = tk.Button(self.register_tools_frame, text="Remove", command=self.remove_data,font=("Arial", 10, "bold"))
        self.remove_button.grid(row=4, column=5, rowspan=1, columnspan=1, padx=5, pady=5, sticky="w")
        ##Show tools data
        self.show_tools_label = tk.Label(self.register_tools_frame, text="Show Data for Tools type: ", font=("Arial", 10, "bold"))
        self.show_tools_label.grid(row=5, column=0,columnspan=2, padx=5, pady=5, sticky="w")
        
        self.show_type_remove_combobox = ttk.Combobox(self.register_tools_frame, values=["weight","caliper","pin_gate","micro_meter"], width=10)
        self.show_type_remove_combobox.grid(row=5, column=2, padx=5, pady=5)
        
        self.show_button = tk.Button(self.register_tools_frame, text="SHOW", command=self.show_data, font=("Arial", 9, "bold"), width=10)
        self.show_button.grid(row=5, column=3, rowspan=1, columnspan=1, padx=5, pady=5, sticky="w")
        
        # Treeview and Scrollbar
        self.tree = ttk.Treeview(self.register_tools_frame, columns=("Tools_ID", "Calibrate_Date", "Expiration_Date"), show="headings")
        self.tree.grid(row=6, column=0, columnspan=7, padx=20, pady=5, sticky="nsew")

        # Add Scrollbar
        self.scrollbar = ttk.Scrollbar(self.register_tools_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=6, column=7, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Set column headings
        self.tree.heading("Tools_ID", text="Tools ID")
        self.tree.heading("Calibrate_Date", text="Calibrate Date")
        self.tree.heading("Expiration_Date", text="Expiration Date")

    def clear_data(self):
        # ล้างข้อมูลใน Combobox
        self.add_type_combobox.set('')
        self.tools_id_entry.delete(0, tk.END)
        self.calibrate_date_entry.delete(0, tk.END)
        self.expiration_date_entry.delete(0, tk.END)
        self.add_type_remove_combobox.set('')
        self.tools_id_remove_combobox.set('')
        # ล้างข้อมูลใน Label
        self.calibrate_date_label_text.config(text='xx-xx-xxxx')
        self.expiration_date_label_text.config(text='xx-xx-xxxx')
    
    def add_data(self):
        # ดึงข้อมูลจากอินพุท
        tool_type = self.add_type_combobox.get()
        tools_id = self.tools_id_entry.get()
        calibrate_date = self.calibrate_date_entry.get()
        expiration_date = self.expiration_date_entry.get()
        if (not self.frist_add):
            if any([not tool_type,not tools_id,not calibrate_date,not expiration_date]):
                messagebox.showwarning("Warning", "Please fill in all fields for add tools.")
                return

        try:
            cursor = self.connection.cursor()
            # Execute the SQL query to insert data into the database
            sql_query = """
                        MERGE INTO register_tools_tb AS target
                        USING (VALUES (?, ?, ?, ?)) AS source (Tools_Type, Tools_ID, Calibrate_Date, Expiration_Date)
                        ON target.Tools_ID = source.Tools_ID AND target.Tools_Type = source.Tools_Type
                        WHEN MATCHED THEN
                            UPDATE SET
                                target.Calibrate_Date = source.Calibrate_Date,
                                target.Expiration_Date = source.Expiration_Date
                        WHEN NOT MATCHED THEN
                            INSERT (Tools_Type, Tools_ID, Calibrate_Date, Expiration_Date)
                            VALUES (source.Tools_Type, source.Tools_ID, source.Calibrate_Date, source.Expiration_Date);
                        """

            cursor.execute(sql_query, (tool_type, tools_id, calibrate_date, expiration_date))
            self.connection.commit()
            cursor.close()
            # ล้างข้อมูลในอินพุท
            messagebox.showinfo("Success", f"Tool {tools_id} has been saved to the database")
            self.auto_show = 1
            self.show_data()
            self.clear_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while saving {tools_id} to the database: {str(e)}")
            print("Error", f"Error occurred while saving {tools_id} to the database: {str(e)}")
        self.frist_add = False
  
    def remove_data(self):
        tools_id = self.tools_id_remove_combobox.get()
        if (not self.frist_add):
            if any([not tools_id]):
                messagebox.showwarning("Warning", "Please fill in all fields for remove tools.")
                return
        try:
            if tools_id:
                # ลบข้อมูลออกจากฐานข้อมูล
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM register_tools_tb WHERE Tools_ID = ?", (tools_id,))
                self.connection.commit()
                cursor.close()

                # ล้างข้อมูลใน Combobox และ Label
                self.tools_id_remove_combobox.set('')
                self.calibrate_date_label_text.config(text='xx-xx-xxxx')
                self.expiration_date_label_text.config(text='xx-xx-xxxx')
                messagebox.showinfo("Success", f"Tool {tools_id} has been removed from the database")
                self.auto_show = -1
                self.show_data()
                self.clear_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while removing {tools_id} to the database: {str(e)}")
            print("Error", f"Error occurred while removing {tools_id} to the database: {str(e)}")
    
    def show_data(self):
        # Clear previous data
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Get selected tool type
        if (self.auto_show == 1):
            tool_type = self.add_type_combobox.get()
        elif (self.auto_show == -1):
            tool_type = self.add_type_remove_combobox.get()
        else:
            tool_type = self.show_type_remove_combobox.get()
        self.show_type_remove_combobox.set(tool_type)
        # Fetch data from database based on selected tool type
        cursor = self.connection.cursor()
        # cursor.execute("SELECT Tools_ID, Calibrate_Date, Expiration_Date FROM register_tools_tb WHERE Tools_Type = ?", (tool_type,))
        cursor.execute("SELECT Tools_ID, Calibrate_Date, Expiration_Date FROM register_tools_tb WHERE Tools_Type = ? ORDER BY tools_id ASC", (tool_type,))
        data = cursor.fetchall()
        
        # Insert data into the treeview without (',)
        for row in data:
            # Remove the unnecessary (',)
            cleaned_row = tuple(cell.strip("'") for cell in row)
            self.tree.insert("", "end", values=cleaned_row)
        self.auto_show = 0


    
    def on_add_type_remove_change(self, *args):
        # เมื่อมีการเปลี่ยนแปลงค่าของ Combobox ให้อัปเดท Combobox ที่เกี่ยวข้อง
        self.populate_combobox(self.add_type_remove_combobox.get(), 4)
    
    def on_tools_id_remove_change(self, *args):
        # เมื่อมีการเปลี่ยนแปลงค่าของ Combobox ให้อัปเดท Combobox ที่เกี่ยวข้อง
        self.populate_label(self.add_type_remove_combobox.get(), self.tools_id_remove_combobox.get())

    def populate_combobox(self, tool_type, row):
        # ดึงข้อมูลจากฐานข้อมูล
        cursor = self.connection.cursor()
        cursor.execute("SELECT tools_id FROM register_tools_tb WHERE Tools_Type = ?", (tool_type,))
        tools = [row[0] for row in cursor.fetchall()]

        # สร้าง Combobox และกำหนดค่า
        setattr(self, "tools_id_remove_combobox", ttk.Combobox(self.register_tools_frame, values=tools, width=15))
        getattr(self, "tools_id_remove_combobox").grid(row=row, column=2, padx=5, pady=5, sticky="w")
        self.calibrate_date_label_text.config(text="xx-xx-xxxx")
        self.expiration_date_label_text.config(text="xx-xx-xxxx")
        self.tools_id_remove_combobox.bind("<<ComboboxSelected>>", self.on_tools_id_remove_change)  # ผูกเหตุการณ์
        cursor.close()
        
    def populate_label(self, tool_type, tools_id):
        cursor = self.connection.cursor()
        sql_query = "SELECT Calibrate_Date, Expiration_Date FROM register_tools_tb WHERE Tools_Type = ? AND Tools_ID = ?"
        cursor.execute(sql_query, (tool_type, tools_id))
        calibrate_date, expiration_date = cursor.fetchone()
        cursor.close()
        # calibrate_date = datetime.strptime(calibrate_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        # expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").strftime("%d-%m-%Y")

        self.calibrate_date_label_text.config(text=calibrate_date)
        self.expiration_date_label_text.config(text=expiration_date)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToolsRegisterApp(root)  # สร้าง ToolsRegisterApp
    app.create_register_tools_page()  # เรียกใช้ create_register_tools_page เพื่อสร้างหน้า Register Tools
    root.mainloop()

