# Password Manager - Python Project
# One-time dependency: python -m pip install cryptography
# Run with: python PasswordManager.py
# Demo project: keep the generated key file private and make secure backups.

import sqlite3
import secrets
import string
from pathlib import Path
from cryptography.fernet import Fernet

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "passwords.db"
KEY_FILE = BASE_DIR / "password.key"

def load_cipher():
    if not KEY_FILE.exists():
        KEY_FILE.write_bytes(Fernet.generate_key())
        print(f"Created encryption key: {KEY_FILE.name}")
        print("Keep this key private. If it is lost, saved passwords cannot be decrypted.")
    return Fernet(KEY_FILE.read_bytes())

def initialize_database():
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS credentials (
                service TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                encrypted_password BLOB NOT NULL
            )
        """)

def save_credential(cipher):
    service = input("Service / website: ").strip()
    username = input("Username / email: ").strip()
    password = input("Password to store: ")
    if not service or not username or not password:
        print("All fields are required.")
        return
    encrypted = cipher.encrypt(password.encode("utf-8"))
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            "INSERT OR REPLACE INTO credentials (service, username, encrypted_password) VALUES (?, ?, ?)",
            (service, username, encrypted)
        )
    print("Credential saved.")

def retrieve_credential(cipher):
    service = input("Service to search for: ").strip()
    with sqlite3.connect(DB_FILE) as connection:
        row = connection.execute(
            "SELECT username, encrypted_password FROM credentials WHERE service = ?",
            (service,)
        ).fetchone()
    if row is None:
        print("No credential found for that service.")
        return
    username, encrypted = row
    try:
        password = cipher.decrypt(encrypted).decode("utf-8")
    except Exception:
        print("Could not decrypt the password. Check that password.key is the original key.")
        return
    print(f"Username: {username}")
    print(f"Password: {password}")

def generate_password():
    alphabet = string.ascii_letters + string.digits + "!@#$%&*?"
    password = "".join(secrets.choice(alphabet) for _ in range(16))
    print("Generated password:", password)

def main():
    initialize_database()
    cipher = load_cipher()
    while True:
        print("\n=== PASSWORD MANAGER ===")
        print("1. Save credential")
        print("2. Retrieve credential")
        print("3. Generate password")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            save_credential(cipher)
        elif choice == "2":
            retrieve_credential(cipher)
        elif choice == "3":
            generate_password()
        elif choice == "4":
            print("Exiting Password Manager.")
            break
        else:
            print("Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
