# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 21:23:22 2021

@author: Subhikshaa
"""

import os
import socket
import sys
import string
import random

HOST = socket.gethostbyname(socket.gethostname())
PORT = 23
address = (HOST, PORT)
buffer_size = 4000

all_letters= string.ascii_letters   
spl_char=[' ','~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']
dict1 = {}

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    while True:
        server_data = sock.recv(buffer_size).decode()
        if server_data:
            print("************************************************")
            print("Message from server :-")
            print(server_data)
        print("************************************************")
        print("\nType help to see available commands :)\n")
        user_inp = input("telnet> ")
        data = user_inp.split()
        command = data[0]
        
        if command=="exec":
            sock.send(user_inp.encode('utf-8'))
            
        elif command=="send":
            sock.send(user_inp.encode('utf-8'))
            
        elif command=="encrypt":
            key = random.randint(1,15)
            for i in range(len(all_letters)):
                dict1[all_letters[i]] = all_letters[(i+key)%len(all_letters)]
            for i in range(len(spl_char)):
                dict1[spl_char[i]] = spl_char[(i+key)%len(spl_char)]
                
            msg=" ".join(data[i] for i in range(1,len(data)))
            enc_txt=""
            for char in msg:
                if char in all_letters:
                    temp = dict1[char]
                elif char in spl_char:
                    temp = dict1[char]
                else:
                    temp = char 
                enc_txt+=temp
            final_msg="encrypt "+str(key)+" "+enc_txt
            sock.send(final_msg.encode('utf-8'))
            
        elif command=="help":
            sock.send(user_inp.encode('utf-8'))
            
        elif command=="history":
           sock.send(user_inp.encode('utf-8'))
        
        elif command == "quit":
            sock.send(user_inp.encode('utf-8'))
            sys.exit()
            
        elif command == "upload":
            f_name = data[1]
            if os.path.isfile(f_name):
                f_size = os.path.getsize(f_name)
                user_inp += ":" + str(f_size)
                sock.send(user_inp.encode())
                msg = sock.recv(buffer_size).decode()
                print(msg)
    
                with open(f_name, "rb") as f:
                    while True:
                        dt = f.read(buffer_size)
    
                        if not dt:
                            #sock.send("DATA OVER".encode())
                            break
                        sock.sendall(dt)
                        msg1 = sock.recv(buffer_size).decode()
                        print(msg1)
            else:
                print("File does not exist.......\n")
                break
                    
        elif command=="download":
            sock.send(user_inp.encode('utf-8'))
            fileexists=sock.recv(buffer_size).decode()
            if fileexists=="File exists":
                name=f"recvd_{data[1]}"
                filepath = os.path.join("client_data", name)
                filesize=sock.recv(buffer_size).decode()
                filesize=int(filesize)
                size_tmp=0
                with open(filepath, "wb") as f:
                    while True:
                        file_data = sock.recv(buffer_size)
                        size_tmp += len(file_data)
                        print(size_tmp, " bytes have been received so far")
                        if not file_data:
                            break
                        if file_data == b'DATA OVER':
                            break
                        f.write(file_data)
                        
                        if size_tmp >= filesize:
                            break
                print("File downloaded from Server successfully!!")
                print("File saved at locaton : ",filepath)
                sock.send("File downloaded from server Successfully!!".encode('utf-8'))
            elif fileexists=="File does not exist":
                print("Provided file name does not exist in the server...")
                break
        else:
            print("Invalid command......")
            break
            
    sock.close()
        
        