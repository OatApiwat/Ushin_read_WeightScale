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
        self.caliper_label.grid(row=4, column=0, padx=5, pady=5)

        self.pin_gate_label = tk.Label(master, text="Pin Gate:")
        self.pin_gate_label.grid(row=5, column=0, padx=5, pady=5)

        self.micro_meter_label = tk.Label(master, text="Micro Meter:")
        self.micro_meter_label.grid(row=6, column=0, padx=5, pady=5)

        self.part_no_entry = tk.Entry(master)
        self.part_no_entry.grid(row=0, column=1, padx=5, pady=5)

        self.part_name_entry = tk.Entry(master)
        self.part_name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.model_entry = tk.Entry(master)
        self.model_entry.grid(row=2, column=1, padx=5, pady=5)

        self.weight_entry = tk.Entry(master)
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5)

        self.caliper_entry = tk.Entry(master)
        self.caliper_entry.grid(row=4, column=1, padx=5, pady=5)

        self.pin_gate_entry = tk.Entry(master)
        self.pin_gate_entry.grid(row=5, column=1, padx=5, pady=5)

        self.micro_meter_entry = tk.Entry(master)
        self.micro_meter_entry.grid(row=6, column=1, padx=5, pady=5)

        self.folder_button = tk.Button(master, text="Select Folder to save", command=self.select_folder)
        self.folder_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        

        self.save_var = tk.BooleanVar()
        self.save_checkbox = tk.Checkbutton(master, text="Save QR Code", variable=self.save_var)
        self.save_checkbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        self.generate_button = tk.Button(master, text="Generate", command=self.generate_qrcode)
        self.generate_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        self.qr_label = tk.Label(master)
        self.qr_label.grid(row=0, column=2, rowspan=10, padx=5, pady=5)
        
        self.folder_path_label = tk.Label(master, text="")
        self.folder_path_label.grid(row=10, column=0, columnspan=3, padx=5, pady=5)

        # สร้าง QR code ค่าว่างเมื่อเริ่มโปรแกรม
        self.generate_qrcode()

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.folder_path_label.config(text="Selected Folder: " + self.folder_path)

    def generate_qrcode(self):
        part_no = self.part_no_entry.get()
        part_name = self.part_name_entry.get()
        model = self.model_entry.get()
        weight = self.weight_entry.get()
        caliper = self.caliper_entry.get()
        pin_gate = self.pin_gate_entry.get()
        micro_meter = self.micro_meter_entry.get()
        if (self.frist):
            # ตรวจสอบว่ามีช่องข้อมูลใดที่ว่างอยู่หรือไม่
            if any([not part_no, not part_name, not model, not weight, not caliper, not pin_gate, not micro_meter]):
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return  # หยุดการทำงานของฟังก์ชันหากมีช่องข้อมูลใดที่ว่างอยู่
        self.frist = True
        # data = f"Part_no:{part_no},Part_name:{part_name},Model:{model},Weight:{weight},Caliper:{caliper},Pin_Gate:{pin_gate},Micro_meter:{micro_meter}"
        data = ",".join([part_no, part_name, model, weight, caliper, pin_gate, micro_meter])
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
        img = img.resize((500, 500), Image.LANCZOS)



        if self.save_var.get():
            file_name = ",".join([part_no, part_name, model, weight, caliper, pin_gate, micro_meter]) + ".png"
            file_path = self.folder_path + "/" + file_name
            img.save(file_path)

        img = ImageTk.PhotoImage(img)
        self.qr_label.configure(image=img)
        self.qr_label.image = img

root = tk.Tk()
app = QRCodeGeneratorApp(root)
root.mainloop()
