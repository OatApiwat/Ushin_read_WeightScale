import tkinter as tk
from Firebase_Client import MqttFirebaseBridge

class ServerFirebaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Firebase Interface")

        # Set default values
        self.default_broker_address = "192.168.0.238"
        self.default_port = 1883
        self.default_user = "u-shin_user"
        self.default_password = "123qwe"
        self.default_cred = 'https://u-shin01-default-rtdb.asia-southeast1.firebasedatabase.app/'
        self.Certificate = {
            "type": "service_account",
            "project_id": "u-shin01",
            "private_key_id": "bef51851c96bf0d22a67298eeb51d8342b90fbce",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC+tGuv2Jrsymbw\nXozXa+YOzKT37Q+U7EfEJsowg6/OZdl5Zi0lTswzS9kkLnOwmrIAa9Y+czFale9A\nXT+4LDfH4KdsO7LvpV2W0S+4J6mDLoEprAdoJ+2cTIiNwEP/vcMTvASJ4wx1Oivh\nHsdQ63l2+FBDAQH0kT+WHp7ZwrEvow35DeAZ3VXHPAm8WmoXplEPOxNLeXMTgL51\nQMHBh2ZofXJqzk9iT5A5wqfShalGRttNEOPf/4oCQYUmJjmbIkkgCfqPYFYm7WKS\nIMt2C8X3sNRIRITMwbsxogaw1mGl//aTN8E+sALR7xR2J3qyHxX73aGCWko6gN/S\nGASm3SQfAgMBAAECggEABA2UcgrgwlS5w+vDFWRrqwDab5J99EkrkLo8m49aEgpW\nZJ76cqccEsVOw9bzLxKM4xKMOR78e4phX6LSkwINkyftuUdxP4zqLbfSuBirIMQK\nQiTCIBzbaoRpUWntiAtYtS5g8AeR4RGmk2BE8VJ5AGYCo0DHFiWRRUDvojQGhARY\n445VIv8oRFdmP4NLRGHx+QEC6i4fIz9ZdCOlUl5ojnF/f2kj2fGYigFNDjWRaWFw\n3adVuAUCqYyhgQ8MG/GA4sDceknd9/RdaCwNPtbG+I1wxGBQLjk1xKn0SQQe6QvR\n278shjOvN27oMrWYIMueyPDzxxW7qTWVLd4jBUN28QKBgQDegDS4QKLIqdXwGdEd\nk1i/SGVRnruleI3Z3T2kYoca5BLOKE3OuNwfb839/evKJYnfqrlx9sDOIg/OYm/q\nOICeHh9v5m2LjtNdKKcuWjMz801Q9hccKDKjOfKWPmh+2vdCM7Fjf87rNaD4+zOg\n5B83RMLhrzOD0/rygBfaKJVAfQKBgQDbarU28B9usnBjqvhTPtDWtYjx+kUYtaQM\nH/nQYnbNzXOvRynVo3YHrdaWs2dEMsA+9uchXr1f4B0ypZLOi/pQlfGdWm5OigT5\n0CHQdcvYPrUV3Y7SnrytIIntneND/WrKMXBds+sST7f9CnSrGggjnSiwzJ/xSazR\n9QVpWzfVywKBgQCOxYuOs4MA6eHqmFZT+QmYbFb/QbC85Bd5tfpo8gQpoDHk8X3D\n6WDuFysCER5s7xuCVyV52FEttDOaRhX0IF9/lmqrvhuK0pIUFBL6rkxuyG9TRSXd\nHnonvPZJrDAXPmAsrcjkxM08poPtYBtn4RmauFeow2h17d74HnOvvBzRbQKBgDaP\n5XpA4gAb/Vi7hj7lKveJcwGBU7deS+n79Zo9Mf/hbDgVATEwEcS9FNSqzi4mVKoT\nqcwhjAQQbhJPHB+irV9muguAFlgPeEdK223ELSmcBlnmm4KCmLaQldvx3DbnCKw4\n+RFEEVufWUhiVjrKIWYBycGVUNymjoQzYuIdHdhbAoGAd3odJeB+0MZjwBea3vpS\nFkVDRex3eeCkZ23vyB+h5VsnptBpVIeQUvGBd1tG9apvQvTDrCU/sqy7b4pLpAHR\nI344XGBSQt33pXRZcDud8HU4cyYju72DiLLZfEGRzE8tSULWfLHSiLREEVoPpx2D\ndxc4TiKYBd+n6q8hHcQjvQs=\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-73fk2@u-shin01.iam.gserviceaccount.com",
            "client_id": "103734968731056711662",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-73fk2%40u-shin01.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
            }
        # Set up variables for user input
        self.broker_address = tk.StringVar(value=self.default_broker_address)
        self.port = tk.StringVar(value=str(self.default_port))
        self.user = tk.StringVar(value=self.default_user)
        self.password = tk.StringVar(value=self.default_password)
        self.cred = tk.StringVar(value=self.default_cred)

        # Set up GUI components
        self.setup_gui()

    def setup_gui(self):
        # Broker Address
        broker_label = tk.Label(self.root, text="Broker Address:")
        broker_label.grid(row=0, column=0, sticky="w")
        self.broker_entry = tk.Entry(self.root, textvariable=self.broker_address)
        self.broker_entry.grid(row=0, column=1)

        # Port
        port_label = tk.Label(self.root, text="Port:")
        port_label.grid(row=1, column=0, sticky="w")
        self.port_entry = tk.Entry(self.root, textvariable=self.port)
        self.port_entry.grid(row=1, column=1)

        # User
        user_label = tk.Label(self.root, text="User:")
        user_label.grid(row=2, column=0, sticky="w")
        self.user_entry = tk.Entry(self.root, textvariable=self.user)
        self.user_entry.grid(row=2, column=1)

        # Password
        password_label = tk.Label(self.root, text="Password:")
        password_label.grid(row=3, column=0, sticky="w")
        self.password_entry = tk.Entry(self.root, textvariable=self.password)
        self.password_entry.grid(row=3, column=1)

        # Credential
        cred_label = tk.Label(self.root, text="Credential:")
        cred_label.grid(row=4, column=0, sticky="w")
        self.cred_entry = tk.Entry(self.root, textvariable=self.cred)
        self.cred_entry.grid(row=4, column=1)

        # Connect and Disconnect buttons
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect)
        self.connect_button.grid(row=5, column=0, pady=10)

        self.disconnect_button = tk.Button(self.root, text="Disconnect", command=self.disconnect)
        self.disconnect_button.grid(row=5, column=1, pady=10)

        # Status label
        self.status_label = tk.Label(self.root, text="Status: Disconnected")
        self.status_label.grid(row=6, column=0, columnspan=2)

    def connect(self):
        # Get user input values
        broker_address = self.broker_address.get()
        port = int(self.port.get())
        user = self.user.get()
        password = self.password.get()
        cred = self.cred.get()
        Certificate = self.Certificate

        # Create instances of MqttFirebaseBridge with default values
        # Include Certificate as an argument
        self.weight_bridge = MqttFirebaseBridge("Weight", broker_address, port, user, password, cred, Certificate)
        self.caliper_bridge = MqttFirebaseBridge("Caliper", broker_address, port, user, password, cred, Certificate)
        self.pin_gate_bridge = MqttFirebaseBridge("Pin_Gate", broker_address, port, user, password, cred, Certificate)
        self.micro_meter_bridge = MqttFirebaseBridge("Micro_Meter", broker_address, port, user, password, cred, Certificate)

        # Update status label
        self.status_label.config(text="Status: Connected")

        # Disable Connect button after connecting
        self.connect_button.config(state=tk.DISABLED)

    def disconnect(self):
        # Perform disconnection actions here
        # For example, you can set the status label to "Disconnected"
        self.status_label.config(text="Status: Disconnected")

        # Enable the Connect button after disconnecting
        self.connect_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerFirebaseGUI(root)
    root.mainloop()
