import os
import socket
import tkinter as tk
from tkinter import filedialog


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 65432))
    loginData = (input("Introduzca su nombre de usuario: "), input("Introduzca su contraseña: "))
    s.sendall(str(loginData).encode())
    if len(s.recv(1024).decode())<1:
        raise Exception("Error de autenticación")
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[("Text document", ".txt")], parent=root)
    if(file_path == None):
        raise Exception("Archivo no especificado")
    f = open(file_path,"rb")
    s.sendall(f.read())
    s.close()
