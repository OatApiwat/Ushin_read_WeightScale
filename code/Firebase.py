import firebase_admin
from firebase_admin import credentials, db
import pyodbc
import time
import json

class FirebaseMSSQLSync:
    def __init__(self):
        # Initialize Firebase app
        self.firebase_cred = credentials.Certificate({
            "type": "service_account",
            "project_id": "u-shin01",
            "private_key_id": "bc519112be65d6498590b54089bdb51764dff986",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDiy5GkwP3dqlrk\noM59kLGpzP1KiUpR8Z9gae+7pPGglhPiMZqPJV3n0mrddmNwwuHNq+8HMO1LeeQi\nQzWDOuknQYyS3pF8mYGKhfJHzjK6XMQ9dcavViwo2cI683wewBYLMvCCLHto6puL\nJstFLtgkyxKXACj6yT5Cpr6vdaWAIMU1J04Ix1q3UNTV1JRkHAsarquFontS9ZxP\ngHWtM3UFmwhZEtoPkyu12YJ0CG/Cg5HUyXMFpZ3YrNqCsNzuRSJY14WamTrzxtrZ\nREc7ejCVF3dgRVK9pNrIc77RxQZrdVNjJ4h/f4OWgfIVgokUojoc/dgGPNLeH6H0\nH/qX12TbAgMBAAECggEAGQ9IUQ2YH4mm0HNqTZqS3wHNDRLdeO97XlJmUHQZ1NYw\nbUJw4xdMaISqFT1zIG8QN0MjvsYrujbGO/j0LUNxpspJ56KbLcricvV4/3ErzsbY\nUjg004PwjjT9jrj/woAUD3m59JBItJ+Tv0zykfrqnCoqLDAy1v8sl33IPSgBOQZw\nocftf6pQaPUTbR994wIAPp/yDV3xO6WhAESgHPabeh34P0LBAOAAtA13Dpv9/Ras\ncoB5f951U7GTARytzYOJsfPIH8AAQkEjgLAw4xEAMmkegw8754E709VSMeJKMAX/\n56ksWpK2POJyJKycs/Ts25kPKwT52uizmPOg/h/FMQKBgQD9yJXR8MKgUpafrOqO\nRcAhM/DPK76ozJ/0xaV2jofcR7VwzQbyF0ZdM4l3SWwXP07W8E1Zz4v4bUaLibfw\nPOiv0EO0PKLKlBMXpOEc9WVb0EahH0L9EOu8YgoSSYW9Nq6yYS71k9ZmHAmW5TbV\nctBHoCHL4anS9XsyQB9uvz8K6wKBgQDkxqR+fpSkgEjbMz1iEZDPB48ekljQyhLR\nEBTst0/BOrVOZWOoWY12W32OH+E1I+RNr0PxLlMD5E5nV01ZAP8liaOHbXpIfOyQ\nUmTpkiUMXNXA6a52vORFg7JNn4JdC4yQ70Rio5NzgOpUU38/upRacFkTyzMlz1ib\nRNAQMbmx0QKBgQDOzc7wpm4jMUnW0pTM3SAErovUdsRGT4EleI4uP1WM9s5vHlRD\noR3QwzeJAkbX5tn7IxUVU6CvD3VGLjK6zRecdW1GiYbq56FrSgu7imlPWTjFAXGY\nQVqoR4gHgOw/1Tik2bbnndI/oSdbVGvLomUBiQchWkIGS85Zk5FJsQTRgwKBgGrb\nSav3zdAER4NzLIGo+L1qp3O9IZTsPdu+qjdi6/KyTEtA2kqhAY098Kg4xcU/bXzH\nl3GIlKfltKVaRruC1qoe3u37ubkv+IL0qUPbykg6+HBx9dZqJik9+UN+dLKnGVH9\nIDD+fHnfxhP7KB2JNZAEl+bB67MGZTmo65IU18pxAoGBAKwjllL5V5nY3rh35xRJ\nSaXOfQ0WnZUVr4p1ZUM+H/1bO7AxN801BM6HXcucgILgRs3qtmhEUQh9bt8f5XUz\nBtu62zKG0ItV+eahzwUw0js5o6iD87KT8YIu7P96vABWE1jqjYsdC8iZKEwltfVO\nVxczxcOYE4o1BuGFfTcYTVCe\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-73fk2@u-shin01.iam.gserviceaccount.com",
            "client_id": "103734968731056711662",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-73fk2%40u-shin01.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
            })
        firebase_admin.initialize_app(self.firebase_cred, {
            'databaseURL': 'https://u-shin01-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })

        # Initialize MSSQL connection
        self.connection = pyodbc.connect('DRIVER={SQL Server};'
                                    'SERVER=127.0.0.1;'
                                    'DATABASE=U-shin_db;'
                                    'UID=sa;'
                                    'PWD=sa@admin;')

        # Firebase Realtime Database references
        self.ref_lot_tools_type = db.reference('U-shin/Register/Lot_Tools_type')
        self.ref_status = db.reference('U-shin/Register/Status')
        self.ref_value = db.reference('U-shin/Register/Value')

        # Listen to changes in Firebase Realtime Database
        self.ref_lot_tools_type.listen(self.handle_change)

    # Function to check if lot exists in MSSQL
    def check_sql_lot(self, data_):
        lot = data_['lot']
        tools_type = data_['tools_type']
        cursor = self.connection.cursor()
        query = f"SELECT * FROM register_value_tb WHERE Lot = '{lot}' AND Tools_Type = '{tools_type}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return len(rows) > 0

    def check_sql_maxmin(self, data_):
        lot = data_['lot']
        tools_type = data_['tools_type']
        cursor = self.connection.cursor()
        query = f"SELECT * FROM register_value_tb WHERE Lot = '{lot}' AND Tools_Type = '{tools_type}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return len(rows) > 0

    # Callback function when there's a change in Firebase Realtime Database
    def handle_change(self, event):
        try:
            if event.event_type == 'put':
                data_ = event.data
                lot = data_['lot']
                tools_type = data_['tools_type']
                if data_.strip():
                    if self.check_sql(data_):
                        self.update_topic(self.ref_lot_tools_type,"OK")
                        time.sleep(0.5)
                        self.update_topic(self.ref_lot_tools_type," ")
                        self.update_topic(self.ref_status," ")
                    else:
                        self.update_topic(self.ref_lot_tools_type,"NG")
                        time.sleep(0.5)
                        self.update_topic(self.ref_lot_tools_type," ")
                        self.update_topic(self.ref_status," ")
        except Exception as e:
            print(f"Error handling Firebase change event: {e}")

    # Function to update status in Firebase
    def update_topic(self,ref, status):
        ref.set(status)

if __name__ == "__main__":
    sync_instance = FirebaseMSSQLSync()

