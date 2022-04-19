import socket
import zono.zonocrypt
import pynput.keyboard as keyboard
import pynput.mouse as mouse 
import threading



kbd = keyboard.Controller()
mc = mouse.Controller()

objcrypt = zono.zonocrypt.objcrypt(
    hash_algorithm=zono.zonocrypt.objcrypt.SHA512)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
ipaddr = s.getsockname()[0]
s.close()

IP = ipaddr
PORT = 4245
HEADER = 512
FORMAT = 'utf-8'
IP_GLOBAL = IP
print(IP)

actions = dict(
    release=kbd.release,
    press=kbd.press,
    press_mouse=mc.press,
    release_mouse=mc.release,
    move=lambda x:mc.move(x[0],x[1])
)



def send_raw(pkt, conn):
    message = objcrypt.encode(pkt)
    msg_length = len(message)

    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    conn.send(send_length)
    conn.send(message)


class CloseExc(Exception):
    pass

def recv_raw(client):
    try:
        msg_len = int(client.recv(HEADER).decode(FORMAT))
        msg = client.recv(msg_len)
        msg = objcrypt.decode(msg)
        return msg

    except:
        raise CloseExc()




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



def recv_loop(conn, addr):
    while True:
        try:
            pkt = recv_raw(conn)
            # actions[pkt['action']](pkt['inf'])
            print(pkt)
        except socket.error:
            return
        except CloseExc:
            return
        except Exception as e:
            print(e)

def accept_connections():
    server.listen()
    while True:
        conn, addr = server.accept()
        threading.Thread(target=recv_loop,args = (conn,addr)).start()


accept_connections()

