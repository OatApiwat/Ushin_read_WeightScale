import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import qrcode
import pyodbc
from PIL import ImageTk, Image
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import babel.numbers


class QRCodeGeneratorApp:
    def __init__(self, master,sqlconndction,tools_type):
        self.master = master
        self.folder_path = None
        self.frist = True
        self.state_ = "normal"
        self.count = 0
        self.connection = sqlconndction
        self.tools_type = tools_type #for all tools
        self.tools_types = [] #for collect tools
        self.added_type = []
        self.max_values = {tool_type: [] for tool_type in self.tools_type}
        self.min_values = {tool_type: [] for tool_type in self.tools_type}
        self.added_key_id = {type: [] for type in ['specification_key', 'non_specification_key']}
        self.max_min_window = None
        
    def create_register_part_page(self):
        self.row_index =1
        self.add_specification_input('specification_key')
        self.add_specification_input('non_specification_key')
        self.add_tools_input()
        self.row_footprint = self.row_index
        self.add_footprint()
        self.qr_label = tk.Label(self.register_part_frame)
        
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT key_id FROM key_type_id_tb WHERE Type = ?", 'specification_key')
        specification_key_id = [row.key_id for row in cursor.fetchall()]
        cursor.close()
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT key_id FROM key_type_id_tb WHERE Type = ?", 'non_specification_key')
        non_specification_key_id = [row.key_id for row in cursor.fetchall()]
        cursor.close()
        key_name = specification_key_id + non_specification_key_id + ['','1']
        self.en00_label = tk.Label(self.register_part_frame, text="",width=10)
        self.en00_label.grid(row=1, column=4, columnspan=1, padx=5, pady=5)
        self.qr_label.grid(row=1, column=5, rowspan=(len(key_name)),columnspan = 5, padx=5, pady=5, sticky="nswe")   
        print(len(key_name))  
        if(self.frist):
            self.generate_qrcode()


            
    def add_specification_input(self,type):
        self.added_key_id[f"{type}"] = []
        cursor = self.connection.cursor()
        # row_index = self.row_index  # กำหนดค่าเริ่มต้นของ row_index
        cursor.execute(f"SELECT key_id FROM key_type_id_tb WHERE Type = '{type}'")
        model_keys = cursor.fetchall()  # เก็บข้อมูล key_id ที่มี Type เป็น 'specification_key'
        for key in model_keys:
            key_id = key[0]
            self.added_key_id[f"{type}"].append(key_id)
            label_text = key_id.capitalize() + ":"
            setattr(self, f"{key_id}_label", tk.Label(self.register_part_frame, text=label_text, font=("Arial", 10, "bold")))
            getattr(self, f"{key_id}_label").grid(row=self.row_index, column=0, padx=5, pady=5, sticky="w")

            # เช็คว่า key_id เป็น "Production Date" หรือไม่
            if key_id == "Product Date":
                # สร้าง DateEntry แทน Entry
                setattr(self, f"{key_id}_entry", DateEntry(self.register_part_frame, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy'))
                getattr(self, f"{key_id}_entry").delete(0, tk.END)  # ลบค่าทั้งหมดที่มีอยู่ใน DateEntry
                getattr(self, f"{key_id}_entry").grid(row=self.row_index, column=1, padx=5, pady=5, sticky="w")

            else:
                # สร้าง Entry ปกติ
                setattr(self, f"{key_id}_entry", tk.Entry(self.register_part_frame, state=self.state_))
                getattr(self, f"{key_id}_entry").grid(row=self.row_index, column=1, padx=5, pady=5)

            self.row_index += 1
                    #add button for check part no.
        if(type == 'specification_key'):
            self.check_part_button = tk.Button(self.register_part_frame, text="Check Spec.", command=self.check_spec)
            self.check_part_button.grid(row=self.row_index-1, column=2, rowspan=1, columnspan=2, padx=5, pady=5, sticky="w")
        cursor.close()
    
    def add_tools_input(self):
        self.row_index+=1
        self.add_tools_label = tk.Label(self.register_part_frame, text="Add tools",font=("Arial", 10, "bold"))
        self.add_tools_label.grid(row=self.row_index, column=0, padx=5, pady=5, sticky="w")
        self.add_tools_combobox = ttk.Combobox(self.register_part_frame, width=15)
        self.add_tools_combobox['values'] = self.tools_type
        self.add_tools_combobox.grid(row=self.row_index, column=1, padx=5, pady=5, sticky="w")
        self.add_tools_button = tk.Button(self.register_part_frame, text="Add", command=self.add_tools)
        self.add_tools_button.grid(row=self.row_index, column=2, padx=5, pady=5, sticky="w")
        self.del_tools_button = tk.Button(self.register_part_frame, text="Del", command=self.del_tools)
        self.del_tools_button.grid(row=self.row_index, column=3, padx=5, pady=5, sticky="w")
    
    def check_spec(self):
        # ดึงข้อมูลจากฐานข้อมูล
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT key_id FROM key_type_id_tb WHERE Type = ?", 'specification_key')
        specification_key_id = [row.key_id for row in cursor.fetchall()]
        cursor.close()
        
        specification_values = []
        for spec_id in specification_key_id:
            entry_name = f"{spec_id}_entry"
            specification_value = getattr(self, entry_name).get().upper().replace(" ", "")
            specification_values.append(specification_value)
        
        spec_check = '_'.join(specification_values)
        print("spec_check: ",spec_check)
        # 
        self.clear_tools()
        self.added_type = []
        print("self.added_type: ",self.added_type)
        spec_values, tools_types, type_id_values, max_values, min_values, type_values = self.read_data(spec_check)
        if len(tools_types) > 0:
            
            for type_tools in tools_types:
                if type_tools not in self.added_type:
                    self.added_type.append(type_tools)
            self.update_show_tools()
            # print("spec_values: ",spec_values)
            # print("tools_types: ",tools_types)
            # print("type_id_values: ",type_id_values)
            print("tools_types_check: ",tools_types)
            print("min_values_check: ",min_values)
            # print("type_values: ",type_values)
            for i in range(len(tools_types)):
                self.max_values[f"{tools_types[i]}"] = max_values[i]
                self.min_values[f"{tools_types[i]}"] = min_values[i]
                getattr(self, f"{tools_types[i]}_entry").insert(0,type_values[i])
                getattr(self, f"{tools_types[i]}_max_min_label").config(text=f" {max_values[i]}, {min_values[i]}")
                getattr(self, f"{tools_types[i]}_type_combobox").set(type_id_values[i])
        else:
            messagebox.showerror("Error", "No specification.")

    def read_data(self,spec_check):
        try:
            cursor = self.connection.cursor()
            # Execute SQL query to retrieve data
            # cursor.execute("SELECT Specification_key, Tools_Type, Tools_ID, max, min, iter FROM specification_tb WHERE Specification_key = %s", (spec_check,))
            # Create SQL query
            sql_query = f"SELECT Specification_key, Tools_Type, Tools_ID, max, min, iter FROM specification_tb WHERE Specification_key='{spec_check}'"
            # Execute query
            cursor.execute(sql_query)
            # Fetch all rows
            rows = cursor.fetchall()
            # Close the cursor
            cursor.close()
            
            # Initialize dictionaries to store data
            data_dict = {}

            # Iterate through the rows fetched from the database
            for row in rows:
                # Extract key from row
                key = (row[0], row[1], row[2], row[5])  # Using tuple as key
                # Check if key exists in data_dict
                if key in data_dict:
                    # Append max value to existing max_values list
                    data_dict[key]["max_values"].append(row[3])
                    # Append min value to existing min_values list
                    data_dict[key]["min_values"].append(row[4])
                else:
                    # Create new entry in data_dict
                    data_dict[key] = {
                        "spec_value": row[0],
                        "tools_type": row[1],
                        "type_id_value": row[2],
                        "type_value": row[5],
                        "max_values": [row[3]],
                        "min_values": [row[4]]
                    }

            # Initialize lists to store final data
            spec_values = []
            tools_types = []
            type_id_values = []
            type_values = []
            max_values = []
            min_values = []

            # Iterate through data_dict to extract values
            for key, value in data_dict.items():
                spec_values.append(value["spec_value"])
                tools_types.append(value["tools_type"])
                type_id_values.append(value["type_id_value"])
                type_values.append(value["type_value"])
                max_values.append(value["max_values"])
                min_values.append(value["min_values"])

            # Return the retrieved data
            return spec_values, tools_types, type_id_values, max_values, min_values, type_values

        except Exception as e:
            # Handle any errors that occur during data retrieval
            messagebox.showerror("Error", f"Error occurred while reading data from the database: {str(e)}")
            print("Error", f"Error occurred while reading data from the database: {str(e)}")

    
    def add_tools(self):
        tools_type = self.add_tools_combobox.get()
        if (tools_type in self.added_type):
            messagebox.showwarning("Warning", f"{tools_type} is added.")
            return
        self.clear_tools()
        self.added_type.append(tools_type)
        # self.tools_type.remove(tools_type)
        self.add_tools_combobox['values'] = self.tools_type
        # print(self.added_type)
        self.update_show_tools()
        
    def del_tools(self):
        tools_type = self.add_tools_combobox.get()
        if (len(self.added_type) <= 0) or (tools_type not in self.added_type):
            messagebox.showwarning("Warning", f"{tools_type} is not added.")
            return
        self.clear_tools()
        self.added_type.remove(tools_type)
        # self.tools_type.append(tools_type)
        self.add_tools_combobox['values'] = self.tools_type
        self.update_show_tools()
            
    def update_show_tools(self):
        tools_types = self.added_type#ดึงจาก db เพิ่มเข้าไปในนี้
        self.tools_types = tools_types
        
        row_top = self.row_index
        row_lowwer = row_top+1
        for tool_type in tools_types:
            if (self.count%2 == 0):
                self.row_index+=1
                row_top = self.row_index
                add_column = 0
                print(add_column)
            else:
                add_column = 4
            label_text = tool_type.capitalize() + ":"
            setattr(self, f"{tool_type}_label", tk.Label(self.register_part_frame, text=label_text))
            getattr(self, f"{tool_type}_label").grid(row=row_top, column=0+add_column, padx=5, pady=5, sticky="w"+"e")
            setattr(self, f"{tool_type}_entry", tk.Entry(self.register_part_frame, width=15))
            getattr(self, f"{tool_type}_entry").grid(row=row_top, column=1+add_column, padx=5, pady=5, sticky="w")
            setattr(self, f"add_button_{tool_type}", tk.Button(self.register_part_frame, text="max, min", command=getattr(self, f"add_max_min_{tool_type}"), state=self.state_))
            getattr(self, f"add_button_{tool_type}").grid(row=row_top, column=2+add_column,columnspan=2, padx=5, pady=5, sticky="w")
            if (self.count%2 == 0):
                self.row_index+=1
                row_lowwer = self.row_index
            setattr(self, f"{tool_type}_max_min_label", tk.Label(self.register_part_frame, text=" [], []"))
            getattr(self, f"{tool_type}_max_min_label").grid(row=row_lowwer, column=1+add_column, columnspan=3, padx=5, pady=5, sticky="w")

            self.populate_combobox(f"{tool_type}", row_lowwer,add_column)
            self.count+=1
        self.row_footprint = self.row_index
        print("self.row_footprint: ",self.row_footprint)
        
        if(self.row_footprint > 12):
            self.add_footprint() 
            
    def clear_tools(self):
        tools_types = self.added_type
        print("self.added_type: ",self.added_type)
        if (tools_types):
            for tool_type in tools_types:
                if (self.count%2 == 0):
                    self.row_index-=1
                getattr(self, f"{tool_type}_label").destroy()
                getattr(self, f"{tool_type}_entry").destroy()
                getattr(self, f"add_button_{tool_type}").destroy()
                getattr(self, f"{tool_type}_max_min_label").destroy()
                getattr(self, f"{tool_type}_type_combobox").destroy()
                # self.added_type.remove(tool_type)
                self.count-=1
            
    def populate_combobox(self, tool_type, row,add_column):
        # ดึงข้อมูลจากฐานข้อมูล
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT Tools_ID FROM register_tools_tb WHERE Tools_Type = ?", tool_type)
        tools = [row.Tools_ID for row in cursor.fetchall()]

        # สร้าง Combobox และกำหนดค่า
        setattr(self, f"{tool_type}_type_combobox", ttk.Combobox(self.register_part_frame, values=tools, width=8, state=self.state_))
        getattr(self, f"{tool_type}_type_combobox").grid(row=row, column=0+add_column, padx=5, pady=5)

        cursor.close()
        
    def add_max_min_Weight(self):
        self.open_max_min_window("Weight")

    def add_max_min_Caliper(self):
        self.open_max_min_window("Caliper")

    def add_max_min_PinGate(self):
        self.open_max_min_window("PinGate")

    def add_max_min_Micrometer(self):
        self.open_max_min_window("Micrometer")
        
    def add_max_min_Torque(self):
        self.open_max_min_window("Torque")
         
    def open_max_min_window(self, field):
        print("self.max_min_window: ",self.max_min_window)
        if self.max_min_window and self.max_min_window.winfo_exists():
            messagebox.showwarning("Warning", "Window is already open.")
            return
        print("field: ",field)
        field_entry_value = getattr(self, f"{field}_entry").get()
        if field_entry_value.strip():  # ตรวจสอบว่ามีค่าอย่างน้อยหนึ่งตัวอักษรหรือไม่
            num_entries = int(field_entry_value)
        else:
            num_entries = 0  # กำหนดให้ num_entries เป็น 0 ถ้าไม่มีค่าใน field_entry
            print(f"No value found for {field}")
        
        self.max_min_window = tk.Toplevel(self.register_part_frame)
        self.max_min_window.title(f"Enter Max, Min for {field}")

        entries = []
        for i in range(num_entries):
            label_max = tk.Label(self.max_min_window, text=f"Max {i+1}:")
            label_max.grid(row=i, column=0, padx=5, pady=5)

            label_min = tk.Label(self.max_min_window, text=f"Min {i+1}:")
            label_min.grid(row=i, column=2, padx=5, pady=5)

            entry_max = tk.Entry(self.max_min_window)
            entry_max.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry_max)

            entry_min = tk.Entry(self.max_min_window)
            entry_min.grid(row=i, column=3, padx=5, pady=5)
            entries.append(entry_min)

        def on_submit():
            max_values = [entry.get() for entry in entries[::2]]  # Every other entry is for max values
            min_values = [entry.get() for entry in entries[1::2]]  # Every other entry is for min values
            # Check if all values are float
            if not all((value.lstrip('-').replace('.', '').isdigit() or (value.startswith('-') and value[1:].replace('.', '').isdigit())) for value in max_values + min_values):
                messagebox.showwarning("Warning", "Please enter only numeric values for max and min.")
                return
        # Store max and min values into respective dictionaries
            self.max_values[f"{field}"] = max_values
            self.min_values[f"{field}"] = min_values
            getattr(self, f"{field}_max_min_label").config(text=f" {max_values}, {min_values}")
            # messagebox.showinfo("Info", f"Max values: {max_values}, Min values: {min_values} for {field}")
            self.max_min_window.destroy()

        submit_button = tk.Button(self.max_min_window, text="Submit", command=on_submit)
        submit_button.grid(row=num_entries, column=0, columnspan=4, padx=5, pady=5)
        
    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.folder_path_label.config(text="Selected Folder: " + self.folder_path) 

    def add_footprint(self):
        self.row_footprint+=1
        print(self.row_footprint)
        if(self.row_footprint > 12):
            self.save_var_checkbox.destroy()
            self.save_db_checkbox.destroy()
            self.generate_button.destroy()
            self.folder_button.destroy()
            self.clear_data_button.destroy()
            self.folder_path_label.destroy()
            self.en01_label.destroy()
            self.en02_label.destroy()
            start_row =self.row_footprint
        else:
            start_row =12
            
        self.save_var = tk.BooleanVar(value=False)
        self.save_var_checkbox = tk.Checkbutton(self.register_part_frame, text="Save to Path", variable=self.save_var)
        self.save_var_checkbox.grid(row=start_row, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky="w")
        
        self.save_db = tk.BooleanVar(value=True)
        self.save_db_checkbox = tk.Checkbutton(self.register_part_frame, text="Save to Data Base", variable=self.save_db)
        self.save_db_checkbox.grid(row=start_row, column=1, columnspan=2, rowspan=1, padx=5, pady=5, sticky="w")
        
        self.generate_button = tk.Button(self.register_part_frame, text="Register Part", command=self.generate_qrcode, width=15, height=3, font=("Arial", 12, "bold"))
        self.generate_button.grid(row=start_row, column=5, rowspan=2, columnspan=3, padx=5, pady=5)
        self.en01_label = tk.Label(self.register_part_frame, text="",width=10)
        self.en01_label.grid(row=start_row, column=4, columnspan=1, padx=5, pady=5)
        
        start_row+=1
        self.folder_button = tk.Button(self.register_part_frame, text="Select Folder to save", command=self.select_folder)
        self.folder_button.grid(row=start_row, column=0, columnspan=2, padx=(5, 2), pady=5, sticky='w')
        start_row+=1
        self.clear_data_button = tk.Button(self.register_part_frame, text="Reset data", command=self.clear_data, width=15, height=1, font=("Arial", 9, "bold"))
        self.clear_data_button.grid(row=start_row, column=5, columnspan=3, padx=5, pady=5)
        self.en02_label = tk.Label(self.register_part_frame, text="",width=10)
        self.en02_label.grid(row=start_row, column=4, columnspan=1, padx=5, pady=5)
        
        start_row+=1
        self.folder_path_label = tk.Label(self.register_part_frame, text="Folder is not selected!")
        self.folder_path_label.grid(row=start_row, column=0, columnspan=7, padx=5, pady=5)
        
        
#for QR code
    def generate_qrcode(self):    
        # ดึงข้อมูลจากฐานข้อมูล
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT key_id FROM key_type_id_tb WHERE Type = ?", 'specification_key')
        specification_key_id = [row.key_id for row in cursor.fetchall()]
        cursor.close()
        
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT key_id FROM key_type_id_tb WHERE Type = ?", 'non_specification_key')
        non_specification_key_id = [row.key_id for row in cursor.fetchall()]
        cursor.close()
        
        tools_types = self.tools_types
        key_name = specification_key_id + non_specification_key_id
        key_values = []  # สร้าง Lists เพื่อเก็บค่าของแต่ละ key_id
        type_values = []
        type_id_values = []
        max_values = []
        min_values = []
        specification_values = []
        for spec_id in specification_key_id:
            entry_name = f"{spec_id}_entry"
            specification_value = getattr(self, entry_name).get().upper().replace(" ", "")
            specification_values.append(specification_value)
        for key_id in key_name:
            entry_name = f"{key_id}_entry"
            key_value = getattr(self, entry_name).get().upper().replace(" ", "")
            key_values.append(key_value)
        for type_id in tools_types:
            type_value_entry_name = f"{type_id}_entry"
            type_value_id_entry_name = f"{type_id}_type_combobox"
            type_value = getattr(self, type_value_entry_name).get().upper().replace(" ", "")
            type_id_value = getattr(self, type_value_id_entry_name).get()
            max_value = self.max_values[f"{type_id}"]
            min_value = self.min_values[f"{type_id}"]
            type_values.append(type_value)
            type_id_values.append(type_id_value)
            max_values.append(max_value)
            min_values.append(min_value)
        mic_lot = '_'.join(key_values)
        spec_values = '_'.join(specification_values)
        
        
        # print("mic_lot: ",mic_lot)
        print("spec_values: ",spec_values)
        print("specification_key: ",specification_key_id)
        print("non specification_key: ",non_specification_key_id)
        print("tools_types: ",tools_types)
        print("type_id_values: ",type_id_values)
        print("max_values: ",max_values)
        print("min_values: ",min_values)
        print("type_values: ",type_values)
        
        print("key_name:", key_name) #MIc_Lot
        print("key_values: ",key_values)
        print("mic_lot: ",mic_lot)
        
        

        
        if (not self.frist):
            # แปลงสตริงใน type_values เป็นจำนวนเต็มและเก็บในตัวแปรใหม่
            int_values = [int(val) for val in type_values]
            # ตรวจสอบว่าทุกค่าใน int_values เป็นจำนวนเต็มบวกหรือไม่
            all_positive = all(isinstance(val, int) and (0 < val <= 10) for val in int_values)
            max_values_empty_list = any(not sublist for sublist in max_values)
            min_values_empty_list = any(not sublist for sublist in min_values)
            if any(not value for value in key_values + type_values + type_id_values):
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return
            elif not all_positive:
                messagebox.showwarning("Warning", "The number of times measured should be in the range 1-10.")
                return
            elif not type_id_values:
                messagebox.showwarning("Warning", "Please fill in tools id.")
                return
            elif max_values_empty_list or min_values_empty_list:
                messagebox.showwarning("Warning", "Please fill in max and min.")
                return
        if self.save_var.get():
            if not self.folder_path:  # ตรวจสอบว่ายังไม่ได้เลือกที่เก็บ
                messagebox.showwarning("Warning", "Please select a folder to save the QR Code.")
                return  # หยุดการทำงานของฟังก์ชั่นหากยังไม่ได้เลือกที่เก็บ
        data_insert_to_specification_tb = (spec_values,tools_types,type_id_values,max_values,min_values,type_values)
        data_insert_to_value_tb = mic_lot, tools_types, type_id_values, max_values, min_values, type_values,key_name,key_values
        
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(mic_lot)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((300, 300), Image.LANCZOS)
        if (not self.frist):
            if self.save_var.get() and self.save_db.get():
                self.save_file(mic_lot,img)
                self.insert_to_specification_tb(data_insert_to_specification_tb)
                self.insert_to_value_tb(data_insert_to_value_tb)
                messagebox.showinfo("Success", "Data has been saved to file path and database.")
            elif self.save_db.get():
                self.insert_to_specification_tb(data_insert_to_specification_tb)
                self.insert_to_value_tb(data_insert_to_value_tb)
                messagebox.showinfo("Success", "Data has been saved to file path.")
            else:
                messagebox.showinfo("Success", "QR code has been generated.")
        img = img.resize((170, 170), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.qr_label.configure(image=img)
        self.qr_label.image = img
        self.frist = False


    def insert_to_specification_tb(self, data_insert_to_specification_tb):
        spec_values, tools_types, type_id_values, max_values, min_values, type_values = data_insert_to_specification_tb
        try:
            cursor = self.connection.cursor()
            for i in range(len(tools_types)):
                tools_type = tools_types[i]
                num_loops = int(type_values[i])
                try:
                    sql_query = f"DELETE FROM specification_tb WHERE Specification_key='{spec_values}' AND Tools_Type='{tools_type}'"
                    # # Execute query
                    cursor.execute(sql_query)
                except Exception as e:
                    print("error: DELETE FROM specification_tb as ",str(e))
                for j in range(num_loops):
                    no = j + 1
                    print("no_insert_to_specification_tb: ",no)
                    # # Create SQL query
                    # sql_query = f"SELECT Specification_key, Tools_Type, no FROM specification_tb WHERE Specification_key='{spec_values}' AND Tools_Type='{tools_type}' AND no='{no}'"
                    # # Execute query
                    # cursor.execute(sql_query)

                    # # Fetch results
                    # rows = cursor.fetchall()

                    # # Check if data exists in the database
                    # if len(rows) > 0:
                    #     update_query = f"UPDATE specification_tb SET Tools_ID = '{type_id_values[i]}', max='{max_values[i][j]}', min='{min_values[i][j]}', iter='{num_loops}' WHERE Specification_key='{spec_values}' AND Tools_Type='{tools_type}' AND no='{no}'"
                    #     cursor.execute(update_query)
                    # else:
                    #     # If no data exists, insert new data
                    try:
                        insert_query = f"INSERT INTO specification_tb (Specification_key, Tools_Type,Tools_ID, no, max, min, iter) VALUES ('{spec_values}', '{tools_type}','{type_id_values[i]}', '{no}', '{max_values[i][j]}', '{min_values[i][j]}', '{num_loops}')"
                        cursor.execute(insert_query)
                    except Exception as e:
                        print("error: INSERT INTO specification_tb as ",str(e))
                self.connection.commit()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while insert_to_specification_tb: {str(e)}")
            print("Error", f"Error occurred while insert_to_specification_tb: {str(e)}",tools_type)

    def insert_to_value_tb(self, data_insert_to_value_tb):
        mic_lot, tools_types, type_id_values, max_values, min_values, type_values,key_name,key_values = data_insert_to_value_tb
        try:
            
            for i in range(len(tools_types)):
                cursor = self.connection.cursor()
                # Create SQL query
                sql_query = f"SELECT Expiration_Date FROM register_tools_tb WHERE Tools_Type='{tools_types[i]}' AND Tools_ID='{type_id_values[i]}'"
                cursor.execute(sql_query)
                exp_date = [row.Expiration_Date for row in cursor.fetchall()]
                cursor.close()
                if (len(exp_date)>0):
                    expiration_date = exp_date[0]
                else:
                    messagebox.showerror("Error", f"Error please register tools type: {str(tools_types[i])}")
                tools_type = tools_types[i]
                num_loops = int(type_values[i])
                for j in range(num_loops):
                    no_ = j + 1
                    # Create SQL query
                    try:
                        cursor = self.connection.cursor()
                        sql_query = f"DELETE FROM value_tb WHERE MIC_Lot='{mic_lot}' AND Tools_Type='{tools_type}' AND iter != '{num_loops}'"
                        # # Execute query
                        cursor.execute(sql_query)
                        
                        sql_query = f"SELECT MIC_Lot, Tools_Type, no FROM value_tb WHERE MIC_Lot='{mic_lot}' AND Tools_Type='{tools_type}' AND no='{no_}' AND iter = '{num_loops}'"
                        # Execute query
                        cursor.execute(sql_query)

                        # Fetch results
                        rows = cursor.fetchall()
                        self.connection.commit()
                        cursor.close()
                    except Exception as e:
                        messagebox.showerror("Error", f"Error occurred while insert_to_value_tb01: {str(e)}")
                    # Check if data exists in the database
                    if len(rows) > 0:
                        try:
                            cursor = self.connection.cursor()
                            
                            
                            update_query = f"UPDATE value_tb SET Tools_ID = '{type_id_values[i]}',Expiration_Date = '{expiration_date}', max='{max_values[i][j]}', min='{min_values[i][j]}', iter='{num_loops}' WHERE MIC_Lot='{mic_lot}' AND Tools_Type='{tools_type}' AND no='{no_}'"
                            cursor.execute(update_query)
                            
                            self.connection.commit()
                            cursor.close()
                        except Exception as e:
                            messagebox.showerror("Error", f"Error occurred while insert_to_value_tb02: {str(e)}")
                    else:
                        # If no data exists, insert new data
                        try:
                            cursor = self.connection.cursor()
                            insert_query = f"INSERT INTO value_tb (MIC_Lot, Tools_Type,Tools_ID,Expiration_Date , no, max, min, iter) VALUES ('{mic_lot}', '{tools_type}','{type_id_values[i]}','{expiration_date}', '{no_}', '{max_values[i][j]}', '{min_values[i][j]}', '{num_loops}')"
                            cursor.execute(insert_query)
                            self.connection.commit()
                            cursor.close()
                        except Exception as e:
                            messagebox.showerror("Error", f"Error occurred while insert_to_value_tb03: {str(e)}")
                    for k in range(len(key_name)):
                        try:
                            print(key_name[k]," :: ",key_values[k])
                            cursor = self.connection.cursor()
                            update_query = f"UPDATE value_tb SET [{key_name[k]}] = '{key_values[k]}' WHERE MIC_Lot='{mic_lot}' AND Tools_Type='{tools_type}' AND no='{no_}'"
                            cursor.execute(update_query)
                            self.connection.commit()
                            cursor.close()
                        except Exception as e:
                            messagebox.showerror("Error", f"Error occurred while insert_to_value_tb04: {str(e)}")
                            print("Error", f"Error occurred while insert_to_value_tb04: {str(e)}")
                    # self.connection.commit()
                    # cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while insert_to_value_tb: {str(e)}")
            print("Error", f"Error occurred while insert_to_value_tb: {str(e)}")
    
    def clear_data(self):
        # ล้างข้อมูลทุกช่องข้อมูลในฟอร์ม
        # ล้างข้อมูลทุกช่องข้อมูลในฟอร์ม
        self.max_values = {tool_type: [] for tool_type in self.tools_type}
        self.min_values = {tool_type: [] for tool_type in self.tools_type}
        for tool_type in self.added_type:
            getattr(self, f"{tool_type}_entry").delete(0, tk.END)
            self.max_values[tool_type] = []
            self.min_values[tool_type] = []
            getattr(self, f"{tool_type}_max_min_label").config(text=f" {self.max_values[tool_type]}, {self.min_values[tool_type]}")
            getattr(self, f"{tool_type}_type_combobox").set('')

    
        # ล้างข้อมูลของส่วนอื่น ๆ
        for tool_type in self.added_key_id['specification_key']:
            getattr(self, f"{tool_type}_entry").delete(0, tk.END)

        for tool_type in self.added_key_id['non_specification_key']:
            getattr(self, f"{tool_type}_entry").delete(0, tk.END)
        
        self.add_tools_combobox.set('')
        self.save_var_checkbox.destroy()
        self.save_db_checkbox.destroy()
        self.generate_button.destroy()
        self.folder_button.destroy()
        self.clear_data_button.destroy()
        self.folder_path_label.destroy()

        self.state_ = "normal"
        self.add_footprint()
        # self.create_register_part_page()
        
    def save_file(self, data,img):
        file_name = data + ".png"
        file_path = self.folder_path + "/" + file_name
        img.save(file_path)

