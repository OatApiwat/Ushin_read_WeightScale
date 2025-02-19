import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def initialize_firebase():
    """เริ่มต้นใช้งาน Firebase"""
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "u-shin01",
        "private_key_id": "409c87f6d52fef1e934947bba1b8c40d6a0d386f",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEugIBADANBgkqhkiG9w0BAQEFAASCBKQwggSgAgEAAoIBAQCI9VbnIooJDzWg\numYEo3r94JJVu1MDfH6c/jiG8/0FU0qbtluFby91EZNposCxwFRkOvV6gAJNbHK5\nCfIj1jKpRqpQm+adJXrVDolj9n87dLVswT4U73U4Rsz6wZMJou0wzLZwWP0bm1xE\nI4jGsIpBMtpK6PsBhnSwOz8cCv7YeM9pWbsi+0IMyLDevsFTmUNs6yi+51DWAQD4\naik0tT7eDwvYaiUmqTnrRqHn4ei8Q5LneGJ1N/XmZXiek9LJAs1aKXKMPyXn7Mfm\nzuxG2QSywZB8+8OEzseJme34rjdQwjGlo3JGDYnGVUJ+1Zwq4CON7Hjwr030eORH\nKjSy+5JtAgMBAAECgf9/U5d3SqUJxxoUUzaFGXc+j4l8KqsCkrsjOTVUQYD5cnXq\nTZ7IbpWwQKbLjoOWvTe39xhAysFZOXlujdCPgJOYzBmK12WOs0l+ygTw6jlfDSGd\n+gm9bOGNcEUg2tXYH6Bjve3ehNzKzaT5tA90qKvf8WcAPZkd0eKp9Gq3p4FFva7s\nyHhXIG1zlYz93ua0W5ydUxhsEcf8GUjuGuUsW2jebmSE9ffFD5XRxvqWPnxR8+mi\nJd4T9HkAWLQ9krkpwb01r9GEtiTq4pfj6+hABJHflGLUYYyn/hDQgHQkwwYaacVc\nchgcx5U6iHKfhxXMNi81aCNYPk4Vzn2Mfqj0s4kCgYEAu2dI7KrgRtClBAfX6ECu\n4MPtgdEDoSP2ZCl+HcEuwB/NHfSm58Dt+cNwS1TXDRWgTs8np1glZH0XAG+fl266\nvR0w+PgNbwTCmHICb4Q0bz3XPcDHG2pv2wU/Fzkc+iiUudZxDbU49SA8AeF6ZENL\nvwsnbbFzlsygf6R3ZkGEvl8CgYEAuxcTm8giwq4kv5TVwMqR1+75qVpZyXPItYRI\nvKGBkMkvXLuVig6TEghBCuN5kea0OcinUXV3FcLHQcU+fT/zMZ5lFVMWHGVI1ETq\n0qBNpsinWuZn4RJCLlaRaFb/2US/4518HyAGYykzamVzMi0tJr9x2PWuG+lWssY1\nzwi9SrMCgYBU4DiFB/c/22uBYdQFmpYZsmM1cmbEardDMg+uhjoYRc7ujEmzmQuv\nHTcUxz4G7Q6H4wbAogl9c7IhPmz3du0YjcoKWL4s0+kWhjxYKXZeE5ISo+cJobE7\nbyrd574aBpsld9wIK1W6n3jOGUMHefsqcXDQG5iQaekfJmv1YiMu3QKBgCE3s6+R\nFTrjmHq7fkhAryxbrdA3zoFKIXS5DAER2+NNFS+tzps4gzxMYuAAC3GwOIeZ7Ls1\n0/L1JlOzJakvVYqVyPTET8Sy5v9pTRgghij6r1wgVIlNqJp5nE+eQsbcwgUzzPnp\nwbiRdCOL56wdAUtD6n7PAB7MiywqrRsZPiKpAoGAXfvoqXo5mF6JXLoJjLcPISiO\nttvVjGpagrx25oVMH5b9TduKdHKqMZjSSAVtAWpAzcFeqp9XHcx7St0CXOZiabMY\n58tglz/a/UkyUkDNA7qFnDI3QSmV/03mOgCcF8MeEo7ZZ1FPd10BD4/kVJ6P566l\nOn9q6sLyucoCTEHcawQ=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-73fk2@u-shin01.iam.gserviceaccount.com",
        "client_id": "103734968731056711662",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-73fk2%40u-shin01.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    })
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://u-shin01-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

def send_data_to_firebase(data):
    """ส่งข้อมูลไปยัง Firebase Realtime Database"""
    ref = db.reference('/test')
    ref.push(data)

def main():
    # เริ่มต้นใช้งาน Firebase
    initialize_firebase()

    # ข้อมูลที่ต้องการส่งไปยัง Firebase
    data = {
        'key1': 'value1',
        'key2': 'value2',
        # เพิ่มข้อมูลเพิ่มเติมตามต้องการ
    }

    # ส่งข้อมูลไปยัง Firebase
    send_data_to_firebase(data)
    print("ข้อมูลถูกส่งไปยัง Firebase แล้ว")

if __name__ == "__main__":
    main()
