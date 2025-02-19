from cryptography.fernet import Fernet
import base64

def encrypt_message(key, message):
    # """เข้ารหัสข้อความด้วยคีย์ที่กำหนด"""
    cipher_suite = Fernet(base64.urlsafe_b64encode(key.encode()))
    return cipher_suite.encrypt(message)

def decrypt_message(key, encrypted_message):
    # """ถอดรหัสข้อความด้วยคีย์ที่กำหนด"""
    cipher_suite = Fernet(base64.urlsafe_b64encode(key.encode()))
    return cipher_suite.decrypt(encrypted_message)

def main():
    # กำหนดคีย์
    key = "reerthyjtrethjytrethjytrewrdjtyr"
    print(len(key))
    # ข้อความที่ต้องการเข้ารหัส
    message = b"Hello, World! This is a secret message."

    # เข้ารหัสข้อความ
    encrypted_message = encrypt_message(key, message)
    print("encode :", encrypted_message)

    # ถอดรหัสข้อความ
    decrypted_message = decrypt_message(key, encrypted_message)
    print("decode :", decrypted_message.decode('utf-8'))

if __name__ == "__main__":
    main()
