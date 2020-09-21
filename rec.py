from threading import Thread#needed libraries
import sys, os
import socket

HOST = ""

def change_name(name):#function for changing the name of the file
    if os.path.exists(name):#in case file with such a name exists we change its name
        i = 1
        new_name=name
        while os.path.exists(new_name):
            if "." in name:#splitting the filename by '.' symbol if it has an extension
                no_ext = "".join(name.split(".")[:-1])#inserting '_c' mark before extension
                ext = name.split(".")[-1]
                new_name = no_ext+"_c"+str(i)+"."+ext
            else:
                new_name = no_ext+"_c"+str(i)#just adding '_c' mark in case if ther is no extension
            i += 1
        return new_name
    else:
        return name


def download_file(con, addr):#function for downloading the file
    with con:
        print("Receiving from ", addr)
        size = int.from_bytes(con.recv(1), 'big')#get the size of the file
        name = (con.recv(size)).decode()#get the name of the file
        name = change_name(name)#in case if file with such name already exists we change its name
        with open(name, "wb") as file:#recieving data and writing it
            while True:
                d = con.recv(1024)
                if not d:
                    break
                file.write(d)
        print(name, " is downloaded.")


if __name__ == "__main__":
    port = int(sys.argv[1]) #getting our port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:#socket
        sock.bind((HOST, port))
        while True:#listen
            sock.listen(1)
            con, addr = sock.accept()
            thread = Thread(target=download_file, args=(con, addr))#downloading a file in a separate thread
            thread.start()