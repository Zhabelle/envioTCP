import nacl.utils as pynacl
import nacl.secret as pysecret
import socket, time
from Crypto.Cipher import ChaCha20
from nacl.signing import SigningKey, VerifyKey


userData = {
    "taqueches": "barbacha",
    "fido": "el_perro",
    "a": "b"
}

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 65432))
    s.listen()
    c,a = s.accept()
    print(f"{a} conectado")

#   Nombre de usuario y contraseña
    print("\n-Nombre de usuario y contraseña")
    loginData = c.recv(1024).decode().strip("()").replace("'","").split(", ")
    loginError = loginData[0] not in userData.keys() or userData[loginData[0]] != loginData[1]
    if not loginError:
        c.sendall("autenticación existosa".encode())
    
#   Bitácora de accesos (logs)
    print("\n-logs")
    mensaje = f"[{time.strftime('%d.%m.%G-%H:%M:%S')}] [{'WARN' if loginError else 'INFO'}] \"{loginData[0]}\" ha {'intentado iniciar' if loginError else 'iniciado'} sesión.\n"
    f = open("bitácora.txt", "a", encoding='utf-8')
    f.write(mensaje)
    print(mensaje)
    f.close()

    if loginError:
        c.close()
        s.close()
        raise Exception("Error de autenticación")
    
#   Generación y Recuperación de Claves hacia o desde 1 archivo
    print("\n-Generación y Recuperación de Claves hacia o desde 1 archivo")
    
#   Cifrado de Archivos
    print("-Cifrado de archivo")
    filename = "serv_file.txt"
    f = open(filename, "wb")
    data = c.recv(1024)
    if len(data.decode()) < 1:
        raise Exception("No se recibieron datos")
    
    key = pynacl.random(pysecret.SecretBox.KEY_SIZE)
    cipher = ChaCha20.new(key=key)
    encryptedData = cipher.encrypt(data)
    nonce = cipher.nonce
    print(encryptedData)
#   Descifrado de Archivos
    print("\n-Decifrado de archivo")
    cipher = ChaCha20.new(key=key, nonce=nonce)
    decryptedData = cipher.decrypt(encryptedData)
    print(decryptedData)
#   Firma de Archivos
    print("\n-Firma de archivo")
    sign_key = SigningKey.generate()
    signedData = sign_key.sign(encryptedData)
    print(signedData)
    f.write(signedData)
#   Verificación de Firma de Archivos
    print("\n-Verificación de firma")
    verify_key = VerifyKey(sign_key.verify_key.encode())
    print(verify_key.verify(signedData))
    
    c.close()
    s.close()
