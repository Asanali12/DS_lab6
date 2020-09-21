from threading import Thread#needed libraries
import sys, os
import socket


def send_file(name, addr, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((addr, port))
        sock.sendall(len(name).to_bytes(1, 'big'))#send the name of the file
        sock.sendall(str(name).encode())#send the file itself
        actual = os.path.getsize(name)#getting the size of the file
        sending = 0#already sent data
        with open(name, "rb") as file:#opening file
            while 1 == 1:
                progress = (sending / actual) * 100#checking how much is sent
                print(progress,"%", " sent")
                buff = file.read(1024)#reading the file
                if not buff:
                    break
                sock.sendall(buff)#sending the data
                sending = sending + len(buff)#checking the amount sent
        print("Successfully sent a file.")


if __name__ == "__main__":
    file = sys.argv[1]
    addr = sys.argv[2]
    port = int(sys.argv[3])
    # create a separate thread for sending a file
    th = Thread(target=send_file, args=(file, addr, port))
    th.start()
    th.join()
    print("Exit")