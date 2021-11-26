# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 20:04:58 2021

@author: Subhikshaa
"""

import threading
import os
import subprocess
import socket
from database import *
from datetime import datetime, date
import time
import string

HOST = socket.gethostbyname(socket.gethostname())
PORT = 23
address = (HOST, PORT)
buffer_size = 4000

all_letters= string.ascii_letters   
spl_char=[' ','~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']
dict2 = {}  

def client_thread(conn,addr):
    print(f"**Connected to {addr}**")
    conn.send("Welcome from Server".encode('utf-8'))
    while True:
        print("*********************************************************")
        data = conn.recv(buffer_size).decode()
        data = data.split()
        command = data[0]
        print(f"Command : {command}")
        
        conn_accepted=False
        
        if command=="exec":
            exec_msg = " ".join(data[i] for i in range(1,len(data)))
            result = subprocess.run(exec_msg, stdout=subprocess.PIPE)
            output = result.stdout.decode()
            output = "Command executed" + output
            conn.send(output.encode('utf-8'))
            print("Command executed and sent output to client successfully")
            conn_accepted=True
            
        elif command=="send":
            client_msg="Message recieved"
            print("Message from client : ",*data[1:])
            conn.send(client_msg.encode())
            conn_accepted = True
            
        elif command=="help":
            help_str = "Available commands:-\nupload <filename> : Upload the file\ndownload <filename> : download the file\nexec <command>:execute command and send output\n" \
                       "send <text> : send plain text message\nencrypt <text> : send encrypted text message" \
                       "\nGET/HEAD <host>: send request to web server\nscan <host> <start port> <end port>:scan ports start_port to end_port"\
                       "\nhistory : show the history\n"
            conn.send(help_str.encode('utf-8'))
            conn_accepted = True
            
        elif command=="history":
            histories = print_history_table(db_cursor)
            conn.send(("History table:-\n" + histories).encode('utf-8'))
            conn_accepted = True
        
        elif command == "quit":
            print("Closing connection......")
            conn.send(b"SERVER DISCONNECTED.....")
            conn_accepted = True
            break
        
        elif command=="encrypt":
            key=int(data[1])
            enc_txt=" ".join(data[i] for i in range(2,len(data)))
            print("Encrypted Message from client : ",enc_txt)
            for i in range(len(all_letters)):
                dict2[all_letters[i]] = all_letters[(i-key)%(len(all_letters))]
            for i in range(len(spl_char)):
                dict2[spl_char[i]] = spl_char[(i-key)%len(spl_char)]
            dec_txt=""
            for char in enc_txt:
                if char in all_letters:
                    temp = dict2[char]
                elif char in spl_char:
                    temp = dict2[char]
                else:
                    temp = char
                dec_txt+=temp
            client_msg="Message recieved"
            print("Decrypted Message from client : ",dec_txt)
            conn.send(client_msg.encode())
            conn_accepted=True
        
        elif command == "upload":
            path = data[1]
            filename, filesize = path.split(":")
            filesize = int(filesize)
            conn.send("Filename and filesize received".encode())
            size_tmp = 0
            name = f"recvd_{filename}"
            filepath = os.path.join("server_data", name)
            with open(filepath, "wb") as f:
                while True:
                    file_data = conn.recv(buffer_size)
                    size_tmp += len(file_data)
                    print(size_tmp, " bytes have been received so far")
                    if not file_data:
                        break
                    if file_data == b'DATA OVER':
                        break
                    f.write(file_data)
                    conn.send("Data received".encode('utf-8'))
                    if size_tmp >= filesize:
                        break
            conn.send("File is uploaded at Server successfully!!".encode())
            print("File uploaded at Server successfully!!")
            print("File saved at locaton : ",filepath)
            conn_accepted = True
            
        elif command=="download":
            filename=data[1]
            if os.path.isfile(filename):
                conn.send("File exists".encode("utf-8"))
                f_size=os.path.getsize(filename)
                conn.send(str(f_size).encode("utf-8"))
                with open(filename, "rb") as f:
                    while True:
                        dt = f.read(buffer_size)
    
                        if not dt:
                            conn.send("DATA OVER".encode())
                            break
                        conn.sendall(dt)
                        msg1 = conn.recv(buffer_size).decode()
                        print(msg1)
            else:
                conn.send("File does not exist".encode("utf-8"))
            conn_accepted=True
            
        elif command=="GET" or command=="HEAD":
            ip = data[1]
            target_port = 80
            http_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                http_client.connect((ip, target_port))
            except socket.gaierror:
                conn.send(b'Hostname could not be resolved')
                print("Hostname could not be resolved")
                break
            request = command + " / HTTP/1.1\r\nHost:+ " + ip + "\r\nAccept: text/html\r\n\r\n"
            http_client.sendall(request.encode('utf-8'))
            recvd_data=http_client.recv(buffer_size)
            conn.send(recvd_data)
            http_client.close()
            conn_accepted=True
            
        elif command=="scan":
            host=data[1]
            startport=int(data[2])
            endport=int(data[3])
            start_time = time.time()
            try:
                target_host = socket.gethostbyname(host)
            except socket.gaierror:
                conn.send(b'Hostname could not be resolved')
                break
                
            print("Starting scan for host:", target_host)
            flag=0
            for i in range(startport, endport+1):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                conn1 = s.connect_ex((target_host, i))
                if conn1 == 0:
                    flag=1
                    op=f"Port {i}: OPEN"
                    conn.send(op.encode("utf-8"))
                s.close()
            if flag==0:
                op=f"No open ports......\nTime taken: {time.time() - start_time}"
            else:
              op=f"Time taken: {time.time() - start_time}"  
            conn.send(op.encode("utf-8"))
            conn_accepted=True
            
        else:
            conn.send(b'Invalid command...')
            
        if conn_accepted:
            now = datetime.now()
            curr_time = now.strftime("%H:%M:%S")
            today = date.today()
            tdy_date = today.strftime("%d/%m/%Y")
            insert_record(db_cursor, str(addr[1]), command, curr_time, tdy_date)
            
    conn.close()
        

            
def start(address,HOST):
    print("TELNET SERVER STARTING...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(address)
    server_socket.listen(4)
    print("LISTENING...")
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=client_thread, args=(conn, addr))
        thread.start()

        

start(address,HOST)
