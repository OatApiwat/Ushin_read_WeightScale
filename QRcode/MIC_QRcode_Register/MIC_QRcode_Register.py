import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import qrcode
from PIL import ImageTk, Image

class QRCodeGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.folder_path = None
        self.frist = False
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
        master.title("MIC QR Code Register")

        self.part_no_label = tk.Label(master, text="Part No:")
        self.part_no_label.grid(row=0, column=0, padx=5, pady=5)

        self.part_name_label = tk.Label(master, text="Part Name:")
        self.part_name_label.grid(row=1, column=0, padx=5, pady=5)

        self.model_label = tk.Label(master, text="Model:")
        self.model_label.grid(row=2, column=0, padx=5, pady=5)

        self.weight_label = tk.Label(master, text="Weight:")
        self.weight_label.grid(row=3, column=0, padx=5, pady=5)

        self.caliper_label = tk.Label(master, text="Caliper:")
        self.caliper_label.grid(row=5, column=0, padx=5, pady=5)

        self.pin_gate_label = tk.Label(master, text="Pin Gate:")
        self.pin_gate_label.grid(row=7, column=0, padx=5, pady=5)

        self.micro_meter_label = tk.Label(master, text="Micro Meter:")
        self.micro_meter_label.grid(row=9, column=0, padx=5, pady=5)

        self.part_no_entry = tk.Entry(master)
        self.part_no_entry.grid(row=0, column=1, padx=5, pady=5)

        self.part_name_entry = tk.Entry(master)
        self.part_name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.model_entry = tk.Entry(master)
        self.model_entry.grid(row=2, column=1, padx=5, pady=5)

        self.weight_entry = tk.Entry(master)
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5)

        self.caliper_entry = tk.Entry(master)
        self.caliper_entry.grid(row=5, column=1, padx=5, pady=5)

        self.pin_gate_entry = tk.Entry(master)
        self.pin_gate_entry.grid(row=7, column=1, padx=5, pady=5)

        self.micro_meter_entry = tk.Entry(master)
        self.micro_meter_entry.grid(row=9, column=1, padx=5, pady=5)
    ## for show max min
        self.weight_max_min_label = tk.Label(master, text="[max]:[min] : ")
        self.weight_max_min_label.grid(row=4, column=1,columnspan=3, padx=5, pady=5, sticky="w")

        self.caliper_max_min_label = tk.Label(master, text="[max]:[min] : ")
        self.caliper_max_min_label.grid(row=6, column=1,columnspan=3, padx=5, pady=5, sticky="w")

        self.pin_gate_max_min_label = tk.Label(master, text="[max]:[min] : ")
        self.pin_gate_max_min_label.grid(row=8, column=1,columnspan=3, padx=5, pady=5, sticky="w")

        self.micro_meter_max_min_label = tk.Label(master, text="[max]:[min] : ")
        self.micro_meter_max_min_label.grid(row=10, column=1,columnspan=3, padx=5, pady=5, sticky="w")


        #add max min
        self.add_button_weight = tk.Button(master, text="max, min", command=self.add_max_min_weight)
        self.add_button_weight.grid(row=3, column=2, padx=5, pady=5)

        self.add_button_caliper = tk.Button(master, text="max, min", command=self.add_max_min_caliper)
        self.add_button_caliper.grid(row=5, column=2, padx=5, pady=5)

        self.add_button_pin_gate = tk.Button(master, text="max, min", command=self.add_max_min_pin_gate)
        self.add_button_pin_gate.grid(row=7, column=2, padx=5, pady=5)

        self.add_button_micro_meter = tk.Button(master, text="max, min", command=self.add_max_min_micro_meter)
        self.add_button_micro_meter.grid(row=9, column=2, padx=5, pady=5)

        self.save_var = tk.BooleanVar()
        self.save_checkbox = tk.Checkbutton(master, text="Save to Path", variable=self.save_var)
        self.save_checkbox.grid(row=11, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky="w")

        self.folder_button = tk.Button(master, text="Select Folder to save", command=self.select_folder)
        self.folder_button.grid(row=12, column=0, columnspan=1, padx=5, pady=5)

        self.sent_firebase = tk.BooleanVar(value=True)
        self.save_checkbox = tk.Checkbutton(master, text="Sent to Fire Base", variable=self.sent_firebase)
        self.save_checkbox.grid(row=11, column=1, columnspan=1, rowspan=1, padx=5, pady=5, sticky="w")

        self.folder_button = tk.Button(master, text="Setting Fire Base", command=self.setting_firebase)
        self.folder_button.grid(row=12, column=1, columnspan=1, padx=5, pady=5)

        self.save_db = tk.BooleanVar(value=True)
        self.save_checkbox = tk.Checkbutton(master, text="Save to Data Base", variable=self.save_db)
        self.save_checkbox.grid(row=11, column=2, columnspan=1, rowspan=1, padx=5, pady=5, sticky="w")

        self.folder_button = tk.Button(master, text="Setting Data Base", command=self.setting_database)
        self.folder_button.grid(row=12, column=2, columnspan=1, padx=5, pady=5)

        self.generate_button = tk.Button(master, text="Generate", command=self.generate_qrcode, width=15, height=3, font=("Arial", 12, "bold"))
        self.generate_button.grid(row=11, column=3, rowspan=2, columnspan=2, padx=5, pady=5)


        self.qr_label = tk.Label(master)
        self.qr_label.grid(row=0, column=3, rowspan=10, padx=5, pady=5)
        
        self.folder_path_label = tk.Label(master, text="Folder is not selected!")
        self.folder_path_label.grid(row=13, column=0, columnspan=4, padx=5, pady=5)

        # สร้าง QR code ค่าว่างเมื่อเริ่มโปรแกรม
        self.generate_qrcode()

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.folder_path_label.config(text="Selected Folder: " + self.folder_path)
    
    #for max min
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
        
        max_min_window = tk.Toplevel(self.master)
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


        if (self.frist):
            # ตรวจสอบว่ามีช่องข้อมูลใดที่ว่างอยู่หรือไม่
            if any([not part_no, not part_name, not model, not weight, not caliper, not pin_gate, not micro_meter]):
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return  # หยุดการทำงานของฟังก์ชันหากมีช่องข้อมูลใดที่ว่างอยู่ 
            # เช็คว่าข้อมูลที่กรอกเป็นตัวเลขเท่านั้นหรือไม่
            elif not (weight.isdigit() and caliper.isdigit() and pin_gate.isdigit() and micro_meter.isdigit()):
                messagebox.showwarning("Warning", "Please enter only numbers 0-999 in Weight, Caliper, Pin Gate and Micro Meter")
                return  # หยุดการทำงานของฟังก์ชันหากมีข้อมูลที่ไม่ถูกต้อง
            
            # ตรวจสอบ max_values และ min_values ของ Weight
            if not self.max_values["Weight"] or not self.min_values["Weight"]:
                messagebox.showwarning("Warning", "Please enter both max and min values for Weight.")
                return

            # ตรวจสอบ max_values และ min_values ของ Caliper
            if not self.max_values["Caliper"] or not self.min_values["Caliper"]:
                messagebox.showwarning("Warning", "Please enter both max and min values for Caliper.")
                return

            # ตรวจสอบ max_values และ min_values ของ Pin Gate
            if not self.max_values["Pin Gate"] or not self.min_values["Pin Gate"]:
                messagebox.showwarning("Warning", "Please enter both max and min values for Pin Gate.")
                return

            # ตรวจสอบ max_values และ min_values ของ Micro Meter
            if not self.max_values["Micro Meter"] or not self.min_values["Micro Meter"]:
                messagebox.showwarning("Warning", "Please enter both max and min values for Micro Meter.")
                return


        
        # data = f"Part_no:{part_no},Part_name:{part_name},Model:{model},Weight:{weight},Caliper:{caliper},Pin_Gate:{pin_gate},Micro_meter:{micro_meter}"
        # data = ",".join([part_no, part_name, model, weight, caliper, pin_gate, micro_meter,self.max_values["Weight"],self.min_values["Weight"],self.max_values["Caliper"],self.min_values["Caliper"],self.max_values["Pin Gate"],self.min_values["Pin Gate"],self.max_values["Micro Meter"],self.min_values["Micro Meter"]])
        data = ",".join([
            part_no, 
            part_name, 
            model, 
            weight, 
            caliper, 
            pin_gate, 
            micro_meter,
            "_".join(self.max_values["Weight"]),  
            "_".join(self.min_values["Weight"]),  
            "_".join(self.max_values["Caliper"]),  
            "_".join(self.min_values["Caliper"]),  
            "_".join(self.max_values["Pin Gate"]),  
            "_".join(self.min_values["Pin Gate"]),  
            "_".join(self.max_values["Micro Meter"]),  
            "_".join(self.min_values["Micro Meter"])  
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

        if self.save_var.get():
            file_name = data + ".png"
            file_path = self.folder_path + "/" + file_name
            img.save(file_path)
            messagebox.showinfo("Success", file_name + " has been saved.")
        elif(self.frist):
            messagebox.showinfo("Success", "QR code has been generated.")
        
        img = ImageTk.PhotoImage(img)
        self.qr_label.configure(image=img)
        self.qr_label.image = img
        self.frist = True
    
    def setting_database(self):
        pass
    def setting_firebase(self):
        pass
        
root = tk.Tk()
app = QRCodeGeneratorApp(root)
root.mainloop()
