import nacl.utils as pynacl
import socket

def getRand() -> str:
    bs = pynacl.random(size=128)
    r = 0
    for c in bs:
        r += c
    return '{0:X}'.format(r)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 65432))
    s.listen()
    c,a = s.accept()
    print(f"{a} conectado")
    
    filename = c.recv(1024).decode()
    filename = filename.replace(".txt", "_serv.txt")
    c.send("a".encode())
    f = open(filename, "wb")
    f.write(c.recv(1024))
    
    c.close()
    s.close()
