import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import qrcode
import pyodbc
from PIL import ImageTk, Image
from tkinter import ttk
from tkcalendar import Calendar, DateEntry



class QRCodeGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.folder_path = None
        self.frist = True
        self.state_ = "normal"
        
        self.max_values = {
            "Weight": [],
            "Caliper": [],
            "Pin Gate": [],
            "Micro Meter": []
        }
        self.min_values = {
            "Weight": [],
            "Caliper": [],
            "Pin Gate": [],
            "Micro Meter": []
        }
        
        self.connection = pyodbc.connect('DRIVER={SQL Server};'
                                    'SERVER=127.0.0.1;'
                                    'DATABASE=U-shin_db;'
                                    'UID=sa;'
                                    'PWD=sa@admin;')
        
        # self.notebook = ttk.Notebook(master)
        # self.notebook.pack(fill='both', expand=True)
        
        # self.register_part_frame = ttk.Frame(self.notebook)
        # self.notebook.add(self.register_part_frame, text='Register Part')
        
    def create_register_part_page(self):
        self.part_no_label = tk.Label(self.register_part_frame, text="Part No:", font=("Arial", 10, "bold"))
        self.part_no_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.production_date_label = tk.Label(self.register_part_frame, text="Production Date:", font=("Arial", 10, "bold"))
        self.production_date_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.part_name_label = tk.Label(self.register_part_frame, text="Part Name:", font=("Arial", 10, "bold"))
        self.part_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.model_label = tk.Label(self.register_part_frame, text="Model:", font=("Arial", 10, "bold"))
        self.model_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.weight_label = tk.Label(self.register_part_frame, text="Weight:")
        self.weight_label.grid(row=4, column=0, padx=5, pady=5)

        self.caliper_label = tk.Label(self.register_part_frame, text="Caliper:")
        self.caliper_label.grid(row=6, column=0, padx=5, pady=5)

        self.pin_gate_label = tk.Label(self.register_part_frame, text="Pin Gate:")
        self.pin_gate_label.grid(row=8, column=0, padx=5, pady=5)

        self.micro_meter_label = tk.Label(self.register_part_frame, text="Micro Meter:")
        self.micro_meter_label.grid(row=10, column=0, padx=5, pady=5)
        
        self.part_no_entry = tk.Entry(self.register_part_frame)
        self.part_no_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.calendar_entry = DateEntry(self.register_part_frame, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        self.calendar_entry.delete(0, tk.END)  # ลบค่าทั้งหมดที่มีอยู่ใน DateEntry
        self.calendar_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.part_name_entry = tk.Entry(self.register_part_frame,state=self.state_)
        self.part_name_entry.grid(row=2, column=1, padx=5, pady=5)

        self.model_entry = tk.Entry(self.register_part_frame,state=self.state_)
        self.model_entry.grid(row=3, column=1, padx=5, pady=5)
        
        self.weight_entry = tk.Entry(self.register_part_frame,state=self.state_)
        self.weight_entry.grid(row=4, column=1, padx=5, pady=5)

        self.caliper_entry = tk.Entry(self.register_part_frame,state=self.state_)
        self.caliper_entry.grid(row=6, column=1, padx=5, pady=5)

        self.pin_gate_entry = tk.Entry(self.register_part_frame,state=self.state_)
        self.pin_gate_entry.grid(row=8, column=1, padx=5, pady=5)

        self.micro_meter_entry = tk.Entry(self.register_part_frame,state=self.state_)
        self.micro_meter_entry.grid(row=10, column=1, padx=5, pady=5)
        
        #add button for check part no.
        self.check_part_button = tk.Button(self.register_part_frame, text="Check Part no.", command=self.check_part)
        self.check_part_button.grid(row=0, column=2, rowspan=1, columnspan=1, padx=5, pady=5, sticky="w")
        
        #add button for clear date
        self.clear_date_button = tk.Button(self.register_part_frame, text="Clear date", command=self.clear_date)
        self.clear_date_button.grid(row=1, column=2, rowspan=1, columnspan=1, padx=5, pady=5, sticky="w")
    
    ## for show max min
        self.weight_max_min_label = tk.Label(self.register_part_frame, text="[max]:[min] : ")
        self.weight_max_min_label.grid(row=5, column=1,columnspan=3, padx=5, pady=5, sticky="w")

        self.caliper_max_min_label = tk.Label(self.register_part_frame, text="[max]:[min] : ")
        self.caliper_max_min_label.grid(row=7, column=1,columnspan=3, padx=5, pady=5, sticky="w")

        self.pin_gate_max_min_label = tk.Label(self.register_part_frame, text="[max]:[min] : ")
        self.pin_gate_max_min_label.grid(row=9, column=1,columnspan=3, padx=5, pady=5, sticky="w")

        self.micro_meter_max_min_label = tk.Label(self.register_part_frame, text="[max]:[min] : ")
        self.micro_meter_max_min_label.grid(row=11, column=1,columnspan=3, padx=5, pady=5, sticky="w")

        #add type
        self.populate_combobox("weight", 5)
        self.populate_combobox("caliper", 7)
        self.populate_combobox("pin_gate", 9)
        self.populate_combobox("micro_meter", 11)

        #add max min
        self.add_button_weight = tk.Button(self.register_part_frame, text="max, min", command=self.add_max_min_weight,state=self.state_)
        self.add_button_weight.grid(row=4, column=2, padx=5, pady=5)

        self.add_button_caliper = tk.Button(self.register_part_frame, text="max, min", command=self.add_max_min_caliper,state=self.state_)
        self.add_button_caliper.grid(row=6, column=2, padx=5, pady=5)

        self.add_button_pin_gate = tk.Button(self.register_part_frame, text="max, min", command=self.add_max_min_pin_gate,state=self.state_)
        self.add_button_pin_gate.grid(row=8, column=2, padx=5, pady=5)

        self.add_button_micro_meter = tk.Button(self.register_part_frame, text="max, min", command=self.add_max_min_micro_meter,state=self.state_)
        self.add_button_micro_meter.grid(row=10, column=2, padx=5, pady=5)

        self.save_var = tk.BooleanVar(value=False)
        self.save_checkbox = tk.Checkbutton(self.register_part_frame, text="Save to Path", variable=self.save_var)
        self.save_checkbox.grid(row=12, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky="w")

        self.folder_button = tk.Button(self.register_part_frame, text="Select Folder to save", command=self.select_folder)
        self.folder_button.grid(row=13, column=0, columnspan=2, padx=(5, 2), pady=5, sticky='w')

        self.save_db = tk.BooleanVar(value=True)
        self.save_checkbox = tk.Checkbutton(self.register_part_frame, text="Save to Data Base", variable=self.save_db)
        self.save_checkbox.grid(row=12, column=1, columnspan=2, rowspan=1, padx=5, pady=5, sticky="w")

        self.generate_button = tk.Button(self.register_part_frame, text="Register Part", command=self.generate_qrcode, width=15, height=3, font=("Arial", 12, "bold"))
        self.generate_button.grid(row=10, column=3, rowspan=2, columnspan=3, padx=5, pady=5)
        
        self.clear_data_button = tk.Button(self.register_part_frame, text="Reset data", command=self.clear_data, width=15, height=1, font=("Arial", 9, "bold"))
        self.clear_data_button.grid(row=13, column=3, columnspan=3, padx=5, pady=5)


        self.qr_label = tk.Label(self.register_part_frame)
        self.qr_label.grid(row=0, column=3, rowspan=10, padx=5, pady=5)
        
        self.folder_path_label = tk.Label(self.register_part_frame, text="Folder is not selected!")
        self.folder_path_label.grid(row=14, column=0, columnspan=4, padx=5, pady=5)
        
        if(self.frist):
            self.generate_qrcode()

    def populate_combobox(self, tool_type, row):
        # ดึงข้อมูลจากฐานข้อมูล
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT Tools_ID FROM register_tools_tb WHERE Tools_Type = ?", tool_type)
        tools = [row.Tools_ID for row in cursor.fetchall()]

        # สร้าง Combobox และกำหนดค่า
        setattr(self, f"{tool_type}_type_combobox", ttk.Combobox(self.register_part_frame, values=tools, width=10, state=self.state_))
        getattr(self, f"{tool_type}_type_combobox").grid(row=row, column=0, padx=5, pady=5)

        cursor.close()
        
    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.folder_path_label.config(text="Selected Folder: " + self.folder_path)
    
    def check_part(self):
        part_no = self.part_no_entry.get().upper().replace(" ", "")
        production_date = self.calendar_entry.get()
        part_name = self.part_name_entry.get().upper().replace(" ", "")
        model = self.model_entry.get().upper().replace(" ", "")
        weight = "weight"
        caliper = "caliper"
        pin_gate = "pin_gate"
        micro_meter = "micro_meter"
        lot = "_".join([
            part_no, 
            part_name, 
            model,
            production_date
            ])
        msg_ = False
        if not part_no:
            messagebox.showwarning("Warning", "Please fill in the Part No field.")
            return
        # print(production_date)
        if production_date.strip():
            try:
                cursor_check = self.connection.cursor()
                # SQL query to select data based on PartNo from register_part_tb
                sql_query_vale_part = "SELECT * FROM register_value_tb WHERE PartNo = ? AND ProductionDate = ?"
                cursor_check.execute(sql_query_vale_part, (part_no,production_date))
                row_value_part = cursor_check.fetchone()
                if row_value_part:
                    self.part_name_entry.delete(0, tk.END)
                    self.part_name_entry.insert(0, row_value_part.PartName)
                    msg_=True
                    lot = "_".join([
                        part_no, 
                        row_value_part.PartName, 
                        row_value_part.Model,
                        production_date
                        ])
                else:
                    messagebox.showwarning("Warning", f"Lot: {lot} is not registered.")
                    # self.clear_data()
                    return
                cursor_check.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error occurred while checking the lot: {str(e)}")
        
        try:
            cursor_check = self.connection.cursor()

            # SQL query to select data based on PartNo from register_part_tb
            sql_query_register_part = "SELECT * FROM register_part_tb WHERE PartNo = ?"
            cursor_check.execute(sql_query_register_part, (part_no,))
            row_register_part = cursor_check.fetchone()

            if row_register_part:
                self.model_entry.delete(0, tk.END)
                self.model_entry.insert(0, row_register_part.Model)
                
                self.weight_type_combobox.set(row_register_part.Weight_type)
                self.weight_entry.delete(0, tk.END)
                self.weight_entry.insert(0, row_register_part.Weight_total)

                self.caliper_type_combobox.set(row_register_part.Caliper_type)
                self.caliper_entry.delete(0, tk.END)
                self.caliper_entry.insert(0, row_register_part.Caliper_total)

                self.pin_gate_type_combobox.set(row_register_part.PinGate_type)
                self.pin_gate_entry.delete(0, tk.END)
                self.pin_gate_entry.insert(0, row_register_part.PinGate_total)

                self.micro_meter_type_combobox.set(row_register_part.MicroMeter_type)
                self.micro_meter_entry.delete(0, tk.END)
                self.micro_meter_entry.insert(0, row_register_part.MicroMeter_total)
                
                cursor_check.close()
                # Fetch and populate max/min values for each field
                self.fetch_and_populate_maxmin_values(part_no,weight,caliper,pin_gate,micro_meter)

                if (msg_):
                    messagebox.showinfo("Success", f"Lot: {lot} is registered.")
                else:
                    messagebox.showinfo("Success", f"Part No: {part_no} is registered.")

            else:
                messagebox.showwarning("Warning", f"Part No: {part_no} is not registered.")
                return

        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while checking the part number: {str(e)}")
            
    def fetch_and_populate_maxmin_values(self, part_no,weight,caliper,pin_gate,micro_meter):
        try:
            cursor = self.connection.cursor()

            # Fetch max/min values for weight
            sql_query_weight_maxmin = "SELECT * FROM register_maxmin_tb WHERE PartNo = ? AND Type = ?"
            cursor.execute(sql_query_weight_maxmin, (part_no,weight))
            row_weight_maxmin = cursor.fetchall()
            if row_weight_maxmin:
                # Populate max/min values for weight
                max_values_weight = [str(row.max) for row in row_weight_maxmin]
                min_values_weight = [str(row.min) for row in row_weight_maxmin]
                self.max_values["Weight"] = max_values_weight
                self.min_values["Weight"] = min_values_weight
                self.weight_max_min_label.config(text=f"[max]:[min] : [{', '.join(max_values_weight)}] : [{', '.join(min_values_weight)}]")

            # Fetch max/min values for caliper
            sql_query_weight_maxmin = "SELECT * FROM register_maxmin_tb WHERE PartNo = ? AND Type = ?"
            cursor.execute(sql_query_weight_maxmin, (part_no,caliper))
            row_caliper_maxmin = cursor.fetchall()
            if row_caliper_maxmin:
                # Populate max/min values for caliper
                max_values_caliper = [str(row.max) for row in row_caliper_maxmin]
                min_values_caliper = [str(row.min) for row in row_caliper_maxmin]
                self.max_values["Caliper"] = max_values_caliper
                self.min_values["Caliper"] = min_values_caliper
                self.caliper_max_min_label.config(text=f"[max]:[min] : [{', '.join(max_values_caliper)}] : [{', '.join(min_values_caliper)}]")

            # Fetch max/min values for pin gate
            sql_query_weight_maxmin = "SELECT * FROM register_maxmin_tb WHERE PartNo = ? AND Type = ?"
            cursor.execute(sql_query_weight_maxmin, (part_no,pin_gate))
            row_pin_gate_maxmin = cursor.fetchall()
            if row_pin_gate_maxmin:
                # Populate max/min values for pin gate
                max_values_pin_gate = [str(row.max) for row in row_pin_gate_maxmin]
                min_values_pin_gate = [str(row.min) for row in row_pin_gate_maxmin]
                self.max_values["Pin Gate"] = max_values_pin_gate
                self.min_values["Pin Gate"] = min_values_pin_gate
                self.pin_gate_max_min_label.config(text=f"[max]:[min] : [{', '.join(max_values_pin_gate)}] : [{', '.join(min_values_pin_gate)}]")

            # Fetch max/min values for micro meter
            sql_query_weight_maxmin = "SELECT * FROM register_maxmin_tb WHERE PartNo = ? AND Type = ?"
            cursor.execute(sql_query_weight_maxmin, (part_no,micro_meter))
            row_micro_meter_maxmin = cursor.fetchall()
            if row_micro_meter_maxmin:
                # Populate max/min values for micro meter
                max_values_micro_meter = [str(row.max) for row in row_micro_meter_maxmin]
                min_values_micro_meter = [str(row.min) for row in row_micro_meter_maxmin]
                self.max_values["Micro Meter"] = max_values_micro_meter
                self.min_values["Micro Meter"] = min_values_micro_meter
                self.micro_meter_max_min_label.config(text=f"[max]:[min] : [{', '.join(max_values_micro_meter)}] : [{', '.join(min_values_micro_meter)}]")
            cursor.close()
        except Exception as e:
            print(f"Error occurred while fetching max/min values: {str(e)}")
            messagebox.showerror("Error", f"Error occurred while fetching max/min values: {str(e)}")

    def clear_date(self):
        self.calendar_entry.delete(0, tk.END)  # ลบค่าทั้งหมดที่มีอยู่ใน DateEntry

    def clear_data(self):
        # ล้างข้อมูลทุกช่องข้อมูลในฟอร์ม
        self.part_no_entry.delete(0, tk.END)
        self.calendar_entry.delete(0, tk.END)
        self.part_name_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.caliper_entry.delete(0, tk.END)
        self.pin_gate_entry.delete(0, tk.END)
        self.micro_meter_entry.delete(0, tk.END)
        self.weight_type_combobox.set('')
        self.caliper_type_combobox.set('')
        self.pin_gate_type_combobox.set('')
        self.micro_meter_type_combobox.set('')
        self.weight_max_min_label.config(text="[max]:[min] : ")
        self.caliper_max_min_label.config(text="[max]:[min] : ")
        self.pin_gate_max_min_label.config(text="[max]:[min] : ")
        self.micro_meter_max_min_label.config(text="[max]:[min] : ")
        self.max_values["Weight"]=0
        self.min_values["Weight"]=0
        self.max_values["Caliper"]=0
        self.min_values["Caliper"]=0
        self.max_values["Pin Gate"]=0
        self.min_values["Pin Gate"]=0
        self.max_values["Micro Meter"]=0
        self.min_values["Micro Meter"]=0
        self.state_ = "normal"
        self.create_register_part_page()

    def add_max_min_weight(self):
        self.open_max_min_window("Weight")

    def add_max_min_caliper(self):
        self.open_max_min_window("Caliper")

    def add_max_min_pin_gate(self):
        self.open_max_min_window("Pin Gate")

    def add_max_min_micro_meter(self):
        self.open_max_min_window("Micro Meter")

    def open_max_min_window(self, field):
        num_entries = int(self.weight_entry.get()) if field == "Weight" else \
                    int(self.caliper_entry.get()) if field == "Caliper" else \
                    int(self.pin_gate_entry.get()) if field == "Pin Gate" else \
                    int(self.micro_meter_entry.get())
        
        max_min_window = tk.Toplevel(self.register_part_frame)
        max_min_window.title(f"Enter Max, Min for {field}")

        entries = []
        for i in range(num_entries):
            label_max = tk.Label(max_min_window, text=f"Max {i+1}:")
            label_max.grid(row=i, column=0, padx=5, pady=5)

            label_min = tk.Label(max_min_window, text=f"Min {i+1}:")
            label_min.grid(row=i, column=2, padx=5, pady=5)

            entry_max = tk.Entry(max_min_window)
            entry_max.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry_max)

            entry_min = tk.Entry(max_min_window)
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
            if field == "Weight":
                self.max_values["Weight"] = max_values
                self.min_values["Weight"] = min_values
                self.weight_max_min_label.config(text=f"[max]:[min] : {max_values}, {min_values}")
            elif field == "Caliper":
                self.max_values["Caliper"] = max_values
                self.min_values["Caliper"] = min_values
                self.caliper_max_min_label.config(text=f"[max]:[min] : {max_values}, {min_values}")
            elif field == "Pin Gate":
                self.max_values["Pin Gate"] = max_values
                self.min_values["Pin Gate"] = min_values
                self.pin_gate_max_min_label.config(text=f"[max]:[min] : {max_values}, {min_values}")
            elif field == "Micro Meter":
                self.max_values["Micro Meter"] = max_values
                self.min_values["Micro Meter"] = min_values
                self.micro_meter_max_min_label.config(text=f"[max]:[min] : {max_values}, {min_values}")
        
            # Do something with max_values and min_values
            # messagebox.showinfo("Info", f"Max values: {max_values}, Min values: {min_values} for {field}")
            max_min_window.destroy()

        submit_button = tk.Button(max_min_window, text="Submit", command=on_submit)
        submit_button.grid(row=num_entries, column=0, columnspan=4, padx=5, pady=5)

    #for QR code
    def generate_qrcode(self):
        part_no = self.part_no_entry.get().upper().replace(" ", "")
        part_name = self.part_name_entry.get().upper().replace(" ", "")
        model = self.model_entry.get().upper().replace(" ", "")
        weight = self.weight_entry.get().upper().replace(" ", "")
        caliper = self.caliper_entry.get().upper().replace(" ", "")
        pin_gate = self.pin_gate_entry.get().upper().replace(" ", "")
        micro_meter = self.micro_meter_entry.get().upper().replace(" ", "")
        
        # เพิ่มการดึงค่าที่เลือกจาก comboboxes
        weight_type = self.weight_type_combobox.get()
        caliper_type = self.caliper_type_combobox.get()
        pin_gate_type = self.pin_gate_type_combobox.get()
        micro_meter_type = self.micro_meter_type_combobox.get()
        
        production_date = self.calendar_entry.get()


        if (not self.frist):
            # ตรวจสอบว่ามีช่องข้อมูลใดที่ว่างอยู่หรือไม่
            if any([not part_no, not part_name, not model, not weight, not caliper, not pin_gate, not micro_meter,not production_date]):
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return  # หยุดการทำงานของฟังก์ชันหากมีช่องข้อมูลใดที่ว่างอยู่ 
            elif (int(weight) > 0 and not weight_type):
                messagebox.showwarning("Warning", "Please fill in weight type.")
                return  # หยุดการทำงานของฟังก์ชันหากมีช่องข้อมูลใดที่ว่างอยู่ 
            elif (int(caliper) > 0 and not caliper_type):
                messagebox.showwarning("Warning", "Please fill in caliper type.")
                return  # หยุดการทำงานของฟังก์ชันหากมีช่องข้อมูลใดที่ว่างอยู่ 
            elif (int(pin_gate) > 0 and not pin_gate_type):
                messagebox.showwarning("Warning", "Please fill in pin gate type.")
                return  # หยุดการทำงานของฟังก์ชันหากมีช่องข้อมูลใดที่ว่างอยู่ 
            elif (int(micro_meter) > 0 and not micro_meter_type):
                messagebox.showwarning("Warning", "Please fill in micro meter type.")
                return  # หยุดการทำงานของฟังก์ชันหากมีช่องข้อมูลใดที่ว่างอยู่ 
                
            # เช็คว่าข้อมูลที่กรอกเป็นตัวเลขเท่านั้นหรือไม่
            elif not (weight.isdigit() and caliper.isdigit() and pin_gate.isdigit() and micro_meter.isdigit()) or not all(value.isdigit() and int(value) >= 0 for value in [weight, caliper, pin_gate, micro_meter]):
                messagebox.showwarning("Warning", "Please enter non-negative integers in Weight, Caliper, Pin Gate and Micro Meter")
                return  # หยุดการทำงานของฟังก์ชันหากมีข้อมูลที่ไม่ถูกต้อง

            
            # ตรวจสอบ max_values และ min_values ของ Weight
            if (not self.max_values["Weight"] or not self.min_values["Weight"]) and (float(weight) != 0):
                messagebox.showwarning("Warning", "Please enter both max and min values for Weight.")
                return

            # ตรวจสอบ max_values และ min_values ของ Caliper
            if (not self.max_values["Caliper"] or not self.min_values["Caliper"]) and (float(caliper) != 0):
                print(caliper)
                messagebox.showwarning("Warning", "Please enter both max and min values for Caliper.")
                return

            # ตรวจสอบ max_values และ min_values ของ Pin Gate
            if (not self.max_values["Pin Gate"] or not self.min_values["Pin Gate"]) and (float(pin_gate) != 0):
                messagebox.showwarning("Warning", "Please enter both max and min values for Pin Gate.")
                return

            # ตรวจสอบ max_values และ min_values ของ Micro Meter
            if (not self.max_values["Micro Meter"] or not self.min_values["Micro Meter"]) and (float(micro_meter) !=0):
                messagebox.showwarning("Warning", "Please enter both max and min values for Micro Meter.")
                return


        
        lot = "_".join([
            part_no, 
            part_name, 
            model,
            production_date
            ])
        data = ",".join([
            part_no, 
            part_name, 
            model,
            weight, 
            caliper, 
            pin_gate, 
            micro_meter,
            "_".join([str(self.max_values["Weight"])]),
            "_".join([str(self.min_values["Weight"])]),
            "_".join([str(self.max_values["Caliper"])]),
            "_".join([str(self.min_values["Caliper"])]),
            "_".join([str(self.max_values["Pin Gate"])]),
            "_".join([str(self.min_values["Pin Gate"])]),
            "_".join([str(self.max_values["Micro Meter"])]),
            "_".join([str(self.min_values["Micro Meter"])])

        ])

        if self.save_var.get():
            if not self.folder_path:  # ตรวจสอบว่ายังไม่ได้เลือกที่เก็บ
                messagebox.showwarning("Warning", "Please select a folder to save the QR Code.")
                return  # หยุดการทำงานของฟังก์ชั่นหากยังไม่ได้เลือกที่เก็บ
        


        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((300, 300), Image.LANCZOS)

        data_to_insert = (part_no, model, weight_type, weight, caliper_type, caliper, pin_gate_type, pin_gate, micro_meter_type, micro_meter)
        
        if (not self.frist):
            if self.save_var.get() and self.save_db.get():
                self.save_file(data,img)
                self.insert_register_into_database(data_to_insert)
                # Call the method to insert Weight max and min values into the database
                self.insert_max_min_into_database(part_no,"weight", self.max_values["Weight"], self.min_values["Weight"])
                self.insert_max_min_into_database(part_no,"caliper", self.max_values["Caliper"], self.min_values["Caliper"])
                self.insert_max_min_into_database(part_no,"pin_gate", self.max_values["Pin Gate"], self.min_values["Pin Gate"])
                self.insert_max_min_into_database(part_no,"micro_meter", self.max_values["Micro Meter"], self.min_values["Micro Meter"])
                self.insert_lot_into_database(part_no,part_name,model,production_date,lot,"weight", self.max_values["Weight"], self.min_values["Weight"])
                self.insert_lot_into_database(part_no,part_name,model,production_date,lot,"caliper", self.max_values["Caliper"], self.min_values["Caliper"])
                self.insert_lot_into_database(part_no,part_name,model,production_date,lot,"pin_gate", self.max_values["Pin Gate"], self.min_values["Pin Gate"])
                self.insert_lot_into_database(part_no,part_name,model,production_date,lot,"micro_meter", self.max_values["Micro Meter"], self.min_values["Micro Meter"])
                messagebox.showinfo("Success", "Data has been saved to the database and file path.")
            elif self.save_db.get():
                self.insert_register_into_database(data_to_insert)
                # Call the method to insert Weight max and min values into the database
                self.insert_max_min_into_database(part_no,"weight", self.max_values["Weight"], self.min_values["Weight"])
                self.insert_max_min_into_database(part_no,"caliper", self.max_values["Caliper"], self.min_values["Caliper"])
                self.insert_max_min_into_database(part_no,"pin_gate", self.max_values["Pin Gate"], self.min_values["Pin Gate"])
                self.insert_max_min_into_database(part_no,"micro_meter", self.max_values["Micro Meter"], self.min_values["Micro Meter"])
                self.insert_lot_into_database(part_no,part_name,model,production_date,lot,"weight", self.max_values["Weight"], self.min_values["Weight"])
                self.insert_lot_into_database(part_no,part_name,model,production_date,lot,"caliper", self.max_values["Caliper"], self.min_values["Caliper"])
                self.insert_lot_into_database(part_no,part_name,model,production_date,lot,"pin_gate", self.max_values["Pin Gate"], self.min_values["Pin Gate"])
                self.insert_lot_into_database(part_no,part_name,model,production_date,lot,"micro_meter", self.max_values["Micro Meter"], self.min_values["Micro Meter"])
                messagebox.showinfo("Success", "Data has been saved to the database.")
            elif self.save_var.get():
                self.save_file(data,img)
                messagebox.showinfo("Success", "Data has been saved to file path.")
            else:
                messagebox.showinfo("Success", "QR code has been generated.")
        
        img = ImageTk.PhotoImage(img)
        self.qr_label.configure(image=img)
        self.qr_label.image = img
        self.frist = False
        # self.clear_data()
    
    def insert_register_into_database(self, data):
        try:
            cursor = self.connection.cursor()

            # Define your SQL query to insert or replace data into the database based on Lot column
            # sql_query = "INSERT INTO register_tb (Lot,PartNo, PartName, Model, Weight, Caliper, PinGate, MicroMeter) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            sql_query = """
                        MERGE INTO register_part_tb AS target
                        USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source (PartNo, Model, Weight_type, Weight_total, Caliper_type, Caliper_total, PinGate_type, PinGate_total, MicroMeter_type, MicroMeter_total)
                        ON target.PartNo = source.PartNo
                        WHEN MATCHED THEN
                            UPDATE SET
                                target.Model = source.Model,
                                target.Weight_type = source.Weight_type,
                                target.Weight_total = source.Weight_total,
                                target.Caliper_type = source.Caliper_type,
                                target.Caliper_total = source.Caliper_total,
                                target.PinGate_type = source.PinGate_type,
                                target.PinGate_total = source.PinGate_total,
                                target.MicroMeter_type = source.MicroMeter_type,
                                target.MicroMeter_total = source.MicroMeter_total
                        WHEN NOT MATCHED THEN
                            INSERT (PartNo, Model, Weight_type, Weight_total, Caliper_type, Caliper_total, PinGate_type, PinGate_total, MicroMeter_type, MicroMeter_total)
                            VALUES (source.PartNo, source.Model, source.Weight_type, source.Weight_total, source.Caliper_type, source.Caliper_total, source.PinGate_type,source.PinGate_total, source.MicroMeter_type, source.MicroMeter_total);
                    """
            # Execute the SQL query with the data
            cursor.execute(sql_query, data)

            # Commit the transaction
            self.connection.commit()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while saving data to the database: {str(e)}")
            print("Error", f"Error occurred while saving data to the database: {str(e)}")
            
    def insert_max_min_into_database(self,part_no,field_name, max_values, min_values):
        iter_ = getattr(self, f"{field_name}_entry").get().upper().replace(" ", "")
        if (int(iter_)>0):
            try:
                cursor = self.connection.cursor()

                # Loop through max_values and min_values lists to insert each pair into the database
                for i, (max_val, min_val) in enumerate(zip(max_values, min_values), start=1):
                        sql_query = f"""
                                    MERGE INTO register_maxmin_tb AS target
                                    USING (VALUES (?, ?, ?, ?, ?, ?)) AS source (PartNo,Type, [no], [max], [min],[iter])
                                    ON target.PartNo = source.Partno AND target.[no] = source.[no] AND target.Type = source.Type
                                    WHEN MATCHED THEN
                                        UPDATE SET
                                            target.[max] = source.[max],
                                            target.[min] = source.[min],
                                            target.[iter] = source.[iter],
                                            target.PartNo = source.PartNo
                                    WHEN NOT MATCHED THEN
                                        INSERT (PartNo,Type, [no], [max], [min], [iter])
                                        VALUES (source.PartNo,source.Type, source.[no], source.[max], source.[min], source.[iter]);
                                """
                        # Execute the SQL query with the data
                        cursor.execute(sql_query, (part_no,field_name, i, max_val, min_val, iter_))

                        # Commit the transaction
                        self.connection.commit()
                cursor.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error occurred while saving {field_name} max and min data to the database: {str(e)}")
                print("Error", f"Error occurred while saving {field_name} max and min data to the database: {str(e)}")

    def insert_lot_into_database(self, part_no, part_name, model, production_date, lot, field_name, max_values, min_values):
        iter_ = getattr(self, f"{field_name}_entry").get().upper().replace(" ", "")
        if int(iter_) > 0:
            try:
                cursor = self.connection.cursor()

                # Query to fetch Tools_ID and Expiration_Date from register_tools_tb based on Tools_Type
                tools_query = """
                            SELECT Tools_ID, Expiration_Date
                            FROM register_tools_tb
                            WHERE Tools_Type = ?
                            """
                cursor.execute(tools_query, (field_name,))
                tools_data = cursor.fetchone()  # Fetches the first row

                if tools_data:  # If data is fetched successfully
                    tools_id, expiration_date = tools_data

                    # Loop through max_values and min_values lists to insert or update each pair into the database
                    for i, (max_val, min_val) in enumerate(zip(max_values, min_values), start=1):
                        sql_query = """
                                    MERGE INTO register_value_tb AS target
                                    USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source (
                                        PartNo, PartName, Model, ProductionDate, Lot, Tools_Type, Tools_ID,
                                        Expiration_Date, Iter, No, Max, Min
                                    )
                                    ON target.PartNo = source.PartNo AND target.No = source.No 
                                        AND target.Tools_Type = source.Tools_Type AND target.Lot = source.Lot
                                    WHEN MATCHED THEN
                                        UPDATE SET
                                            target.Max = source.Max,
                                            target.Min = source.Min,
                                            target.Iter = source.Iter,
                                            target.Tools_ID = source.Tools_ID,
                                            target.Expiration_Date = source.Expiration_Date
                                    WHEN NOT MATCHED THEN
                                        INSERT (
                                            PartNo, PartName, Model, ProductionDate, Lot, Tools_Type, Tools_ID,
                                            Expiration_Date, Iter, No, Max, Min
                                        )
                                        VALUES (
                                            source.PartNo, source.PartName, source.Model, source.ProductionDate,
                                            source.Lot, source.Tools_Type, source.Tools_ID, source.Expiration_Date,
                                            source.Iter, source.No, source.Max, source.Min
                                        );
                                    """
                        # Execute the SQL query with the data
                        cursor.execute(sql_query, (
                            part_no, part_name, model, production_date, lot, field_name, tools_id, expiration_date,
                            int(iter_), i, float(max_val), float(min_val)
                        ))

                # Commit the transaction
                self.connection.commit()
                cursor.close()

            except Exception as e:
                print("Error", f"An error occurred while saving {field_name} and lot data to the database: {str(e)}")
                messagebox.showerror("Error", f"An error occurred while saving {field_name} and lot data to the database: {str(e)}")


    def save_file(self, data,img):
        file_name = data + ".png"
        file_path = self.folder_path + "/" + file_name
        img.save(file_path)