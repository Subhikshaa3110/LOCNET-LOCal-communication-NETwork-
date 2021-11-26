# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 22:09:02 2021

@author: Subhikshaa
"""

import os
import socket
import sys


HOST = socket.gethostbyname(socket.gethostname())
PORT = 23
address = (HOST, PORT)
buffer_size = 4000

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    while True:
        server_data = sock.recv(buffer_size).decode()
        if server_data:
            print("************************************************")
            print("Message from server :-")
            print(server_data)

        print("\n1-Send Request to http web server(GET/HEAD)\n2-scan ip for open ports\n3-quit")
        c = input(">")

        if c == '1':
            print("command structure: <Request type> <host>")
            cmd = input("Telnet> ")
            sock.send(cmd.encode('utf-8'))

        elif c == '2':
            print("command structure: scan <host> <start port> <end port>")
            cmd = input("Telnet> ")
            sock.send(cmd.encode('utf-8'))
        
        elif c=='3':
            sock.send(b'quit')
            sys.exit()
            
        else:
            print("Invalid option....")
            break
            
    sock.close()
            
