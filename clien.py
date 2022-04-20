import os
import socket


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 65432))
    f = open("datos.txt","rb")
    s.send((os.getcwd()+"\\"+f.name).encode())
    s.recv(1024)
    a = f.read()
    s.sendall(a)
    s.close()
