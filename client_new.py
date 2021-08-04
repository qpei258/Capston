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
        print("서버 {ip}에 연결되었습니다. 포트 번호 : {port}".format(ip=SERVER_IP, port=SERVER_PORT))

        #filename = input('전송할 파일명 입력 : ')

        with open("E:/caps/test.jpg", 'rb') as f:
            filesize = getsize("E:/caps/test.jpg")
            print("파일크기 : {}바이트".format(filesize))
            client_socket.send((str(filesize)+'\n').encode())
            try:
                numtotal = 0
                data = f.read(4096)
                while (data):
                    numtotal += client_socket.send(data)
                    time.sleep(0.15)
                    print("{}/{}바이트 전송됨".format(numtotal, filesize))
                    data = f.read(4096)
                print("{} 전송완료.".format("E:/caps/test.jpg"))
                print()
            except Exception as ex:
                print(ex)
        f.close()
        client_socket.send(('nofile'+'\n').encode())
        print("전체 파일 전송 완료.")
        print()
        result = client_socket.recv(1024)
        client_socket.close()
        print("서버 {ip}와 연결이 해제되었습니다. 포트 번호 : {port}".format(ip=SERVER_IP, port=SERVER_PORT))
        time.sleep(3)

        return result.decode()