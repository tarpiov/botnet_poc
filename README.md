# Tutorial de uso:

En este repositorio se nos presentan 3 archivos:
- `server.py` -> Servidor en escucha de conexiones de bots. *(IP y Puerto configurables)*
- `target.py` -> Archivo a ejecutar por el bot (pruebalo en maquina virtual o con tu propio entorno).
- `admin.py`  -> Command&Control, encargado de enviar ordenes al servidor.

>Primero debemos ejecutar el `server.py` y el `admin.py` en nuestra máquina local, posteriormente se ejecutará el `target.py`en la maquina víctima

Dentro del `server.py` se registrarán los logs y aparecerán en pantalla.

--- 

# Admin

<img src="https://i.imgur.com/67oyEu4.png" width=600px>

El admin se conectará de la misma forma que hace el bot, pero con la diferencia que el admin envía una clave de administrador "`poc`" con la cual el server interpretará de que se trata del administrador y no de un bot. (Por el contrario, el bot envía "`bot`")

> El archivo `admin.py` cuenta con varios comandos para las comunicaciones de la botnet

- `clear` -> Limpiar la pantalla.
- `help` -> Ver el banner de ayuda de comandos.
- `show` -> Ver conexiones activas de los bots.
- `connect` -> Conectarse a un bot mediante su puerto tcp.
	- Cuando se escribe el comando deberás escribir el puerto después, y si todo va bien ganarás acceso a la máquina. Para salir del Command&Control usa `exit`
- `bye` -> Salir
