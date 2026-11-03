#------Practical 1 Security Global

#------a.Confidentiality:Keeping a diary in a private lockbox so nobody else can read your personal notes

from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

message = "My personal diary is private!"

encrypted = cipher.encrypt(message.encode())
decrypted = cipher.decrypt(encrypted).decode()

print("Lockbox key:", key.decode())
print("Locked:", encrypted)
print("Unlocked:", decrypted)

#-----b.Integrity:Using a tamper-evident sticker on a food delivery bag so you know if any fries were taken
#-----on the way.

import hashlib

data = "Burger, Fries, Coke"
hash1 = hashlib.sha256(data.encode()).hexdigest()

tampered = "Burger, Coke"
hash2 = hashlib.sha256(tampered.encode()).hexdigest()

print("Original bag:", data)
print("Original hash:", hash1)

print("After tampering:", tampered)
print("New hash:", hash2)

print("Integrity verified?", hash1 == hash2)

#-----c.Availablity:Keeping a spare house key hidden in your car so you never get locked out if you lose your
#-----main set

import shutil

original_file = "house_key.txt"
backup_file = "spare_house_key.txt"

shutil.copyfile(original_file, backup_file)

print("Backup completed!")
print("Spare key is available!")

#-----d.Authentication:Showing your photo ID to enter a building while a security guard writes your name in a
#-----sign-in sheet.

from datetime import datetime

users = {
    "Pranay": "ID123",
    "Rahul": "ID456"
}

name = input("Enter your name: ")
photo_id = input("Enter your photo ID: ")

if users.get(name) == photo_id:
    print("Identity verified. Entry allowed.")
    status = "Entry allowed"
else:
    print("Identity not verified. Entry denied.")
    status = "Entry denied"

with open("entry_register.txt", "a") as file:
    file.write(f"{name} - {status} - {datetime.now()}\n")

print("Entry recorded in security register!")

#------e.Non Repudiation:Signing a certified mail delivery receipt so you cannot later claim you never received the
#------package

import hashlib

receiver = "Pranay"
package = "Laptop"

receipt = receiver + " received " + package

signature = hashlib.sha256(receipt.encode()).hexdigest()

received_receipt = "Pranay received Laptop"
received_signature = hashlib.sha256(received_receipt.encode()).hexdigest()

print("Delivery Receipt:", receipt)
print("Signature:", signature)

print("Receipt verified:", signature == received_signature)


#----Practical 2 : Operating System Security

#---a.User Authentication and Persmission
#---Family members get keys to every room, but houseguests are given keys that only open
#---the guest room door

#---auth+perms

import hashlib

users = {}
permissions = {
    "family": ["bedroom", "kitchen", "living room", "guest room"],
    "guest": ["guest room"]
}

def hash_pass(passw):
    return hashlib.sha256(passw.encode()).hexdigest()

def register(username, passw, role):
    users[username] = [hash_pass(passw), role]
    print("Registered Successfully!")

def login(username, passw, room):
    if username in users and users[username][0] == hash_pass(passw):
        print("Authentication Successful!")

        role = users[username][1]

        if room in permissions.get(role, []):
            print("Access Granted to",role,"for", room)
        else:
            print("Access Denied to",role,"for", room)
    else:
        print("Invalid Username or Password!")

register("Pranay", "family123", "family")
register("Rahul", "guest123", "guest")

login("Pranay", "family123", "bedroom")
login("Rahul", "guest123", "guest room")
login("Rahul", "guest123", "kitchen")

#---auth

import hashlib

users = {}

def hash_pass(passw):
    return hashlib.sha256(passw.encode()).hexdigest()

def register(username, passw):
    users[username] = hash_pass(passw)
    print("Registered",username, "Successfully!")

def login(user, passw):
    if users.get(user) == hash_pass(passw):
        print("Access Granted to",user)
    else:
        print("Access Denied to",user)

register("family", "family123")
register("guest", "guest123")

login("family", "family123")
login("guest", "wrong123")


#--perms

permissions = {
    "family": ["bedroom", "kitchen", "living room", "guest room"],
    "guest": ["guest room"]
}

def access_room(user_role, room):
    if room in permissions.get(user_role, []):
        print(f"{user_role} can access {room}")
    else:
        print(f"{user_role} cannot access {room}")

access_room("family", "bedroom")
access_room("guest", "guest room")
access_room("guest", "kitchen")
access_room("guest", "living room")


