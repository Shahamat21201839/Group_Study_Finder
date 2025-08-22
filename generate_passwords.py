#!/usr/bin/env python3
"""
Password Hash Generator for Sample Data
Run this script to generate proper password hashes for sample users.
All sample users will have the password: password123
"""

from werkzeug.security import generate_password_hash

def generate_sample_passwords():
    password = "password123"
    hash_value = generate_password_hash(password)

    print("Password Hash Generator")
    print("="*50)
    print(f"Password: {password}")
    print(f"Hash: {hash_value}")
    print()
    print("Use this hash value in your sample_data.sql file")
    print("All sample users should use this same hash for password123")

    return hash_value

if __name__ == "__main__":
    generate_sample_passwords()
