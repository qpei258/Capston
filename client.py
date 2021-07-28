import socket

HOST = '127.0.0.1'
PORT = 8081


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("파일 전송 시작")
with open("E:/caps/test.jpg", 'rb') as f:
    try:
        data = f.read(1024)
        while data:
            data_transferred = client_socket.send(data)
            data = f.read(1024)
    except Exception as e:
        print(e)
print("파일 전송 완료")

client_socket.settimeout(3)
message = client_socket.recv(1024)

print(message.decode())


client_socket.close()
