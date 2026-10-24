from cryptography.fernet import Fernet
import json
import os
import hashlib
import random
import string

KEY_FILE = "secret.key"
DATA_FILE = "passwords.json"
MASTER_FILE = "master.json"

def hash_password(password):
    """Hash the master password using SHA-256 for secure comparison."""
    return hashlib.sha256(password.encode()).hexdigest()

def setup_master_password():
    """Set up a master password if one doesn't exist yet."""
    if not os.path.exists(MASTER_FILE):
        print("--- First Time Setup ---")
        master_pwd = input("Create a Master Password: ")
        hashed = hash_password(master_pwd)
        with open(MASTER_FILE, "w") as f:
            json.dump({"master_hash": hashed}, f)
        print("Master password set successfully!\n")

def verify_master_password():
    """Verify the entered master password against the stored hash."""
    setup_master_password()
    with open(MASTER_FILE, "r") as f:
        data = json.load(f)
        stored_hash = data["master_hash"]

    attempts = 3
    while attempts > 0:
        entered_pwd = input("Enter your Master Password: ")
        if hash_password(entered_pwd) == stored_hash:
            print("Access granted!\n")
            return True
        else:
            attempts -= 1
            print(f"Incorrect password. Attempts remaining: {attempts}")

    print("Too many incorrect attempts. Exiting.")
    return False

def load_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

def load_passwords():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_password(cipher, service, username, password):
    passwords = load_passwords()
    encrypted_pwd = cipher.encrypt(password.encode()).decode()
    passwords[service] = {"username": username, "password": encrypted_pwd}

    with open(DATA_FILE, "w") as f:
        json.dump(passwords, f, indent=4)
    print(f"✅ Saved password for '{service}' successfully!")

def get_password(cipher, service):
    passwords = load_passwords()
    if service in passwords:
        encrypted_pwd = passwords[service]["password"].encode()
        decrypted_pwd = cipher.decrypt(encrypted_pwd).decode()
        print(f"\n--- {service} ---")
        print(f"Username: {passwords[service]['username']}")
        print(f"Password: {decrypted_pwd}")
    else:
        print(f"❌ Service '{service}' not found.")

def list_services():
    passwords = load_passwords()
    if not passwords:
        print("No stored passwords found.")
        return
    print("\n--- Saved Services ---")
    for service in passwords.keys():
        print(f"- {service}")

def delete_password(service):
    passwords = load_passwords()
    if service in passwords:
        del passwords[service]
        with open(DATA_FILE, "w") as f:
            json.dump(passwords, f, indent=4)
        print(f"🗑️ Deleted service '{service}' successfully!")
    else:
        print(f"❌ Service '{service}' not found.")

def generate_random_password(length=12):
    """Generate a strong random password containing letters, numbers, and symbols."""
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(length))
    return password

if __name__ == "__main__":
    if verify_master_password():
        key = load_or_create_key()
        cipher = Fernet(key)

        while True:
            print("\n==============================")
            print("🔒 PYTHON PASSWORD MANAGER")
            print("==============================")
            print("1. Add Password")
            print("2. Get Password")
            print("3. List All Services")
            print("4. Generate Random Password")
            print("5. Delete Password")
            print("6. Exit")

            choice = input("Choose an option (1-6): ")

            if choice == "1":
                s = input("Service name (e.g., GitHub): ").strip()
                u = input("Username/Email: ").strip()
                gen_choice = input("Do you want to auto-generate a strong password? (y/n): ").strip().lower()
                if gen_choice == 'y':
                    p = generate_random_password()
                    print(f"Generated Password: {p}")
                else:
                    p = input("Enter password: ")
                save_password(cipher, s, u, p)

            elif choice == "2":
                s = input("Service name to look up: ").strip()
                get_password(cipher, s)

            elif choice == "3":
                list_services()

            elif choice == "4":
                length = input("Enter password length (default 12): ").strip()
                length = int(length) if length.isdigit() else 12
                pwd = generate_random_password(length)
                print(f"\n🔑 Generated Secure Password: {pwd}")

            elif choice == "5":
                s = input("Service name to delete: ").strip()
                confirm = input(f"Are you sure you want to delete '{s}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    delete_password(s)

            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please choose between 1 and 6.")
