import socket

HOST = ""
PORT = 8081


def receive(socket):
    data = socket.recv(1024)
    with open("D:/caps/test.jpg", 'wb') as f:
        try:
            while data:
                f.write(data)
                data = socket.recv(1024)
        except Exception as e:
            print(e)
        f.flush()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

while True:
    client_socket, addr = server_socket.accept()
    receive(client_socket)

    client_socket.send('수신 완료'.encode())









