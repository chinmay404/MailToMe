import socket
import sqlite3
import ssl
import threading
import smtplib
import pickle
import os
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Database
print("[+] Database intializing ....")
try:
    conn = sqlite3.connect('mailtome.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS email (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT,
                    body TEXT,
                    recipient TEXT,
                    attachment_name TEXT
                )''')
    conn.commit()
    print("[+] Database Connected")
except :
    print("[-] Database Failure.")


SENDER_MAIL = 'mailtome1718@gmail.com'
SENDER_PASSWORD = ''
FORMAT = 'utf-8'
disconnect_message = "[-] Connection Closed By server"

# Initialize SMTP server
print("[+] Login SMTP ....")
context = ssl.create_default_context()
smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
smtp_server.login(SENDER_MAIL, SENDER_PASSWORD)
print("[+] Login Successful")


def send_mail(client_socket, addr):
    c2 = conn.cursor()
    BUFFER_SIZE = 2048
    data = b''
    bytes_received = 0
    print("[+] Reciving......")
    while True:
        file_data = client_socket.recv(BUFFER_SIZE)
        if not file_data:
            print("[+] File End.")
            break
        else:
            data += file_data
            bytes_received += len(data)
    print(f"[+] Recived : {bytes_received}")
    data = pickle.loads(data)
    subject = data[0]
    
    body = data[1] + "\n\n\nFrom Mailtome.com"
    recipient = data[2]

    print(f'[*] User : {addr} ')
    msg = EmailMessage()
    msg['From'] = SENDER_MAIL
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)
    if data[4] is not None:
        msg.add_attachment(data[4], maintype='application',
                           subtype='octet-stream', filename=data[3])
        c.execute('INSERT INTO email (subject, body, recipient, attachment_name) VALUES (?, ?, ?, ?)',
                  (subject, body, recipient, data[3]))
    c.execute('INSERT INTO email (subject, body, recipient, attachment_name) VALUES (?, ?, ?, ?)',
              (subject, body, recipient, data[3]))
    conn.commit()
    # c.close()
    try:
        smtp_server.send_message(msg)
        print(f"[+] Mail Sent To : {recipient} ")
        # client_socket.close()
    except:
        print("[-] Error Send Mail")

    print(f"[+] {addr} : disconnected")
    print(f"[+] [ACTIVE] : {threading.active_count() - 1}")
    if client_socket.fileno() != -1:
        client_socket.close()
        print(f"[*] Disconnect Forcefully : {addr}")


def handle_client(conn, addr):
    print(f"[+] {addr} : connected.")
    send_mail(conn, addr)


def start():
    server.listen()
    print(f"[+] listening : {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        # print(conn, addr)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[+] [ACTIVE] : {threading.active_count() - 1}")


# Server socket
HEADER = 64
PORT = 5090
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "quit"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print("[+] server is starting...")
start()
