
#Practical 1 – Security Goals
#----a. Confidentiality – RSA Message Encryption and Decryption---

from cryptography.fernet import Fernet
key=Fernet.generate_key()
cipher=Fernet(key)
message="Top Secret message!"
encrypted=cipher.encrypt(message.encode())
decrypted=cipher.decrypt(encrypted).decode()
print("Key;",key.decode())
print("encyrpted;",encrypted)
print("deecyrpted;",decrypted)


#----b. Integrity – Hash Comparison to Detect Data Tampering---

import hashlib
data="This is important"
hash1=hashlib.sha256(data.encode()).hexdigest()
tampered="this is important"
hash2=hashlib.sha256(tampered.encode()).hexdigest()
print("hash1;",hash1)
print("hash2;",hash2)
print("integrity verified?",hash1==hash2)


#----c. Availability – Monitoring Website/Server Availability---

import shutil
original_file = r"C:\Users\student\Downloads\data.txt"
backup_file = r"C:\Users\student\Downloads\backup_data.txt"
shutil.copyfile(original_file,backup_file)
print("Backup completed!")


#---d. Authentication – OTP-Based Authentication--

users={
    "admin":"password123",
    "user1":"hello123"
}
username = input("Enter username: ")
password = input("Enter password: ")

if users.get(username) == password:
    print("Access granted")
else:
    print("Access denied")


#----e. Non-Repudiation – RSA Digital Signature and Verification--

import hashlib
message = "Approve $5000 transfer"
signature = hashlib.sha256(message.encode()).hexdigest()

received_message = "Approve $5000 transfer"
received_signature = hashlib.sha256(received_message.encode()).hexdigest()

print("Signature verified:", signature == received_signature)

#-----f. Accountability – User Activity Logging-----
import datetime

def log_action(user, action):
    with open("audit_log.txt", "a") as log:
        timestamp = datetime.datetime.now()
        log.write(f"{timestamp} - {user}: {action}\n")

log_action("admin", "Logged in")
log_action("user1", "Viewed report")

print("Actions logged successfully!")




#----------Practical 2 – OS Security-------------


#-----1) Key Concepts of OS Security

#------------a. User Authentication with Password Hashing-----

import hashlib
users={}
def hash_pass(passw):
    return hashlib.sha256(passw.encode()).hexdigest()
def register(username,passw):
    users[username]=hash_pass(passw)
    print("Registered Successfully!")
def login(user,passw):
    if users.get(user)==hash_pass(passw):
        print("Access Granted!")
    else:
        print("Access Denied!")
register("admin","securepass")
login("admin","securepass")
login("admin","wrongpass")



#--------b. Role-Based File Access (Read/Write Permissions)
permissions={
"admin":["read","write"],
"guest":["read"]
}
def access_file(user_role,action):
    if action in permissions.get(user_role,[]):
        print(f"{user_role} can {action} the file")
    else:
        print(f"{user_role} cannot {action} the file")
access_file("admin","write")
access_file("guest","write")
access_file("guest","read")


#-----------c. File Encryption with AES

from cryptography.fernet import Fernet
key=Fernet.generate_key()
with open("filekey.key","wb") as filekey:
    filekey.write(key)
def encrypt_file(filename):
    with open("filekey.key","rb") as filekey:
        key=filekey.read()
    fernet=Fernet(key)
    with open(filename,"rb") as file:
        data=file.read()
    encrypted=fernet.encrypt(data)
    with open(filename,"wb") as file:
        file.write(encrypted)
    print("File Encrypted")
encrypt_file("example.txt")

