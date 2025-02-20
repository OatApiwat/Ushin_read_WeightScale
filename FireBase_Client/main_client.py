from Firebase_Client import MqttFirebaseBridge

class Server_Firebase:
    def __init__(self):
        #setting
        self.broker_address = "172.16.104.216"
        self.port = 1883
        self.user = "u-shin_user"
        self.password = "123qwe"
        self.Certificate = {
                        "type": "service_account",
                        "project_id": "measurement-u-shin",
                        "private_key_id": "80e93f2aaf0dac52b1d5cfe2784d8c6caa9f8746",
                        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/72/5H4mPEpK6\noqMCSrThTkGCZKa/nI5SJmvnEcu8ydkZifQV834O3dIfmVnXCuFeif2i4HNuHI2u\nrKX8FY+KexNVUgKSJmhoq03/0KhglsSAQGKBNLNodevn1RhoKYU/J+vvSv+mazwc\nYFiPKdplC3tDJXbltNqW795EspwxKpdFZARJo2IKypklzbdVMstSPMGMDVMB3Xf6\nbrEopTeRVNXqbdWqGhkJOx+pkALI64wjARP9V67tiThH48+w23o5dDDTyb5WfEi5\nqYx7hXzb9OtfY4Pkr5yNa013u0VscOn1FXuuH0n0vJQNaSk5K8jIhy4EtFI/Ru1N\nsk6tGmdxAgMBAAECggEAAR//EO72hOFWKbOJjdd+V9Tyl4YQdg5x8berrGmG2xij\n89vj97XXAAz1k4HAYVvQk3wFDN5CysTo26+iPniptPBjpmczOAyD7iaxJ28A1Uz4\nDtbRxVXuC/gh17dI8twLGDLutC1FRbngIyW+/Fr2fTf/yr1aY55f4n2kISKw9SeW\n5NpM65BKXRI0LD0zAolF3kO4DyGi3KaYRnSxXUoS0pb+k6tzBEwwBgVuhM9OAR9s\ntpt8ERqjB5Bzm5YaoIW7pzQnpL7kwdIZotsaNYUNZ/83EUUK9U71bdhAfVvbpJHI\nOxom3M3BhO/ly9IaL76b1nIjmRP8p1xS9htaslb79QKBgQDfMwmw48Tj3v3lCHZP\n5FLTy47j//f7633TB0FfZtsIQIztIs+PjKWsaYtO9lA7BouvAw6aW4SSmgY0mNIB\nXiGDs5v46U3Z8bN34tSfZi9d9zGwgW6gFY/KdQ3dCM4C6xSocaPqqGvg1uoauhiQ\n2yOnKV22hL+SJKynnXnCGcyudwKBgQDcJDeXJYwxShtTat04vA1Vgz7RXHoBkBXz\nWnBJOJaBKhNPDk0tVe/g4T69cbyk9uHXikWXdh+/ye7zM03CX5Vdmjn/RuCJiuVI\nvab8QfVkK6hbBpCghnrOK2lqQpgZZMwA1Hcf2A7CKROdeNGtTYlDt/sMLJR4GXzD\nYyrFklQLVwKBgBvLPjyx0FXT8efwatM+CnZnVc7clCPhylRaBfD8XPAlIadx+0jT\n6dmTdw6JK6p+ASz1A3+DP/oFhhpMoXIcJ64/0n9nhhNKvt+B9po23lUkMCLbq0vy\nA2rhsq1AqG7CmVr0c8YH3Q8tlA9p9x8qusDZLNtKopRvTrS8rmnWTp+3AoGBALM+\nwgzNw9K2Vn2be7kgVXMVRGbP93+iRF07fEYCT3moOsSaDnkligX/IUi7fTCM3OLV\ncUicI8nTsD5RvbTQgxwN4b9bhKQ5deu+kGLBif8gFRrYw5YRKZkJe/HLe3Dhw8HB\nPaWuFIY/T/teTsvfYC7FdSI6gkEv74hgDImGVexNAoGBAMluIOSSPzp8Vb7FD+WD\n84eBvncSDW7/1uW/T5OJDLPVgDZQIKmLUVgYHo5I4QVdZYlWn8vGsIzqdPn5/Hnu\nosH7zAISGXowIGslb3wy7yoLjXOV83tjIK5O1jsVWcj9M6NCBrxaxcQ9z0M7Fb4o\nUSRFjeOk1AgoeMz1eKpF40UQ\n-----END PRIVATE KEY-----\n",
                        "client_email": "firebase-adminsdk-dtjem@measurement-u-shin.iam.gserviceaccount.com",
                        "client_id": "113802573616855996495",
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-dtjem%40measurement-u-shin.iam.gserviceaccount.com",
                        "universe_domain": "googleapis.com"
                        }

        self.cred = 'https://measurement-u-shin-default-rtdb.asia-southeast1.firebasedatabase.app/'
        
        self.tools_type = ["Weight", "Caliper", "PinGate", "Micrometer", "Torque"]
        self.tool_instances = {}

        for tool_type in self.tools_type:
            tool_name = tool_type.lower().replace(" ", "_")  
            self.tool_instances[tool_name] = MqttFirebaseBridge(tool_type, self.broker_address, self.port, self.user, self.password, self.cred, self.Certificate)

if __name__ == "__main__":
    sync_instance = Server_Firebase()