import nacl.utils as pynacl
import nacl.secret as pysecret
import socket
from Crypto.Cipher import ChaCha20

def getRand() -> str:
    bs = pynacl.random(size=128)
    r = 0
    for c in bs:
        r += c
    return '{0:X}'.format(r)

if __name__ == "__main__":
    key = pynacl.random(pysecret.SecretBox.KEY_SIZE)
    cipher = ChaCha20.new(key=key)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 65432))
    s.listen()
    c,a = s.accept()
    print(f"{a} conectado")
    
    filename = c.recv(1024).decode()
    filename = filename.replace(".txt", "_serv.txt")
    c.send("a".encode())
    f = open(filename, "wb")
    data = c.recv(1024)
    encryptedData = cipher.encrypt(data)
    f.write(encryptedData)
    
    c.close()
    s.close()
