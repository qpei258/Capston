import socket
from os.path import exists, getsize
import sys
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8081
SIZE = 1024
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

def sendImage() :
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
try:
    client_socket.connect(SERVER_ADDR)
except Exception as ex:
    print(ex)
    with open("test.jpg", 'rb') as f:
        filesize = getsize("test.jpg")
        print("파일크기 : {}바이트".format(filesize))
        client_socket.send((str(filesize)).encode())
        try:
            numtotal = 0
            data = f.read(SIZE)
            while (data):
                numtotal += client_socket.send(data)
                data = f.read(SIZE)
        except Exception as ex:
            print(ex)
    f.close()
    result = client_socket.recv(SIZE).decode();
    client_socket.close()
    return result
