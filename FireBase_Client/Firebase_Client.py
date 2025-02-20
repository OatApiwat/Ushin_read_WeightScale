import paho.mqtt.client as mqtt
import firebase_admin
from firebase_admin import credentials, db
import time
import json
from cryptography.fernet import Fernet
import base64
class MqttFirebaseBridge:
    def __init__(self, Type,broker_address,port,user,password,cred,Certificate):
        self.broker_address = broker_address
        self.port = port
        self.client = mqtt.Client()
        # self.client.username_pw_set(username= user, password= password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.Type = Type
        
        self.cred = cred
        self.Certificate = Certificate
        self.firebase_cred = credentials.Certificate(self.Certificate)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(self.firebase_cred, {
                'databaseURL': self.cred
            })
        self.ref_lot_tools_type = db.reference(f'U-shin/{Type}/Lot')
        self.ref_value = db.reference(f'U-shin/{Type}/Value')
        # self.ref_maxmin = db.reference(f'U-shin/{Type}/MaxMin')
        self.ref_status = db.reference(f'U-shin/{Type}/Status')
        
        self.start()
     
    def sent_to_status(self,event):
        try:
            if event.event_type == 'put':
                data__ = event.data
                data_= self.decode(data__)
                if (data_ != " " and data_!= None):
                    print("OK: ",data_)
                    self.client.publish(f'/{self.Type}/Status', data_)
                    time.sleep(1.5)
        except Exception as e:
            print(f"Error handling MQTT: {e}")
            
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
                return decrypted_message
            else:
                print("Error: Input message cannot be None.")
                # return None
        except Exception as e:
            print("Error with decode: ", e)
            # return None


    # Function to update status in Firebase
    def update_ref(self, ref, status):
        if status is not None:
            encode_msg = self.encode(status)
            print("encode_msg: ",type(encode_msg))
            if encode_msg is not None:  # เช็คว่าข้อมูลไม่เป็น None ก่อนที่จะเรียกใช้ set()
                ref.set(encode_msg)
            else:
                print("Error: Encoded message cannot be None.")
        else:
            print("Error: Value must not be None.")

    def connect(self):
        self.client.connect(self.broker_address, self.port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(f'/{self.Type}/Lot')
        self.client.subscribe(f'/{self.Type}/Value')

    
    def on_message(self, client, userdata, message):
        print(message.topic+" "+str(message.payload.decode()))
        if message.topic == f'/{self.Type}/Lot':
            self.update_ref(self.ref_lot_tools_type,json.loads(message.payload.decode()))
            time.sleep(0.5)
            self.update_ref(self.ref_lot_tools_type," ")
        elif message.topic == f'/{self.Type}/Value':
            self.update_ref(self.ref_value,json.loads(message.payload.decode()))
            time.sleep(0.5)
            self.update_ref(self.ref_value," ")
            
       
    
    def start(self):
        self.connect()
        # เริ่มการรับข้อมูล
        self.client.loop_start()
        # self.ref_maxmin.listen(self.sent_to_maxmin)
        self.ref_status.listen(self.sent_to_status)

    def close_connections(self):
        self.disconnect_all()

    def disconnect_all(self):
        try:
            # หยุดการรับข้อมูล
            self.client.loop_stop()
            # ตัดการเชื่อมต่อ MQTT broker
            self.client.disconnect()
            # ตัดการเชื่อมต่อ Firebase
            self.ref_status.unlisten()
            firebase_admin.delete_app(firebase_admin.get_app())
            print("Disconnected from MQTT broker and Firebase")
        except Exception as e:
            print("Error disconnecting: ", e)