#-------d. File Integrity Checker---
import hashlib
def get_fhash(filename):
    with open(filename,"rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
og_hash=get_fhash("example.txt")
curr_hash=get_fhash("example.txt")
if og_hash==curr_hash:
    print("File is intact")
else:
    print("File has been changes")


#-----e. Basic IP Firewall Simulation

blocked_ips=["192.168.1.100","10.0.0.5"]
def check_access(ip):
    if ip in blocked_ips:
        print(f"Access Denied for {ip}")
    else:
        print(f"Access Granted for {ip}")
check_access("192.168.1.100")
check_access("8.8.8.8")

#------f. Activity Logging

import datetime
def log_activity(user,action):
    with open("access_log","a") as logfile:
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logfile.write(f"[{time}]{user} -> {action}\n")
log_activity("admin","Accessed settings")
log_activity("guest","tried to delete files")



#-----------2) Key Concepts of OS Memory

#-------g. Simulate Memory Allocation (Static and Dynamic)
memory = [None] * 100
def allocate(process_id, size):
    for i in range(len(memory) - size + 1):
        if all(block is None for block in memory[i:i+size]):
            for j in range(i, i+size):
                memory[j] = process_id
            return f" Allocated {size} blocks to {process_id} at {i}"
    return " No sufficient memory"
def deallocate(process_id):
    count = memory.count(process_id)
    for i in range(len(memory)):
        if memory[i] == process_id:
            memory[i] = None
    return f"Deallocated {count} blocks from {process_id}"
# Demo
print(allocate("P1", 10))
print(allocate("P2", 20))
print(deallocate("P1"))

#------h. Monitor Real Memory Usage of Python Process

import os, psutil
process = psutil.Process(os.getpid())
print(f" Current Memory Usage: {process.memory_info().rss / 1024**2:.2f} MB")

#-----i. Garbage Collection Visualization

import gc
import sys
a = [1] * (10**6) # Create large object
print("Memory used:", sys.getsizeof(a), "bytes")
del a # Delete variable
gc.collect() # Force garbage collection
print(" Garbage collected")

#-------j. Paging Simulation

import math
def paging_simulator(process_size, page_size):
    num_pages = math.ceil(process_size / page_size)
    page_table = {f"Page {i}": f"Frame {i}" for i in range(num_pages)}
    return page_table
# Example: 1024 KB process with 256 KB pages
table = paging_simulator(1024, 256)
for k, v in table.items():
    print(f"{k} → {v}")

#--------k. Memory Leak Simulation and Detection

import tracemalloc
tracemalloc.start()
def leak_memory():
    leaky_list = []
    for _ in range(100000):
        leaky_list.append("leak" * 1000)
    return leaky_list
leak_memory()
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")
print(" Memory Leak Detected at:")
for stat in top_stats[:3]:
    print(stat)


#--------l. Simulated Buffer Overflow

def safe_array_write(array, index, value):
    if index < len(array):
        array[index] = value
        return " Value written"
    else:
        return " Buffer Overflow Attempt!"
arr = [0] * 5
print(safe_array_write(arr, 2, 10))
print(safe_array_write(arr, 10, 10))



#-----------Practical 3 – Secure Communication

#------c. RSA Key Generation
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


sender_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
sender_public = sender_private.public_key()

with open("sender_private_key.pem", "wb") as f:
    f.write(
        sender_private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

with open("sender_public_key.pem", "wb") as f:
    f.write(
        sender_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )


receiver_private = rsa.generate_private_key(
    public_exponent=65537, key_size=2048
)
receiver_public = receiver_private.public_key()

with open("receiver_private_key.pem", "wb") as f:
    f.write(
        receiver_private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

with open("receiver_public_key.pem", "wb") as f:
    f.write(
        receiver_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )

print(" All RSA keys generated and saved successfully:")
print("  - sender_private_key.pem & sender_public_key.pem")
print("  - receiver_private_key.pem & receiver_public_key.pem")


#------------d. Sender Side – Encryption and Digital Signing

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# 1. Load Receiver's Public Key (used to ENCRYPT)
with open("receiver_public_key.pem", "rb") as f:
    receiver_public_key = serialization.load_pem_public_key(f.read())

# 2. Load Sender's Private Key (used to SIGN)
with open("sender_private_key.pem", "rb") as f:
    sender_private_key = serialization.load_pem_private_key(
        f.read(), password=None
    )

# 3. Get message dynamically from user input
user_input = input("Enter the message you want to encrypt and sign: ")
message = user_input.encode("utf-8")  # Convert string to bytes

# 4. Encrypt the message with Receiver's Public Key
encrypted_message = receiver_public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

# 5. Sign the message with Sender's Private Key
signature = sender_private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256(),
)

# 6. Save outputs to disk
with open("encrypted_message.bin", "wb") as f:
    f.write(encrypted_message)

with open("signature.bin", "wb") as f:
    f.write(signature)

print("\n Message encrypted and signed successfully.")
print("Saved 'encrypted_message.bin' and 'signature.bin'.")



#---------e. Receiver Side – Decryption and Signature Verification



from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


with open("receiver_private_key.pem", "rb") as f:
    receiver_private_key = serialization.load_pem_private_key(
        f.read(), password=None
    )


with open("sender_public_key.pem", "rb") as f:
    sender_public_key = serialization.load_pem_public_key(f.read())


with open("encrypted_message.bin", "rb") as f:
    encrypted_message = f.read()

with open("signature.bin", "rb") as f:
    signature = f.read()


decrypted_bytes = receiver_private_key.decrypt(
    encrypted_message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

original_message = decrypted_bytes.decode("utf-8")
print(f"\n Decrypted Message: '{original_message}'")


print("\n--- Signature Verification Options ---")
choice = input("Do you want to tamper with the message? (y/n): ").strip().lower()

if choice == "y":
    altered_text = input("Enter the new/altered message: ")
    message_to_verify = altered_text.encode("utf-8")
else:
    message_to_verify = decrypted_bytes


try:
    sender_public_key.verify(
        signature,
        message_to_verify,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    print("\n Signature Verified: Message is authentic and untampered!")
except InvalidSignature:
    print(
        "\n SECURITY ALERT: Signature Verification Failed! The message was tampered with!"
    )


#---------------Practical 4 – Database Security

#--------a. Parameterized Queries (Input Validation / SQL Injection Prevention)

import sqlite3 

conn = sqlite3.connect("students.db") 
cursor = conn.cursor() 

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS users ( 
        username TEXT, 
        password TEXT 
    ) 
""") 

cursor.execute("INSERT INTO users VALUES ('admin', 'admin_password')") 
conn.commit() 

username = input("Enter username: ") 
password = input("Enter password: ") 

query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'" 
cursor.execute(query) 

# Secure Version (Parameterized Query)

# cursor.execute( 
#     "SELECT * FROM users WHERE username = ? AND password = ?", 
#     (username, password) 
# ) 

result = cursor.fetchone() 
print(result) 

if result: 
    print("Login successful!") 
else: 
    print("Invalid credentials!") 

conn.close()

#--------------b. Password Hashing using bcrypt

import sqlite3
import bcrypt

conn = sqlite3.connect("secure_users.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password BLOB
    )
""")
conn.commit()

username = input("Enter username: ")
raw_password = input("Enter password: ")

hashed_password = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt())

cursor.execute(
    "INSERT INTO users VALUES (?, ?)",
    (username, hashed_password)
)
conn.commit()

login_user = input("Username to login: ")
login_pwd = input("Password to login: ")

cursor.execute(
    "SELECT password FROM users WHERE username = ?",
    (login_user,)
)

data = cursor.fetchone()
print(data)

if data and bcrypt.checkpw(login_pwd.encode(), data[0]):
    print("Login successful!")
else:
    print("Login failed!")

conn.close()


#---------c. Role-Based Access Control (RBAC)-----


import sqlite3 

conn = sqlite3.connect("rbac.db") 
cursor = conn.cursor() 

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS users ( 
        username TEXT, 
        password TEXT, 
        role TEXT 
    ) 
""") 

cursor.execute("INSERT INTO users VALUES ('admin', 'admin_pwd', 'admin')") 
cursor.execute("INSERT INTO users VALUES ('john', 'john_pwd', 'student')") 
conn.commit() 

username = input("Enter username: ") 
password = input("Enter password: ") 

cursor.execute( 
    "SELECT role FROM users WHERE username = ? AND password = ?", 
    (username, password)
) 

user = cursor.fetchone() 

if user: 
    role = user[0] 
    print(f"Login successful! Your role is: {role}") 
    
    if role == "admin": 
        print("Access granted to view, add, delete and modify records.") 
    elif role == "student": 
        print("Access granted to view records.") 
    else: 
        print("Limited access.") 
else: 
    print("Invalid credentials!") 

conn.close()


#--------d. Field-Level Encryption using Fernet

from cryptography.fernet import Fernet 
key = Fernet.generate_key() 
cipher = Fernet(key) 
data = "Confidential Information" 
encrypted_data = cipher.encrypt(data.encode()) 
print("Encrypted data:", encrypted_data) 
decrypted_data = cipher.decrypt(encrypted_data).decode() 
print("Decrypted data:", decrypted_data)


#------------Practical 5 – Network Security

#1user_auth.py()

#-----user_auth.py
import sqlite3
import hashlib
import secrets

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "username TEXT PRIMARY KEY, "
        "salt TEXT NOT NULL, "
        "password_hash TEXT NOT NULL)"
    )

    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)

    hash_val = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    )

    return salt, hash_val.hex()

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    if cursor.fetchone():
        conn.close()
        return "Username already exists!"

    salt, password_hash = hash_password(password)

    cursor.execute(
        "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
        (username, salt, password_hash),
    )

    conn.commit()
    conn.close()

    return "User registered successfully!"

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT salt, password_hash FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    conn.close()

    if not result:
        return False

    salt, stored_hash = result
    _, input_hash = hash_password(password, salt)

    return input_hash == stored_hash

if __name__ == "__main__":
    init_db()

    print(register_user("alice", "secret_password"))
    print(register_user("alice", "strong_password"))

    print(
        "Login success?",
        authenticate_user("alice", "secret_password")
    )

    print(
        "Login success?",
        authenticate_user("alice", "wrong_password")
    )

#2secure_server_with_replay.py(1Implement timestamp-based replay attack detection)

import socket
from datetime import datetime, timedelta
from user_auth import authenticate_user, init_db

# Initialize database
init_db()

# Replay protection class
class MessageReceiver:

    def __init__(self):
        self.last_timestamp = None
        self.replay_window = timedelta(seconds=30)

    def verify_timestamp(self, timestamp_str):
        try:
            msg_time = datetime.strptime(
                timestamp_str, "%Y-%m-%d %H:%M:%S"
            )
            now = datetime.utcnow()

            if self.last_timestamp and msg_time <= self.last_timestamp:
                return False, "Replay attack detected: Old timestamp."

            if abs(now - msg_time) > self.replay_window:
                return False, "Timestamp too old or too far in future."

            self.last_timestamp = msg_time
            return True, "Timestamp is valid."

        except ValueError:
            return False, "Invalid timestamp format."

# Server setup
server = socket.socket()
server.bind(("localhost", 9999))
server.listen(1)

print("Server listening on port 9999...")

conn, addr = server.accept()
print(f"Connected by {addr}")

# Step 1: Receive login details
username = conn.recv(1024).decode()
password = conn.recv(1024).decode()

if authenticate_user(username, password):

    conn.send(b"AUTH_OK")
    print("Authenticated:", username)

    # Step 2: Replay Protection
    receiver = MessageReceiver()

    while True:
        data = conn.recv(1024).decode()

        if not data:
            break

        try:
            msg, timestamp_str = data.split("||")

        except ValueError:
            conn.send(b"ERROR: Invalid message format")
            continue

        valid, response = receiver.verify_timestamp(timestamp_str)

        print(f"[{username}] {msg} @ {timestamp_str} => {response}")

        conn.send(response.encode())

else:
    conn.send(b"AUTH_FAILED")
    print("Authentication failed.")

conn.close()


#3secure_client_with_timestamp.py(2Implement timestamp-based replay attack detection)

import socket
from datetime import datetime
import time

client = socket.socket()
client.connect(('localhost', 9999))

# Step 1: Login
client.send(b"alice")      # Username
time.sleep(1)
client.send(b"secret_password")    # Password

auth_response = client.recv(1024)

if auth_response != b"AUTH_OK":
    print("Login failed.")
    client.close()

else:
    print("Login successful.")

    # Step 2: Send messages with timestamps
    while True:
        msg = input("Enter message (or 'exit'): ")

        if msg == "exit":
            break

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"{msg}||{timestamp}"

        client.send(full_msg.encode())

        server_response = client.recv(1024).decode()
        print("Server:", server_response)

        # Simulate replay attempt
        time.sleep(2)
        print("\n[Replaying same message...]")

        client.send(full_msg.encode())
        print("Server:", client.recv(1024).decode())

client.close()

#4secure_server_with_file_transfer.py(1Encrypted File Transfer over Same Connection )

import socket
from user_auth import authenticate_user, init_db
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Constants
AES_KEY = bytes.fromhex("054f0c5c692ffa3e0d0fa7d156966812")
aesgcm = AESGCM(AES_KEY)

# Set up database
init_db()

server = socket.socket()
server.bind(('localhost', 8888))
server.listen(1)

print("File Server listening on port 8888...")

conn, addr = server.accept()
print(f"Connected by {addr}")

# Step 1: Login
username = conn.recv(1024).decode()
password = conn.recv(1024).decode()

if authenticate_user(username, password):

    conn.send(b"AUTH_OK")
    print("Authenticated:", username)

    # Step 2: Receive Encrypted File
    nonce = conn.recv(12)  # AES-GCM nonce (must be 12 bytes)
    filename = conn.recv(1024).decode()
    file_size = int(conn.recv(1024).decode())

    encrypted_data = b''

    while len(encrypted_data) < file_size:
        chunk = conn.recv(4096)

        if not chunk:
            break

        encrypted_data += chunk

    # Decrypt file data
    try:
        decrypted = aesgcm.decrypt(nonce, encrypted_data, None)

        with open("received_" + filename, 'wb') as f:
            f.write(decrypted)

        conn.send(b"File received and decrypted.")
        print(f"File saved: received_{filename}")

    except Exception as e:
        print("Decryption failed:", e)
        conn.send(b"File decryption failed.")

else:
    conn.send(b"AUTH_FAILED")

conn.close()

#5secure_cleint_with_file_transfer.py(2Encrypted File Transfer over Same Connection )

import socket
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# AES Key must match server's
AES_KEY = bytes.fromhex("054f0c5c692ffa3e0d0fa7d156966812")
aesgcm = AESGCM(AES_KEY)

client = socket.socket()
client.connect(('localhost', 8888))

# Step 1: Login
client.send(b"alice")      # Username
time.sleep(1)
client.send(b"secret_password")    # Password

if client.recv(1024) != b"AUTH_OK":
    print("Login failed.")
    client.close()
    exit()

print("Logged in. Ready to send file.")

# Step 2: Select and encrypt file
filename = "sample.txt"  # Make sure this file exists

with open(filename, 'rb') as f:
    file_data = f.read()

nonce = os.urandom(12)  # GCM nonce
encrypted_data = aesgcm.encrypt(nonce, file_data, None)

# Step 3: Send file
client.send(nonce)
time.sleep(0.5)

client.send(filename.encode())
time.sleep(0.5)

client.send(str(len(encrypted_data)).encode())
time.sleep(0.5)

client.sendall(encrypted_data)

# Step 4: Receive server response
print("Server:", client.recv(1024).decode())

client.close()


#6encrypted_file_transfer_over_same.py(3Encrypted File Transfer over Same Connection)

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Get the public key from the private key
public_key = private_key.public_key()

# Save the private key to a PEM file
with open("client_private.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        )
    )

# Save the public key to a PEM file
with open("client_public.pem", "wb") as f:
    f.write(
        public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )




#7replace_pass_based_login.py(Replace password-based login with RSA public-key)

import socket
import secrets
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# Load client public key
with open("client_public.pem", "rb") as f:
    client_public_key = serialization.load_pem_public_key(f.read())

# Set up the server
server = socket.socket()
server.bind(('localhost', 7777))
server.listen(1)

print("RSA Server running...")

# Accept client connection
conn, addr = server.accept()
print("Connected by", addr)

# Step 1: Send challenge to client
challenge = secrets.token_bytes(32)
conn.send(challenge)

# Step 2: Receive signature from client
signature = conn.recv(512)

# Step 3: Verify the signature
try:
    client_public_key.verify(
        signature,
        challenge,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    conn.send(b"AUTH_OK")
    print("RSA Authentication Successful")

except Exception as e:
    conn.send(b"AUTH_FAILED")
    print("RSA Authentication Failed:", str(e))

# Close the connection
conn.close()


#8replace_pass_two.py(Replace password-based login with RSA public-key)


import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# Load private key
with open("client_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Create a socket client
client = socket.socket()
client.connect(('localhost', 7777))

# Step 1: Receive challenge
challenge = client.recv(1024)

# Step 2: Sign the challenge
signature = private_key.sign(
    challenge,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# Step 3: Send signature to the server
client.send(signature)

# Step 4: Receive response from the server
response = client.recv(1024).decode()
print("Server:", response)

# Close the connection
client.close()

#-------a. User Registration and Login using SQLite with Password Hashing
#-----------b. Replay Attack Detection
#2--------time stamp based 
#-------------c. Encrypted File Transfer using AES-GCM
#------d. RSA Public-Key Authentication (Challenge–Response)

#----------Practical 6 – Cloud Security

#---------a. Time-Limited Secure File Access (Flask-Based)

#py -m pip install flask
#create a folder my project containing two files
#prac6.py
#sample.txt
#Time-Limited Secure File Access Demo (Flask Based)
# Download file
from flask import Flask, send_file
import time

app = Flask(__name__)
start = time.time()

@app.route('/')
def home():
    return '<h2>Secure File Access</h2><a href="/download">Download Secret File</a>'

@app.route('/download')
def download():
    if time.time() - start < 20:
        return send_file("backup_data.txt", as_attachment=True)
    else:
        return "Access Denied! Time Expired."

app.run()


#-----b. Client-Side Encrypted Cloud Backup

#py -m pip install flask
#create a folder my project containing two files
#prac6.py
#sample.txt
#make client_encrypted_backup.py
from cryptography.fernet import Fernet
import os
import shutil

# Create a simulated cloud folder
os.makedirs("cloud_backup", exist_ok=True)

# Step 1: Generate a secret key (AES)
key = Fernet.generate_key()
fernet = Fernet(key)

# Save the key securely (local file)
with open("aes.key", "wb") as kf:
    kf.write(key)

# Step 2: Encrypt the file
def encrypt_file(file_path):

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    encrypted_file = "enc_" + os.path.basename(file_path)

    with open(encrypted_file, "wb") as ef:
        ef.write(encrypted_data)

    # Simulate cloud upload
    shutil.copy(encrypted_file, "cloud_backup")

    print(f"Encrypted and uploaded: {encrypted_file}")


# Step 3: Run the encryption
if __name__ == "__main__":

    input_file = "sample_file.txt"

    # Create file if not present
    if not os.path.exists(input_file):
        with open(input_file, "w") as f:
            f.write("Confidential Cloud Backup File")

    encrypt_file(input_file)

#-------c. Intrusion Detection for Cloud Access Logs


#make json file abc.json
#import json
from datetime import datetime

# Set your blacklisted IPs
blacklisted_ips = ["192.168.1.10", "10.0.0.5"]

# Load access logs
with open("abc.json") as f:
    logs = json.load(f)

# Dictionary to count failed attempts
failed_attempts = {}

print("\nIntrusion Detection Log Analysis:\n")

for entry in logs:
    user = entry["user"]
    ip = entry["ip"]
    time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
    status = entry["status"]

    # Blacklist check
    if ip in blacklisted_ips:
        print(f"ALERT: Access from blacklisted IP {ip} by user '{user}'")

    # Time window check (office hours: 08:00 to 18:00)
    if not (8 <= time.hour <= 18):
        print(f"Off-hour login attempt by '{user}' at {time.strftime('%H:%M')}")

    # Failed login tracking
    if status == "failed":
        failed_attempts[user] = failed_attempts.get(user, 0) + 1

        if failed_attempts[user] >= 2:
            print(f"User '{user}' has {failed_attempts[user]} failed login attempts!")

print("\nLog scan completed.\n")

#------d. Invisible Watermarking for Data Leakage Prevention

#Create a folder, for example my project.
#Open the folder in VS Code.
#Create a Python file named prac.py.
#Paste the above code.
#Keep sample.txt in the same folder (or the code will create it).
#Open CMD in that folder.
#py prac.py
import os
import shutil
import hashlib

# Create cloud folder
os.makedirs("cloud_upload", exist_ok=True)

# Function to add watermark
def watermark_text(file_path, user_id):

    with open(file_path, "r") as f:
        content = f.read()

    # Generate watermark
    watermark = hashlib.sha256(user_id.encode()).hexdigest()

    # Add watermark to file
    new_file = "wm_" + os.path.basename(file_path)

    with open(new_file, "w") as f:
        f.write(content + "\nUSER-ID: " + watermark)

    # Upload file
    shutil.copy(new_file, "cloud_upload")

    print("Watermark added successfully")
    print("File uploaded to cloud_upload folder:", new_file)


# Main program
if __name__ == "__main__":

    file = "sample.txt"

    # Create sample file if not present
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("This is confidential data.")

    watermark_text(file, "user123")


#------Practical 7 – IoT Security
#-----a. AES Encryption for IoT Sensor Data
#pip install pycryptodome

from Crypto.Cipher import AES
import base64

# AES requires a 16/24/32 byte key
key = b"ThisIsA16ByteKey"
cipher = AES.new(key, AES.MODE_EAX)

# IoT sensor data (example: temperature)
sensor_data = "Temperature: 28C"

# Encrypt
ciphertext, tag = cipher.encrypt_and_digest(sensor_data.encode())
nonce = cipher.nonce

print("Encrypted Data:", base64.b64encode(ciphertext).decode())

# Decrypt
cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)
decrypted_data = cipher_dec.decrypt(ciphertext).decode()

print("Decrypted Data:", decrypted_data)

#----------b. HMAC-Based Data Integrity Verification

import hmac
import hashlib

# Secret key shared between IoT device and server
secret_key = b"iot_secret_key"

# IoT message
message = b"Humidity: 70%"

# Generate HMAC
hmac_digest = hmac.new(
    secret_key,
    message,
    hashlib.sha256
).hexdigest()

print("Message:", message.decode())
print("Generated HMAC:", hmac_digest)

# Receiver verification
received_hmac = hmac.new(
    secret_key,
    message,
    hashlib.sha256
).hexdigest()

if hmac.compare_digest(hmac_digest, received_hmac):
    print("Message is authentic")
else:
    print("Message tampered!")


#----------c. Secure MQTT Communication using TLS

import paho.mqtt.client as mqtt
import time

# Called when connected to MQTT broker
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code " + str(reason_code))
    client.subscribe("iot/device1")

# Called when a message is received
def on_message(client, userdata, msg):
    print("Received:", msg.topic, msg.payload.decode())

# Create MQTT client
client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect("test.mosquitto.org", 1883, 60)

# Start network loop
client.loop_start()

# Give time to connect
time.sleep(2)

# Publish sensor message
client.publish(
    "iot/device1",
    "Temperature Data: 25C"
)

print("Message published successfully")

# Give time for message to be sent/received
time.sleep(2)

# Stop network loop
client.loop_stop()

# Disconnect
client.disconnect()


#--------d. Packet Sniffing to Demonstrate Unsecured IoT Traffic

from scapy.all import sniff

def packet_callback(packet):
    if packet.haslayer("IP"):
        src = packet["IP"].src
        dst = packet["IP"].dst

        print(f"[IP Packet] {src} → {dst}")

        if packet.haslayer("Raw"):
            payload = packet["Raw"].load
            print("Payload:", payload)

print("Sniffing IoT traffic... Press Ctrl+C to stop")

sniff(prn=packet_callback, count=10)


#------Practical 8 – Security Practices

#----a. Demonstrating a Hash Collision

# toy_collision_demo.py

# Educational demo:
# Two different "certificate" byte-strings
# that produce the same value using a weak toy hash.

def toy_hash(b: bytes) -> int:
    """
    Very weak toy hash:
    sum of bytes modulo 256.

    This is intentionally insecure and collision-prone.
    """
    return sum(b) % 256

def make_base_certs():

    # First certificate-like text
    cert1_txt = """-----BEGIN CERTIFICATE-----
Subject: CN=Alice Example
Issuer: Test CA
PublicKey: AAAAB3NzaC1yc2EAAAADAQABAAABAQCu
-----END CERTIFICATE-----
"""

    # Second certificate-like text
    cert2_txt = """-----BEGIN CERTIFICATE-----
Subject: CN=Bob Example
Issuer: Test CA
PublicKey: AAAAB3NzaC1yc2EAAAADAQABAAABAQCu
-----END CERTIFICATE-----
"""

    return cert1_txt.encode("utf-8"), cert2_txt.encode("utf-8")

def pad_to_match(hash_target: int, current_bytes: bytes) -> bytes:

    cur = sum(current_bytes) % 256

    needed = (hash_target - cur) % 256

    if needed == 0:
        return b''

    return bytes([needed])

def main():

    # Create two certificates
    cert1, cert2 = make_base_certs()

    # Calculate initial hashes
    h1 = toy_hash(cert1)
    h2 = toy_hash(cert2)

    print("Initial toy hashes:")
    print("cert1 hash:", h1)
    print("cert2 hash:", h2)
    print()

    # Make cert2 hash equal to cert1
    padding = pad_to_match(h1, cert2)

    cert2_padded = cert2 + b"\n#PAD:" + padding

    # Calculate hash again
    h2_after = toy_hash(cert2_padded)

    print("After padding cert2:")
    print("cert1 length:", len(cert1),
          "hash:", toy_hash(cert1))

    print("cert2_padded length:", len(cert2_padded),
          "hash:", h2_after)

    print()

    # Check whether files are actually identical
    print("Are bytes identical?:", cert1 == cert2_padded)

    # Check whether their toy hashes are equal
    print(
        "Do they collide under toy_hash?:",
        toy_hash(cert1) == toy_hash(cert2_padded)
    )

    print()

    # Show last bytes in hexadecimal
    def show_tail(b):
        tail = b[-40:]
        return tail.hex()

    print("tail(cert1) (hex):", show_tail(cert1))
    print("tail(cert2_p) (hex):", show_tail(cert2_padded))

    # Save the two files
    with open("cert1_demo.pem", "wb") as f:
        f.write(cert1)

    with open("cert2_demo_padded.pem", "wb") as f:
        f.write(cert2_padded)

    print()
    print("Wrote cert1_demo.pem and cert2_demo_padded.pem to disk.")

if __name__ == "__main__":
    main()


#------b. Computing Hash, MAC and HMAC

#hash

import hashlib

message = "Hello Security Students".encode()

hash_digest = hashlib.sha256(message).hexdigest()

print("Message:", message.decode())
print("SHA256 Hash:", hash_digest)

#hmac mac

import hmac, hashlib
 
key = b'super_secret_key'
msg = b'Authenticate this message'
 
hmac_digest = hmac.new(key, msg, hashlib.sha256).hexdigest()
print("HMAC:", hmac_digest)

#-----c. Key Differences Between Hash, MAC and HMAC

#---------------Practical 9 – Penetration Testing


#----------a. Port Scanning, Banner Grabbing and Vulnerability Checking

from datetime import datetime
import socket

# Database of known vulnerable service banners
vulnerabilities = {
    "Apache/2.2.8": "Outdated Apache version - vulnerable to CVE-2009-3555",
    "OpenSSH_4.7": "Old OpenSSH version - possible remote exploits",
    "Microsoft-IIS/6.0": "IIS 6.0 is deprecated - vulnerable to multiple attacks",
}

def scan_ports(target, ports):
    open_ports = []
    print(f"\n[*] Scanning {target} ...")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"[+] Port {port} is OPEN")
                open_ports.append(port)
            sock.close()
        except Exception:
            pass
    return open_ports



def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode().strip()
        sock.close()
        return banner
    except Exception:
        return None

def check_vulnerabilities(banner):
    for vuln in vulnerabilities:
        if vuln in banner:
            return vulnerabilities[vuln]
    return "No known vulnerability in database."

if __name__ == "__main__":
    target = input("Enter Target IP (e.g., 127.0.0.1): ")
    ports_to_scan = [21, 22, 23, 25, 80, 110, 143, 443, 3389]

    start_time = datetime.now()

    open_ports = scan_ports(target, ports_to_scan)

    print("\n[*] Banner Grabbing and Vulnerability Check:")
    for port in open_ports:
        banner = grab_banner(target, port)
        if banner:
            print(f"\n[Port {port}] Service Banner: {banner}")
            print(" -> " + check_vulnerabilities(banner))
        else:
            print(f"\n[Port {port}] No banner retrieved.")

    end_time = datetime.now()
    print("\n[*] Scan completed in:", end_time - start_time)

#---b. FTP Login/Credential Testing
#---c. SQL Injection Testing
#---d. Directory Enumeration / Directory Brute Forcing

#Port Scanning and Vulnerability
#scan_ports() – Finds open ports.
#grab_banner() – Gets service information.
#check_vulnerabilities() – Checks vulnerable software versions
import socket
from datetime import datetime

# Vulnerability database
vulnerabilities = {
    "Apache/2.2.8": "Outdated Apache version",
    "OpenSSH_4.7": "Old OpenSSH version",
    "Microsoft-IIS/6.0": "Outdated IIS version"
}

# Scan ports
def scan_ports(target, ports):
    open_ports = []

    print("\nScanning ports...")

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))

        if result == 0:
            print("Port", port, "is OPEN")
            open_ports.append(port)

        sock.close()

    return open_ports


# Get service banner
def grab_banner(target, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((target, port))

        banner = sock.recv(1024).decode().strip()
        sock.close()

        return banner

    except:
        return None


# Check vulnerabilities
def check_vulnerabilities(banner):
    for version in vulnerabilities:
        if version in banner:
            return vulnerabilities[version]

    return "No known vulnerability"


# Main program
if __name__ == "__main__":

    target = input("Enter Target IP: ")

    ports = [21, 22, 23, 25, 80, 110, 143, 443, 3389]

    start_time = datetime.now()

    open_ports = scan_ports(target, ports)

    print("\nBanner Checking")

    for port in open_ports:
        banner = grab_banner(target, port)

        if banner:
            print("\nPort:", port)
            print("Banner:", banner)
            print("Vulnerability:", check_vulnerabilities(banner))

        else:
            print("Port", port, "- No banner")

    end_time = datetime.now()

    print("\nScan completed")
    print("Time taken:", end_time - start_time)
#use 127.0.0.1for testing for output


    
#Combined Vulnerability Scanning

import socket
import requests
import ftplib
from datetime import datetime

# Vulnerability database
vulnerabilities = {
    "Apache/2.2.8": "Old Apache version",
    "OpenSSH_4.7": "Old OpenSSH version",
    "Microsoft-IIS/6.0": "Old IIS version"
}

# 1. Port scanning
def scan_ports(target, ports):
    open_ports = []

    print("\nScanning ports...")

    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(0.5)

            result = sock.connect_ex((target, port))

            if result == 0:
                print("Open Port:", port)
                open_ports.append(port)

            sock.close()

        except:
            pass

    return open_ports


# 2. Banner grabbing
def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))

        banner = sock.recv(1024).decode().strip()
        sock.close()

        return banner

    except:
        return None


# 3. Vulnerability checking
def check_vulnerabilities(banner):
    for version in vulnerabilities:
        if version in banner:
            return vulnerabilities[version]

    return "No known vulnerability"


# 4. FTP login testing (localhost only)
def ftp_bruteforce(target, user, wordlist):
    print("\nFTP Login Testing")

    for password in wordlist:
        try:
            ftp = ftplib.FTP(target, timeout=2)
            ftp.login(user, password)

            print("Login successful:", user, password)
            ftp.quit()
            return

        except:
            print("Login failed:", password)

    print("No valid credentials found")


# 5. SQL injection testing (local test application)
def sql_injection_test(url, param):
    print("\nSQL Injection Testing")

    payloads = ["' OR 1=1 -- ", "' OR 'x'='x"]

    for payload in payloads:
        try:
            new_url = f"{url}?{param}={payload}"
            r = requests.get(new_url, timeout=3)

            if "error" in r.text.lower():
                print("Possible SQL error detected")
            else:
                print("No SQL error detected")

        except:
            print("Request failed")


# 6. Directory checking
def dir_bruteforce(url, wordlist):
    print("\nDirectory Checking")

    for word in wordlist:
        try:
            test_url = f"{url}/{word}"
            r = requests.get(test_url, timeout=3)

            if r.status_code == 200:
                print("Found:", test_url)

        except:
            pass


# MAIN PROGRAM
if __name__ == "__main__":

    target = "127.0.0.1"

    ports = [21, 22, 23, 25, 80, 110, 143, 443, 3389]

    start_time = datetime.now()

    # Port scanning
    open_ports = scan_ports(target, ports)

    # Banner checking
    print("\nBanner Checking")

    for port in open_ports:
        banner = grab_banner(target, port)

        if banner:
            print("Port:", port)
            print("Banner:", banner)
            print("Result:", check_vulnerabilities(banner))
        else:
            print("No banner found")

    # FTP testing - localhost only
    ftp_wordlist = ["1234", "admin", "password", "toor"]
    ftp_bruteforce(target, "admin", ftp_wordlist)

    # SQL testing - local application only
    sql_injection_test("http://127.0.0.1/vulnerable.php", "id")

    # Directory checking - local application only
    wordlist = ["admin", "login", "test", "uploads"]
    dir_bruteforce("http://127.0.0.1", wordlist)

    end_time = datetime.now()

    print("\nScan completed")
    print("Time taken:", end_time - start_time)

