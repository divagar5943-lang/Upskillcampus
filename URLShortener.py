# URL Shortener - Python Project
# Run with: python URLShortener.py
# This console version stores short codes; it does not run a public web redirect server.

import sqlite3
import secrets
import string
from pathlib import Path
from urllib.parse import urlparse

DB_FILE = Path(__file__).resolve().parent / "urls.db"
ALPHABET = string.ascii_letters + string.digits

def initialize_database():
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                code TEXT PRIMARY KEY,
                original_url TEXT NOT NULL
            )
        """)

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

def create_short_url(url):
    if not is_valid_url(url):
        print("Please enter a valid URL starting with http:// or https://.")
        return
    with sqlite3.connect(DB_FILE) as connection:
        while True:
            code = "".join(secrets.choice(ALPHABET) for _ in range(6))
            try:
                connection.execute(
                    "INSERT INTO urls (code, original_url) VALUES (?, ?)",
                    (code, url)
                )
                break
            except sqlite3.IntegrityError:
                continue
    print(f"Short code: {code}")
    print(f"Lookup URL: http://short.local/{code}")
    print("Note: this is a local demonstration; no web redirect server is running.")

def find_url(code):
    with sqlite3.connect(DB_FILE) as connection:
        row = connection.execute(
            "SELECT original_url FROM urls WHERE code = ?", (code,)
        ).fetchone()
    if row:
        print("Original URL:", row[0])
    else:
        print("Short code not found.")

def list_urls():
    with sqlite3.connect(DB_FILE) as connection:
        rows = connection.execute(
            "SELECT code, original_url FROM urls ORDER BY rowid DESC"
        ).fetchall()
    if not rows:
        print("No URLs saved yet.")
        return
    for code, url in rows:
        print(f"{code} -> {url}")

def main():
    initialize_database()
    while True:
        print("\n=== URL SHORTENER ===")
        print("1. Shorten a URL")
        print("2. Find original URL")
        print("3. List saved URLs")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            create_short_url(input("Enter long URL: ").strip())
        elif choice == "2":
            find_url(input("Enter short code: ").strip())
        elif choice == "3":
            list_urls()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
