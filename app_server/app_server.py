import socket
import app_oracle_function as of
import sys


HOST = ""
PORT = 8081
SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

while True:
    client_socket, addr = server_socket.accept() #클라이언트 연결 대기

    code = client_socket.recv(SIZE).decode('utf-8')# 클라이언트로부터 문자열을 받고 @를 기준으로 문자열을 배열에 저장
    print(code)
    client_socket.sendall(''.encode())

    if code == "00":
        print("회원가입")

        userdata = client_socket.recv(SIZE).decode('utf-8').split('@')
        for data in userdata:
            print(data)

        id = userdata[0]
        pw = userdata[1]
        name = userdata[2]
        phone = userdata[3]
        gender = userdata[4]
        agency = userdata[5]
        admin = userdata[6]

        of.insert_user(id, pw, name, phone, gender, agency, admin)
        of.commit()
        client_socket.sendall(' '.encode())
        filesize = client_socket.recv(SIZE).decode('utf-8')
        print(filesize)

        with open("D:/caps/test.mp4", 'wb') as f:  # 이미지 파일 저장 위치 지정
            try:
                recvdata = 0
                datasize = 0
                while True:
                    data = client_socket.recv(SIZE)
                    f.write(data)
                    recvdata = sys.getsizeof(data)
                    datasize += recvdata
                    print("{}/{}바이트 수신됨".format(datasize, filesize))
                    if datasize >= int(filesize):
                        break
            except Exception as e:
                print(e)
        print("파일 수신 완료")


        #학습 프로그램 추가

    elif code == "01":
        print("로그인")

        idPw = client_socket.recv(SIZE).decode().split('@')
        id = idPw[0]
        pw = idPw[1]

        print(id)
        print(pw)

        user = of.select_pw_where_id(id)
        print(user)

        if user == None:
            admin = 'fail'
        else:
            if pw != user[1]:
                admin = 'fail'
            else:
                admin = user[7]

        print(admin)
        client_socket.sendall(admin.encode())
        #아이디 비번으로 어드민값 리턴, 3는 로그인 실패 2는 관리자, 1은 사용자


    elif code == "02":
        print("회원 정보 보내기")

        id = client_socket.recv(SIZE).decode()

        userdata = of.select_all_where_id(id)
        name = userdata[2]
        phone = userdata[4]
        agency = userdata[6]

        data = name + '@' + phone + '@' + agency
        client_socket.sendall(data.encode())

    elif code == "03":
        print("회원 정보 수정")
        data = client_socket.recv(SIZE).decode().split('@')

        of.update_where_id(data[1], data[2], data[3], data[0])
        of.commit()

    elif code == "04":
        print("출입 목록")
        id = client_socket.recv(SIZE).decode()        #로그인 아이디를 전송받음
        print(id)
        # 관리자 이름, 출입 목록 전송
        user = of.select_pw_where_id(id)
        name = user[2]
        print(name)        #아이디에 해당하는 이름을 반환

        #전체 출입 횟수를 앱으로 전송
        count = str(of.select_count_records())
        print(count)
        data = name + '@' + count
        client_socket.sendall(data.encode())
        print(data)

        #출입 기록을 앱으로 전송
        cursor = of.entrance_records_return()
        result = cursor.fetchall()
        client_socket.recv(SIZE)
        for record in result:
            date = record[2].split(' ')
            data = record[0] + "@" + record[1] + "@" + date[0] + "@" + date[1]
            client_socket.sendall(data.encode())
            client_socket.recv(SIZE)

    else:
        print("잘못된 입력")
