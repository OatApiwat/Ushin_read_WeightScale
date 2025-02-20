import firebase_admin
from firebase_admin import credentials, db
import pyodbc
import time
import json
from datetime import datetime
from tkinter import messagebox
from cryptography.fernet import Fernet
import base64

class FirebaseMSSQLSync:
    def __init__(self,Type,Certificate,firebase_cred,sql_connect):

        # Initialize Firebase app
        self.firebase_cred = credentials.Certificate(Certificate)

        # Initialize MSSQL connection
        self.connection = pyodbc.connect(sql_connect)

        # Firebase Realtime Database references
        if not firebase_admin._apps:
            firebase_admin.initialize_app(self.firebase_cred, {
                'databaseURL': firebase_cred
            })
        self.ref_lot_tools_type = db.reference(f'U-shin/{Type}/Lot')
        self.ref_status = db.reference(f'U-shin/{Type}/Status')
        self.ref_value = db.reference(f'U-shin/{Type}/Value')

        # Listen to changes in Firebase Realtime Database
        self.ref_lot_tools_type.listen(self.lot_change)
        self.ref_value.listen(self.save_sql)

    def save_sql(self, event):
        try:
            if event.event_type == 'put':
                data__ = event.data
                data_= self.decode(data__)
                print(data_)
                if (data_ != " " and data_!= None):
                    lot = data_['lot']
                    tools_type = data_['tools_type']
                    value = data_['value']
                    judge = data_['judge']
                    no = data_['no']
                    health_tools = data_['health_tools']
                    
                    current_time = datetime.now().time()
                    if datetime.strptime("07:10:00", "%H:%M:%S").time() <= current_time <= datetime.strptime("15:10:00", "%H:%M:%S").time():
                        shift = "A"
                    elif datetime.strptime("15:10:00", "%H:%M:%S").time() < current_time <= datetime.strptime("23:10:00", "%H:%M:%S").time():
                        shift = "B"
                    else:
                        shift = "C"

                    cursor = self.connection.cursor()
                    current_time = datetime.now().time().strftime('%H:%M:%S')
                    cursor.execute("SELECT COUNT(*) FROM value_tb WHERE MIC_Lot = ? AND Tools_Type = ?", (lot, tools_type))
                    count = cursor.fetchone()[0]

                    if count > 0:
                        sql_query = """
                                    UPDATE value_tb
                                    SET  Date = ?,Time =?, Value = ?, Judge = ?, Shift = ?,[health tools] = ?
                                    WHERE MIC_Lot = ? AND Tools_Type = ? AND no = ?
                                    """
                        
                        cursor.execute(sql_query,(datetime.now().strftime("%Y-%m-%d"),current_time,value, judge,shift,health_tools, lot, tools_type,no))
                        self.connection.commit()
                        cursor.close()
                    # Check data in sql
                    time.sleep(0.2)
                    cursor = self.connection.cursor()
                    cursor.execute("SELECT COUNT(*) FROM value_tb WHERE MIC_Lot = ? AND Tools_Type = ? AND Value = ?", (lot, tools_type,value))
                    count = cursor.fetchone()[0]
                    if count > 0:
                        self.update_ref(self.ref_status, "OK")
                        time.sleep(0.5)
                        self.update_ref(self.ref_status, " ")
                    else:
                        self.update_ref(self.ref_status, "NG")
                        time.sleep(0.5)
                        self.update_ref(self.ref_status, " ")
                        
        except Exception as e:
            # messagebox.showerror("Error", f"Error occurred while saving value to the database: {str(e)}")
            print("Error", f"Error occurred while saving data to the database: {str(e)}")

    
    # Function to check if lot exists in MSSQL
    def check_sql(self, data_):
        lot = data_['lot']
        tools_type = data_['tools_type']
        cursor = self.connection.cursor()
        query = f"SELECT * FROM value_tb WHERE MIC_Lot = '{lot}' AND Tools_Type = '{tools_type}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        current_date = datetime.now().strftime("%Y-%m-%d")
        json_array = []
        print("len rows: ",len(rows))
        if len(rows) != 0:
            status = "OK"
        else:
            status = "NG"
            row_dict = {
                'lot': '',
                'tools_type': '',
                'tools_id': '',
                'health_tools': '',
                'max': '',
                'min': '',
                'no':'',
                'iter':'',
                'status': status
            }
            json_array.append(row_dict)
        for row in rows:
            date_string = row.Expiration_Date
            date_format = "%d-%m-%Y"
            date = datetime.strptime(date_string, date_format).strftime("%Y-%m-%d")
            print("date: ",date)
            print("current_date: ",current_date)
            if current_date <= date:
                health_tools = "OK"
            else:
                health_tools = "NG"
            print("health_tools",health_tools)
            row_dict = {
                'lot': row.MIC_Lot,
                'tools_type': row.Tools_Type,
                'tools_id': row.Tools_ID,
                'health_tools': health_tools,
                'max': row.max,
                'min': row.min,
                'no':row.no,
                'iter':row.iter,
                'status': status
            }
            json_array.append(row_dict)
        
        return json.dumps(json_array)



    def lot_change(self, event):
        try:
            if event.event_type == 'put':
                data__ = event.data
                print("data__: ",data__)
                data_= self.decode(data__)
                print("data_: ",data_)
                if (data_ != " " and data_!= None):
                    lot = data_['lot']
                    tools_type = data_['tools_type']
                    maxmin = self.check_sql(data_)
                    if  maxmin != json.dumps([]):
                        print("Lot: ",lot," Tools type: ",tools_type," is OK!")
                    else:
                        print("Lot: ",lot," Tools type: ",tools_type," is NG!")
                    self.update_ref(self.ref_status, maxmin)
                    time.sleep(0.5)
                    self.update_ref(self.ref_lot_tools_type, " ")
                    self.update_ref(self.ref_status, " ")
        except Exception as e:
            print(f"Error handling Firebase change event: {e}")


    # Function to update status in Firebase
    def update_ref(self,ref, status):
        encode_msg = self.encode(status)
        ref.set(encode_msg)
        
        
    def encode(self, msg):
        try:
            print("msg is: ",msg)
            print("type: ",type(msg))
            if msg is not None:  # ตรวจสอบว่าข้อมูลไม่เป็น None
                key = "reerthyjtrethjytrethjytrewrdjtyr"
                # message = json.dumps(msg).encode()  # แปลงเป็น JSON ก่อนเข้ารหัส
                message =msg
                # print("message: ",message)
                encrypted_message = self.encrypt_message(key, message)
                # print("encrypted_message",encrypted_message)
                return encrypted_message.decode('utf-8')
            else:
                print("Error: Input message cannot be None.")
                # return None
        except Exception as e:
            print("Error with encode: ", e)
            # return None
        
    def encrypt_message(self,key, message):
        json_message = json.dumps(message).encode()
        cipher_suite = Fernet(base64.urlsafe_b64encode(key.encode()))
        return cipher_suite.encrypt(json_message)

    def decrypt_message(self,key, encrypted_message):
        cipher_suite = Fernet(base64.urlsafe_b64encode(key.encode()))
        decrypted_message = cipher_suite.decrypt(encrypted_message)
        # ถอดรหัสข้อความและแปลงเป็น JSON ก่อนการคืนค่า
        return json.loads(decrypted_message)
    
    def decode(self, msg):
        try:
            if msg is not None:  # ตรวจสอบว่าข้อมูลไม่เป็น None
                key = "reerthyjtrethjytrethjytrewrdjtyr"
                decrypted_message = self.decrypt_message(key, msg)
                print("decrypted_message: ",decrypted_message)
                # json_string = decrypted_message.decode()  # แปลงกลับเป็นสตริงจากไบต์ก่อนถอดรหัส
                return decrypted_message
                # return json.loads(json_string)  # แปลงเป็นพจนานุกรม
            else:
                print("Error: Input message cannot be None.")
                # return None
        except Exception as e:
            print("Error with decode: ", e)
            # return None
    def close_connections(self):
        self.disconnect_all()

    def disconnect_all(self):
        try:
            # หยุดการรับข้อมูลจาก Firebase
            self.ref_lot_tools_type.unlisten()
            self.ref_value.unlisten()
            
            # ปิดการเชื่อมต่อ Firebase
            firebase_admin.delete_app(firebase_admin.get_app())
            print("Disconnected from Firebase")

            # ปิดการเชื่อมต่อ MSSQL
            self.connection.close()
            print("Disconnected from MSSQL")
        except Exception as e:
            print("Error disconnecting: ", e)



