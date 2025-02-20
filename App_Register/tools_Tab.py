import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import pyodbc
from datetime import datetime
from tkinter import messagebox
import babel.numbers

class ToolsRegisterApp:
    def __init__(self, master,sqlconndction,tools_type):
        self.master = master
        self.frist_add = True
        self.frist_remove = True
        self.auto_show = 0
        self.password = "1"
        self.connection = sqlconndction
        self.tools_type = tools_type
        self.add_key_type = []
        self.remove_key_type = []
        self.add_non_key_type = []
        self.remove_non_key_type = []
        self.update_value_tb()
         # ดึง key_id ที่ Type เป็น 'not-selected' จากฐานข้อมูลและเพิ่มลงใน self.remove_key_type
        cursor = self.connection.cursor()
        cursor.execute("SELECT key_id FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'not-selected'")
        for row in cursor.fetchall():
            self.add_key_type.append(row[0])
            self.add_non_key_type.append(row[0])

        # ดึง key_id ที่ Type เป็น 'specification_key' จากฐานข้อมูลและเพิ่มลงใน self.remove_key_type
        cursor.execute("SELECT key_id FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'specification_key'")
        for row in cursor.fetchall():
            self.remove_key_type.append(row[0])

        # ดึง key_id ที่ Type เป็น 'non_specification_key' จากฐานข้อมูลและเพิ่มลงใน self.remove_key_type
        cursor.execute("SELECT key_id FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'non_specification_key'")
        for row in cursor.fetchall():
            self.remove_non_key_type.append(row[0])

        cursor.close()
        
    def create_register_tools_page(self):
        self.create_register_key()
        self.create_register_tools()
        # self.create_register_equiment_id()
    
    def create_register_key(self):  
        # self.register_database_label = tk.Label(self.register_tools_frame, text="Register Key", font=("Arial", 10, "bold"))
        # self.register_database_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.add_specification_key_label = tk.Label(self.register_tools_frame, text="Add Specification Key", font=("Arial", 8, "bold"))
        self.add_specification_key_label.grid(row=1, column=0,columnspan=2, padx=5, pady=5, sticky="w")
        
        self.add_key_combobox = ttk.Combobox(self.register_tools_frame, width=15)
        self.add_key_combobox['values'] = (self.add_key_type)
        self.add_key_combobox.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.pass_add_entry = tk.Entry(self.register_tools_frame, width=10, show="*")
        self.pass_add_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.add_key_button = tk.Button(self.register_tools_frame, text="Add Key", command=self.add_secification_key)
        self.add_key_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        
        self.remove_specification_key_label = tk.Label(self.register_tools_frame, text="Remove Specification Key", font=("Arial", 8, "bold"))
        self.remove_specification_key_label.grid(row=1, column=3,columnspan=2, padx=5, pady=5, sticky="w")
        
        self.remove_key_combobox = ttk.Combobox(self.register_tools_frame, width=15)
        self.remove_key_combobox['values'] = (self.remove_key_type)
        self.remove_key_combobox.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        
        self.pass_remove_entry = tk.Entry(self.register_tools_frame, width=10, show="*")
        self.pass_remove_entry.grid(row=2, column=4, padx=5, pady=5, sticky="w")
        
        self.remove_key_button = tk.Button(self.register_tools_frame, text="Remove Key", command=self.remove_secification_key)
        self.remove_key_button.grid(row=2, column=5, padx=5, pady=5, sticky="w")
        
        
        self.add_non_specification_key_label = tk.Label(self.register_tools_frame, text="Add non-Specification Key", font=("Arial", 8, "bold"))
        self.add_non_specification_key_label.grid(row=3, column=0,columnspan=3, padx=5, pady=5, sticky="w")
        
        self.add_non_key_combobox = ttk.Combobox(self.register_tools_frame, width=15)
        self.add_non_key_combobox['values'] = (self.add_non_key_type)
        self.add_non_key_combobox.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        self.pass_non_add_entry = tk.Entry(self.register_tools_frame, width=10, show="*")
        self.pass_non_add_entry.grid(row=4, column=1, padx=5, pady=5)
        
        self.add_non_key_button = tk.Button(self.register_tools_frame, text="Add Key", command=self.add_non_secification_key)
        self.add_non_key_button.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        
        # self.test_non_label = tk.Label(self.register_tools_frame, text="          ", font=("Arial", 8, "bold"))
        # self.test_non_label.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        
        self.remove_non_specification_key_label = tk.Label(self.register_tools_frame, text="Remove non-Specification Key", font=("Arial", 8, "bold"))
        self.remove_non_specification_key_label.grid(row=3, column=3,columnspan=3, padx=5, pady=5, sticky="w")
        
        self.remove_non_key_combobox = ttk.Combobox(self.register_tools_frame, width=15)
        self.remove_non_key_combobox['values'] = (self.remove_non_key_type)
        self.remove_non_key_combobox.grid(row=4, column=3, padx=5, pady=5, sticky="w")
        
        self.pass_non_remove_entry = tk.Entry(self.register_tools_frame, width=10, show="*")
        self.pass_non_remove_entry.grid(row=4, column=4, padx=5, pady=5, sticky="w")
        
        self.remove_non_key_button = tk.Button(self.register_tools_frame, text="Remove Key", command=self.remove_non_secification_key)
        self.remove_non_key_button.grid(row=4, column=5, padx=5, pady=5, sticky="w")
      
      
    def add_secification_key(self):
        selected_key = self.add_key_combobox.get()
        password = self.pass_add_entry.get()
        if password == self.password:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE [measurement_db].[dbo].[key_type_id_tb] SET Type = 'specification_key' WHERE key_id = ?", (selected_key,))
            self.connection.commit()
            
            # ดึงข้อมูล key จากฐานข้อมูลและอัปเดตค่าในคอมโบบ็อกภายใน combobox
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'not-selected'")
            self.add_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'specification_key'")
            self.remove_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'not-selected'")
            self.add_non_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'non_specification_key'")
            self.remove_non_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            
            # แสดงข้อมูลใหม่ใน combobox
            self.add_key_combobox['values'] = self.add_key_type
            self.remove_key_combobox['values'] = self.remove_key_type
            self.add_non_key_combobox['values'] = self.add_non_key_type
            
            # แจ้งเตือน
            messagebox.showinfo("Success", "Key '{}' added successfully.".format(selected_key))
            
            # ลบค่าในช่องที่ต้องกรอก
            self.add_key_combobox.set('')
            self.pass_add_entry.delete(0, tk.END)
            self.update_value_tb()
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def remove_secification_key(self):
        selected_key = self.remove_key_combobox.get()
        password = self.pass_remove_entry.get()
        if password == self.password:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE [measurement_db].[dbo].[key_type_id_tb] SET Type = 'not-selected' WHERE key_id = ?", (selected_key,))
            self.connection.commit()
            
            # ดึงข้อมูล key จากฐานข้อมูลและอัปเดตค่าในคอมโบบ็อกภายใน combobox
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'not-selected'")
            self.add_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'specification_key'")
            self.remove_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'not-selected'")
            self.add_non_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'non_specification_key'")
            self.remove_non_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            
            # แสดงข้อมูลใหม่ใน combobox
            self.add_key_combobox['values'] = self.add_key_type
            self.remove_key_combobox['values'] = self.remove_key_type
            self.add_non_key_combobox['values'] = self.add_non_key_type
            
            # แจ้งเตือน
            messagebox.showinfo("Success", "Key '{}' removed successfully.".format(selected_key))
            
            # ลบค่าในช่องที่ต้องกรอก
            self.remove_key_combobox.set('')
            self.pass_remove_entry.delete(0, tk.END)
            self.update_value_tb()
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def add_non_secification_key(self):
        selected_key = self.add_non_key_combobox.get()
        password = self.pass_non_add_entry.get()
        if password == self.password:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE [measurement_db].[dbo].[key_type_id_tb] SET Type = 'non_specification_key' WHERE key_id = ?", (selected_key,))
            self.connection.commit()
            
            # ดึงข้อมูล key จากฐานข้อมูลและอัปเดตค่าในคอมโบบ็อกภายใน combobox
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'not-selected'")
            self.add_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'specification_key'")
            self.remove_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'not-selected'")
            self.add_non_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'non_specification_key'")
            self.remove_non_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            
            # แสดงข้อมูลใหม่ใน combobox
            self.add_key_combobox['values'] = self.add_key_type
            self.remove_non_key_combobox['values'] = self.remove_non_key_type
            self.add_non_key_combobox['values'] = self.add_non_key_type
            
            # แจ้งเตือน
            messagebox.showinfo("Success", "Non-specification key '{}' added successfully.".format(selected_key))
            
            # ลบค่าในช่องที่ต้องกรอก
            self.add_non_key_combobox.set('')
            self.pass_non_add_entry.delete(0, tk.END)
            self.update_value_tb()
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def remove_non_secification_key(self):
        selected_key = self.remove_non_key_combobox.get()
        password = self.pass_non_remove_entry.get()
        if password == self.password:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE [measurement_db].[dbo].[key_type_id_tb] SET Type = 'not-selected' WHERE key_id = ?", (selected_key,))
            self.connection.commit()
            
            # ดึงข้อมูล key จากฐานข้อมูลและอัปเดตค่าในคอมโบบ็อกภายใน combobox
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'not-selected'")
            self.add_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'specification_key'")
            self.remove_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'not-selected'")
            self.add_non_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT [key_id] FROM [measurement_db].[dbo].[key_type_id_tb] WHERE Type = 'non_specification_key'")
            self.remove_non_key_type = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            
            # แสดงข้อมูลใหม่ใน combobox
            self.add_key_combobox['values'] = self.add_key_type
            self.remove_non_key_combobox['values'] = self.remove_non_key_type
            self.add_non_key_combobox['values'] = self.add_non_key_type
            
            # แจ้งเตือน
            messagebox.showinfo("Success", "Non-specification key '{}' removed successfully.".format(selected_key))
            
            # ลบค่าในช่องที่ต้องกรอก
            self.remove_non_key_combobox.set('')
            self.pass_non_remove_entry.delete(0, tk.END)
            self.update_value_tb()
            
        else:
            messagebox.showerror("Error", "Incorrect password.")




    def create_register_tools(self):
        # Add content to the register_tools_frame
        self.add_label = tk.Label(self.register_tools_frame, text="Add Tools", font=("Arial", 10, "bold"))
        self.add_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        
        self.refresh_button = tk.Button(self.register_tools_frame, text="Clear Data", command=self.clear_data)
        self.refresh_button.grid(row=10, column=4, rowspan=1, columnspan=1, padx=5, pady=5, sticky="w")
        
        self.type_label = tk.Label(self.register_tools_frame, text="Type:", font=("Arial", 10, "bold"))
        self.type_label.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        
        self.tools_id_label = tk.Label(self.register_tools_frame, text="ID No:", font=("Arial", 10, "bold"))
        self.tools_id_label.grid(row=6, column=2, padx=5, pady=5, sticky="w")
        
        self.calibrate_date_label = tk.Label(self.register_tools_frame, text="Calibrate Date:", font=("Arial", 10, "bold"))
        self.calibrate_date_label.grid(row=6, column=3, padx=5, pady=5, sticky="w")
        
        self.expiration_date_label = tk.Label(self.register_tools_frame, text="Expiration Date:", font=("Arial", 10, "bold"))
        self.expiration_date_label.grid(row=6, column=4, padx=5, pady=5, sticky="w")
        
        self.type_remove_label = tk.Label(self.register_tools_frame, text="Type:", font=("Arial", 10, "bold"))
        self.type_remove_label.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        
        self.tools_remove_id_label = tk.Label(self.register_tools_frame, text="ID No:", font=("Arial", 10, "bold"))
        self.tools_remove_id_label.grid(row=8, column=2, padx=5, pady=5, sticky="w")
        
        self.calibrate_date_remove_label = tk.Label(self.register_tools_frame, text="Calibrate Date:", font=("Arial", 10, "bold"))
        self.calibrate_date_remove_label.grid(row=8, column=3, padx=5, pady=5, sticky="w")
        
        self.expiration_date_remove_label = tk.Label(self.register_tools_frame, text="Expiration Date:", font=("Arial", 10, "bold"))
        self.expiration_date_remove_label.grid(row=8, column=4, padx=5, pady=5, sticky="w")
        
        
        self.add_type_combobox = ttk.Combobox(self.register_tools_frame, values=self.tools_type, width=10)
        self.add_type_combobox.grid(row=7, column=1, padx=5, pady=5)
        
        self.tools_id_entry = tk.Entry(self.register_tools_frame)
        self.tools_id_entry.grid(row=7, column=2, padx=5, pady=5)
        
        self.calibrate_date_entry = DateEntry(self.register_tools_frame, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        self.calibrate_date_entry.delete(0, tk.END)  # ลบค่าทั้งหมดที่มีอยู่ใน DateEntry
        self.calibrate_date_entry.grid(row=7, column=3, padx=5, pady=5, sticky="w")
        
        self.expiration_date_entry = DateEntry(self.register_tools_frame, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        self.expiration_date_entry.delete(0, tk.END)  # ลบค่าทั้งหมดที่มีอยู่ใน DateEntry
        self.expiration_date_entry.grid(row=7, column=4, padx=5, pady=5, sticky="w")
        
        self.add_button = tk.Button(self.register_tools_frame, text="Add", command=self.add_data, font=("Arial", 10, "bold"), width=6)
        self.add_button.grid(row=7, column=5, rowspan=1, columnspan=1, padx=5, pady=5, sticky="w")
        ##For remove
        self.remove_label = tk.Label(self.register_tools_frame, text="Remove Tools", font=("Arial", 10, "bold"))
        self.remove_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        
        self.add_type_remove_combobox = ttk.Combobox(self.register_tools_frame, values=self.tools_type, width=10)
        self.add_type_remove_combobox.grid(row=9, column=1, padx=5, pady=5)
        
        
        self.tools_id_remove_combobox = ttk.Combobox(self.register_tools_frame, values=[], width=15)
        self.tools_id_remove_combobox.grid(row=9, column=2, padx=5, pady=5, sticky="w")
        self.add_type_remove_combobox.bind("<<ComboboxSelected>>", self.on_add_type_remove_change)
        
        self.calibrate_date_label_text = tk.Label(self.register_tools_frame, text="xx-xx-xxxx", font=("Arial", 10))
        self.calibrate_date_label_text.grid(row=9, column=3, columnspan=1, padx=5, pady=5)
        
        self.expiration_date_label_text = tk.Label(self.register_tools_frame, text="xx-xx-xxxx", font=("Arial", 10))
        self.expiration_date_label_text.grid(row=9, column=4, columnspan=1, padx=5, pady=5)
        
        self.remove_button = tk.Button(self.register_tools_frame, text="Remove", command=self.remove_data,font=("Arial", 10, "bold"))
        self.remove_button.grid(row=9, column=5, rowspan=1, columnspan=1, padx=5, pady=5, sticky="w")
        ##Show tools data
        self.show_tools_label = tk.Label(self.register_tools_frame, text="Show Data for Tools type: ", font=("Arial", 10, "bold"))
        self.show_tools_label.grid(row=10, column=0,columnspan=2, padx=5, pady=5, sticky="w")
        
        self.show_type_remove_combobox = ttk.Combobox(self.register_tools_frame, values=self.tools_type, width=10)
        self.show_type_remove_combobox.grid(row=10, column=2, padx=5, pady=5)
        
        self.show_button = tk.Button(self.register_tools_frame, text="SHOW", command=self.show_data, font=("Arial", 9, "bold"), width=10)
        self.show_button.grid(row=10, column=3, rowspan=1, columnspan=1, padx=5, pady=5, sticky="w")
        
        # Treeview and Scrollbar
        self.tree = ttk.Treeview(self.register_tools_frame, columns=("Tools_ID", "Calibrate_Date", "Expiration_Date"), show="headings", height=10)
        self.tree.grid(row=11, column=0, columnspan=7, padx=20, pady=5, sticky="nsew")

        # Add Scrollbar
        self.scrollbar = ttk.Scrollbar(self.register_tools_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=11, column=7, sticky="ns")
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
        # เพิ่มเคลียร์ข้อมูลใน Combobox และ Entry อื่น ๆ ที่เพิ่มเข้ามาใหม่
        self.add_key_combobox.set('')
        self.pass_add_entry.delete(0, tk.END)
        self.remove_key_combobox.set('')
        self.pass_remove_entry.delete(0, tk.END)
        self.add_non_key_combobox.set('')
        self.pass_non_add_entry.delete(0, tk.END)
        self.remove_non_key_combobox.set('')
        self.pass_non_remove_entry.delete(0, tk.END)
    
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
        self.populate_combobox(self.add_type_remove_combobox.get(), 9)
    
    def on_tools_id_remove_change(self, *args):
        # เมื่อมีการเปลี่ยนแปลงค่าของ Combobox ให้อัปเดท Combobox ที่เกี่ยวข้อง
        self.populate_label(self.add_type_remove_combobox.get(), self.tools_id_remove_combobox.get())

    def populate_combobox(self, tool_type, row):
        # ดึงข้อมูลจากฐานข้อมูล
        cursor = self.connection.cursor()
        cursor.execute("SELECT Tools_ID FROM register_tools_tb WHERE Tools_Type = ? ORDER BY Tools_ID ASC", (tool_type,))
        tools = [row[0] for row in cursor.fetchall()]
        print(tools)

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

        self.calibrate_date_label_text.config(text=calibrate_date)
        self.expiration_date_label_text.config(text=expiration_date)


    def update_value_tb(self):
        try:
            cursor = self.connection.cursor()

            # ดึงข้อมูล key_id และ Type จากตาราง key_type_id_tb
            cursor.execute("SELECT key_id, Type FROM key_type_id_tb")
            key_type_data = cursor.fetchall()

            # ดึงรายการหัวคอลัม์ของตาราง value_tb จาก INFORMATION_SCHEMA.COLUMNS
            cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'value_tb'")
            existing_columns = [row[0] for row in cursor.fetchall()]
            print("existing_columns: ",existing_columns)
            for row in key_type_data:
                key_id = row[0]
                key_type = row[1]

                # ตรวจสอบค่าในตาราง key_type_id_tb ว่า key_id มี Type อะไร
                if key_type == "not-selected":
                    # หาก Type เป็น not-selected ให้ตรวจสอบว่ามี key_id นั้นใน value_tb ไหม
                    if key_id in existing_columns:
                        # ถ้ามีให้ลบหัวคอลัมน์ key_id ออกจากตาราง value_tb
                        cursor.execute(f"ALTER TABLE value_tb DROP COLUMN [{key_id}]")
                        # print(f"Column {key_id} has been dropped from value_tb")

                else:
                    # หาก Type ไม่ใช่ not-selected ให้ตรวจสอบว่ามี key_id นั้นใน value_tb ไหม
                    if key_id not in existing_columns:
                        # ถ้าไม่มีให้เพิ่มหัวคอลัมน์ key_id ลงในตาราง value_tb
                        cursor.execute(f"ALTER TABLE value_tb ADD [{key_id}] varchar(50) NULL")
                        # print(f"Column {key_id} has been added to value_tb")

            self.connection.commit()

        except Exception as e:
            print(f"Error occurred while updating value_tb: {str(e)}")
            messagebox.showerror("Error", f"Error occurred while updating value_tb: {str(e)}")
        
        finally:
            cursor.close()