#---b.Firewalls and Activity Logs
#---A gatekeeper standing at an apartment entrance checks guest lists before letting people in
#---and notes down visitor times.

#---Fire+Acti

import datetime

blocked_ips = ["192.168.1.100", "10.0.0.5"]

def check_access(ip, user):
    if ip in blocked_ips:
        print(f"Access Denied for {user}")
        action = "Entry Denied for",user
    else:
        print(f"Access Granted for {user}")
        action = "Entry Allowed for",user

    with open("access_log.txt", "a") as logfile:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logfile.write(f"[{time}] {user} ({ip}) -> {action}\n")

check_access("192.168.1.100", "Rahul")
check_access("8.8.8.8", "Pranay")

#---fire

blocked_ips = ["192.168.1.100", "10.0.0.5"]

def check_access(ip):
    if ip in blocked_ips:
        print(f"Access Denied for {ip}")
    else:
        print(f"Access Granted for {ip}")

check_access("192.168.1.100")
check_access("8.8.8.8")

#---activi

import datetime

def log_activity(visitor, action):
    with open("visitor_log.txt", "a") as logfile:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logfile.write(f"[{time}] {visitor} -> {action}\n")

log_activity("Rahul", "Entered apartment")
log_activity("Pranay", "Entered apartment")

print("Visitor activity recorded!")

#---c.Memory Management & Buffer Overflows:
#---Assigning designated parking spots keeps cars organized; trying to park a massive semitruck into a compact car spot spills over into adjacent spaces and causes a crash.

#---Mem+Buff

# Memory Management
memory = [None] * 100

def allocate(process_id, size):
    for i in range(len(memory) - size + 1):
        if all(block is None for block in memory[i:i+size]):
            for j in range(i, i+size):
                memory[j] = process_id
            return f"Allocated {size} parking spots to {process_id}"
    return "No sufficient parking space"

def deallocate(process_id):
    count = memory.count(process_id)
    for i in range(len(memory)):
        if memory[i] == process_id:
            memory[i] = None
    return f"Freed {count} parking spots from {process_id}"


# Buffer Overflow
def park_vehicle(parking, vehicle, size, start):
    if start + size <= len(parking):
        for i in range(start, start + size):
            if parking[i] != 0:
                return "Parking space already occupied!"

        for i in range(start, start + size):
            parking[i] = vehicle

        return vehicle + " parked successfully"
    else:
        return "Buffer Overflow! Vehicle exceeds parking space!"


# Demo: Memory Management
print(allocate("Car1", 10))
print(allocate("Car2", 20))
print(deallocate("Car1"))

# Demo: Buffer Overflow
parking = [0] * 5

print(park_vehicle(parking, "Car", 2, 0))
print(park_vehicle(parking, "Truck", 6, 2))
print("Parking:", parking)

#---mem

memory = [None] * 100

def allocate(process_id, size):
    for i in range(len(memory) - size + 1):
        if all(block is None for block in memory[i:i+size]):
            for j in range(i, i+size):
                memory[j] = process_id
            return f"Allocated {size} blocks to {process_id} at {i}"
    return "No sufficient memory"

def deallocate(process_id):
    count = memory.count(process_id)
    for i in range(len(memory)):
        if memory[i] == process_id:
            memory[i] = None
    return f"Deallocated {count} blocks from {process_id}"

print(allocate("Car1", 10))
print(allocate("Car2", 20))
print(deallocate("Car1"))


#--buff

def park_vehicle(parking, vehicle, size, start):
    if start + size <= len(parking):
        for i in range(start, start + size):
            if parking[i] != 0:
                return "Parking space already occupied!"

        for i in range(start, start + size):
            parking[i] = vehicle

        return vehicle + " parked successfully"
    else:
        return "Buffer Overflow! Vehicle exceeds parking space!"

parking = [0] * 5

print(park_vehicle(parking, "Car", 2, 0))
print(park_vehicle(parking, "Truck", 6, 2))
print("Parking:", parking)


#----Practical 3: Secure Communications

#---a.Public/Private Key Encryption
#--Handing out open padlocks (Public Keys) to all your friends. Anyone can snap your
#--padlock onto a box to send you a secret, but only you hold the single master key (Private
#--Key) that opens it.

#---generate_keys

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

receiver_private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048
)

receiver_public_key = receiver_private_key.public_key()

