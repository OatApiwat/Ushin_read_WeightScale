import qrcode
import os

def save_qrcode_to_folder(input1, input2, input3, input4, folder_path):
    # รวม inputs เข้าไปด้วยการใช้ , คั่น
    data = ','.join([input1, input2, input3, input4])
    
    # สร้าง QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # สร้างรูปภาพ QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # สร้าง path สำหรับ save ไฟล์ QR code
    file_path = os.path.join(folder_path, data + ".png")

    # Save รูปภาพ QR code ลงไฟล์
    img.save(file_path)

# เรียกใช้งานฟังก์ชัน
input1 = "value1"
input2 = "value2"
input3 = "value3"
input4 = "value4"
folder_path = "D:/My Documents/IoT_Project/Uchin/QRcode/collect"  # ระบุ path ของ folder ที่ต้องการ save ไฟล์ QR code

save_qrcode_to_folder(input1, input2, input3, input4, folder_path)
