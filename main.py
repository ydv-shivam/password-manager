from cryptography.fernet import Fernet
import json
import os

# Key management for encryption
KEY_FILE = "secret.key"
DATA_FILE = "passwords.json"

def load_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

key = load_or_create_key()
cipher = Fernet(key)

def save_password(service, username, password):
    passwords = load_passwords()
    encrypted_pwd = cipher.encrypt(password.encode()).decode()
    passwords[service] = {"username": username, "password": encrypted_pwd}

    with open(DATA_FILE, "w") as f:
        json.dump(passwords, f, indent=4)
    print(f"Saved password for {service} successfully!")

def load_passwords():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def get_password(service):
    passwords = load_passwords()
    if service in passwords:
        encrypted_pwd = passwords[service]["password"].encode()
        decrypted_pwd = cipher.decrypt(encrypted_pwd).decode()
        print(f"Username: {passwords[service]['username']}")
        print(f"Password: {decrypted_pwd}")
    else:
        print("Service not found.")

if __name__ == "__main__":
    while True:
        choice = input("\n1. Add Password\n2. Get Password\n3. Exit\nChoose an option: ")
        if choice == "1":
            s = input("Service name (e.g., GitHub): ")
            u = input("Username/Email: ")
            p = input("Password: ")
            save_password(s, u, p)
        elif choice == "2":
            s = input("Service name to look up: ")
            get_password(s)
        elif choice == "3":
            break