with open("public_padlock.pem", "wb") as f:
    f.write(receiver_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

with open("private_key.pem", "wb") as f:
    f.write(receiver_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

print("Public Padlock and Private Key Generated!")

#---sender.py

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Friend takes receiver's public padlock
with open("public_padlock.pem", "rb") as f:
    public_padlock = serialization.load_pem_public_key(f.read())

secret_box = input("Enter secret message: ").encode()

# Lock the secret box using public padlock
locked_box = public_padlock.encrypt(
    secret_box,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open("locked_box.bin", "wb") as f:
    f.write(locked_box)

print("Secret box locked and sent successfully!")



#-----recevier.py

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Friend takes receiver's public padlock
with open("public_padlock.pem", "rb") as f:
    public_padlock = serialization.load_pem_public_key(f.read())

secret_box = input("Enter secret message: ").encode()

# Lock the secret box using public padlock
locked_box = public_padlock.encrypt(
    secret_box,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open("locked_box.bin", "wb") as f:
    f.write(locked_box)

print("Secret box locked and sent successfully!")

#---Practical 4: Database Security
#---a.SQL Injection Prevention
#---Ordering at a drive-thru and saying "I want a burger, and erase my total bill!" Smart
#---cashiers process your food order while ignoring administrative commands

#--sql inject+role access

import sqlite3

conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

# Create menu table
cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    item TEXT UNIQUE,
    price INTEGER
)
""")

# Create staff table
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# Insert restaurant menu
cursor.execute("INSERT OR IGNORE INTO menu VALUES ('Burger', 100)")
cursor.execute("INSERT OR IGNORE INTO menu VALUES ('Pizza', 200)")

# Insert staff details
cursor.execute("INSERT OR IGNORE INTO staff VALUES ('admin', 'admin123', 'manager')")
cursor.execute("INSERT OR IGNORE INTO staff VALUES ('john', 'john123', 'cashier')")
cursor.execute("INSERT OR IGNORE INTO staff VALUES ('ram', 'ram123', 'customer')")

conn.commit()

# User Login
username = input("Enter username: ")
password = input("Enter password: ")

cursor.execute(
    "SELECT role FROM staff WHERE username = ? AND password = ?",
    (username, password)
)

user = cursor.fetchone()

if user:
    role = user[0]
    print("Login successful! Role:", role)

    if role == "customer":

        # Customer places food order
        food = input("Enter food order: ")

        # UNSAFE VERSION (SQL Injection Vulnerable)
        # query = f"SELECT * FROM menu WHERE item = '{food}'"
        # cursor.execute(query)

        # SECURE VERSION (Prevents SQL Injection)
        cursor.execute(
            "SELECT * FROM menu WHERE item = ?",
            (food,)
        )

        result = cursor.fetchone()

        if result:
            print("Order accepted:", result[0])
            print("Total bill:", result[1])
        else:
            print("Invalid food order!")

    elif role == "cashier":
        print("Cashier can view and process food orders.")

    elif role == "manager":
        print("Manager can view, add and delete menu items.")

else:
    print("Invalid credentials!")

conn.close()


#-----b.Role-Based Access Control (RBAC)
#---Cashiers can take payments, store managers can issue refunds, and cleaning staff cannot
#---open the cash register.

import sqlite3

conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    username TEXT,
    password TEXT,
    role TEXT
)
""")

cursor.execute("DELETE FROM staff")
cursor.execute("INSERT INTO staff VALUES ('admin', 'admin123', 'manager')")
cursor.execute("INSERT INTO staff VALUES ('john', 'john123', 'cashier')")
cursor.execute("INSERT INTO staff VALUES ('ram', 'ram123', 'customer')")
conn.commit()

username = input("Enter username: ")
password = input("Enter password: ")

cursor.execute(
    "SELECT role FROM staff WHERE username = ? AND password = ?",
    (username, password)
)

user = cursor.fetchone()

if user:
    role = user[0]
    print("Login successful! Role:", role)

    if role == "manager":
        print("Can view, add and delete menu items.")
    elif role == "cashier":
        print("Can view and process food orders.")
    elif role == "customer":
        print("Can place food orders only.")
else:
    print("Invalid credentials!")

conn.close()


#-----sql injection 

import sqlite3

conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    item TEXT,
    price INTEGER
)
""")

cursor.execute("DELETE FROM menu")
cursor.execute("INSERT INTO menu VALUES ('Burger', 100)")
cursor.execute("INSERT INTO menu VALUES ('Pizza', 200)")
conn.commit()

food = input("Enter your food order: ")

# UNSAFE VERSION (SQL Injection Vulnerable)
# query = f"SELECT * FROM menu WHERE item = '{food}'"
# cursor.execute(query)

# SECURE VERSION (Prevents SQL Injection)
cursor.execute(
    "SELECT * FROM menu WHERE item = ?",
    (food,)
)

result = cursor.fetchone()

if result:
    print("Order accepted:", result[0])
    print("Total bill:", result[1])
else:
    print("Invalid food order!")

conn.close()

#----Practical 5 : Network Security
#---a.Replay Attack Prevention:
#---Scanning a barcode ticket at a concert. If someone takes a photo of your ticket and tries
#---scanning the exact same image a minute later, the system flags it as a duplicate.

import time

# Validates ticket uniqueness and freshness window to prevent replay attacks
class Scenario5_1_Replay_ConcertTicketScanner:
    
    # Initialize set for scanned tickets and maximum allowable timestamp drift
    def __init__(self, allowable_time_window_seconds: float = 10.0):
        self.scanned_tickets_database = set()
        self.allowable_time_window = allowable_time_window_seconds
        
    # Scans concert ticket barcode and verifies timestamp freshness and uniqueness
    def scan_concert_ticket(self, ticket_barcode: str, ticket_timestamp: float):
        current_time = time.time()
        ticket_signature = f"{ticket_barcode}_{ticket_timestamp}"
        
        if ticket_signature in self.scanned_tickets_database:
            return False, "REJECTED: Duplicate Ticket Scan / Replay Attack Detected! This ticket photo was already used."
            
        if abs(current_time - ticket_timestamp) > self.allowable_time_window:
            return False, "REJECTED: Expired Ticket Timestamp! Scan attempt outside valid entry window."
            
        self.scanned_tickets_database.add(ticket_signature)
        return True, "SUCCESS: Ticket Validated! Gate turnstile unlocked. Enjoy the concert."

scanner = Scenario5_1_Replay_ConcertTicketScanner()
t_now = time.time()

ok1, ticket_msg1 = scanner.scan_concert_ticket("CONCERT_TICKET_12345", t_now)
ok2, ticket_msg2 = scanner.scan_concert_ticket("CONCERT_TICKET_12345", t_now)

print("Scan 1 (Legitimate):", ticket_msg1)
print("Scan 2 (Replay Attack):", ticket_msg2)

#------Practical 6: Cloud Security

#--a.Time-Limited Links:
#--Giving a visitor a temporary guest pass that automatically expires in 30 seconds.

from flask import Flask
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)

guest_passes = {}

@app.route("/generate")
def generate_guest_pass():
    guest_token = secrets.token_urlsafe(16)

    expiry_time = datetime.now() + timedelta(seconds=30)
    guest_passes[guest_token] = expiry_time

    return f"Guest Link: http://127.0.0.1:5000/guest/{guest_token}"


@app.route("/guest/<token>")
def access_guest_page(token):

    if token in guest_passes and datetime.now() < guest_passes[token]:
        return "Welcome Guest! You have temporary access."

    return "Guest Pass Expired or Invalid"


app.run()


#--b.Zero-Trust Client Encryption
#--Locking your files inside a personal steel safe before handing them to a storage unit
#--company so the workers can never read your papers.

#--zero trust

from cryptography.fernet import Fernet
import os
import shutil

os.makedirs("storage_unit", exist_ok=True)

safe_key = Fernet.generate_key()
personal_safe = Fernet(safe_key)

with open("personal_key.key", "wb") as key_file:
    key_file.write(safe_key)

def lock_document(document_path):
    with open(document_path, "rb") as document:
        original_papers = document.read()

    locked_papers = personal_safe.encrypt(original_papers)

    locked_document = "locked_" + os.path.basename(document_path)

    with open(locked_document, "wb") as document:
        document.write(locked_papers)

    shutil.copy(
        locked_document,
        os.path.join("storage_unit", locked_document)
    )

    print("Document locked and stored safely!")

with open("personal_documents.txt", "w") as document:
    document.write("My Confidential Personal Papers")

lock_document("personal_documents.txt")

#------watermark

import hashlib
import os
import shutil

os.makedirs("LEAKED_DOCUMENTS", exist_ok=True)

def ADD_WATERMARK(DOCUMENT_PATH, USER_ID):

    with open(DOCUMENT_PATH, "r") as FILE:
        ORIGINAL_DOCUMENT = FILE.read()

    HIDDEN_MARK = hashlib.sha256(USER_ID.encode()).hexdigest()

    WATERMARK = f"\n<!--USER-ID: {HIDDEN_MARK}-->"

    WATERMARKED_DOCUMENT = "MARKED_" + os.path.basename(DOCUMENT_PATH)

    with open(WATERMARKED_DOCUMENT, "w") as FILE:
        FILE.write(ORIGINAL_DOCUMENT + WATERMARK)

    shutil.copy(WATERMARKED_DOCUMENT, "LEAKED_DOCUMENTS")

    print("WATERMARK ADDED SUCCESSFULLY")

with open("CONFIDENTIAL.txt", "w") as FILE:
    FILE.write("CONFIDENTIAL COMPANY DOCUMENT")

ADD_WATERMARK("CONFIDENTIAL.txt", "EMPLOYEE101")


#----Practical 7:  Iot Security
#---a.Packet Sniffing vs. Encryption:
#--Unencrypted smart home devices broadcast updates like open postcards that anyone
#--nearby can read. Encrypting the connection places those postcards into sealed, opaque
#--envelopes.

#---Practical 8: Security Practices
#---a.Hashes & HMACs:
#--A plastic protective seal on a bottle of medicine. If the seal is broken or tampered with,
#--you know the contents inside are unsafe.


#-- hmac

import hmac
import hashlib
import secrets

secret_key = secrets.token_bytes(32)

medicine = "Aspirin Tablets"

seal = hmac.new(secret_key, medicine.encode(), hashlib.sha256).hexdigest()

print("Original Seal:", seal)

tampered_medicine = "Aspirin Tablets (Contaminated)"

new_seal = hmac.new(secret_key, tampered_medicine.encode(), hashlib.sha256).hexdigest()

if hmac.compare_digest(seal, new_seal):
    print("Seal Intact: Medicine is safe.")
else:
    print("Tampering Detected: Medicine is unsafe.")

#--hashes

import hashlib

medicine = "Aspirin Tablets"

seal = hashlib.sha256(medicine.encode()).hexdigest()

print("Original Seal:", seal)

tampered_medicine = "Aspirin Tablets (Contaminated)"

new_seal = hashlib.sha256(tampered_medicine.encode()).hexdigest()

if seal == new_seal:
    print("Seal Intact: Medicine is safe.")
else:
    print("Tampering Detected: Medicine is unsafe.")



#--mac

import hashlib

secret_key = b"medicine_secret"

medicine = "Aspirin Tablets"

seal = hashlib.blake2b(medicine.encode(), key=secret_key).hexdigest()

print("Original Seal:", seal)

tampered_medicine = "Aspirin Tablets (Contaminated)"

new_seal = hashlib.blake2b(tampered_medicine.encode(), key=secret_key).hexdigest()

if seal == new_seal:
    print("Seal Intact: Medicine is safe.")
else:
    print("Tampering Detected: Medicine is unsafe.")


#--Practical 9 : Penetration Tessting

#--Scanning & Exploitation:
#--Hiring a professional locksmith to walk around your house, jiggle door handles, and check
#--window latches. They hand you a list of weak locks so you can fix them before a thief
#--visits.

import socket

vulnerabilities = {
    "Apache/2.2.8": "Weak lock - Outdated Apache version",
    "OpenSSH_4.7": "Weak lock - Old OpenSSH version",
    "Microsoft-IIS/6.0": "Weak lock - Outdated IIS version"
}

def scan_doors_and_windows(house, doors_windows):
    weak_locks = []

    for door_window in doors_windows:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        if sock.connect_ex((house, door_window)) == 0:
            print("Accessible Entry Point:", door_window)
            weak_locks.append(door_window)

        sock.close()

    return weak_locks

def inspect_locks(house, door_window):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((house, door_window))
        lock_type = sock.recv(1024).decode().strip()
        sock.close()
        return lock_type
    except:
        return None

def check_weak_locks(lock_type):
    for lock in vulnerabilities:
        if lock in lock_type:
            return vulnerabilities[lock]

    return "No known weakness found"

house = input("Enter House IP: ")
doors_windows = [21, 22, 23, 80, 443, 3389]

weak_locks = scan_doors_and_windows(house, doors_windows)

for door_window in weak_locks:
    lock_type = inspect_locks(house, door_window)

    if lock_type:
        print("Lock Type:", lock_type)
        print("Result:", check_weak_locks(lock_type))
    else:
        print("No lock information retrieved for:", door_window)



