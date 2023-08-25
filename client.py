import socket
import threading
from datetime import datetime
import eel


messages = []

host = '192.168.0.31'
port = 8000

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
name = ""
msg2 = ''

def listen():
    global name
    global msg2
    while True:
        msg = soc.recv(1024)
        
        if msg.decode("utf-8").startswith("SIGNIN_TAG:"):
            name = msg.decode('utf-8')[msg.decode('utf-8').index(':')+1:]
            
        else:
            msg2 = msg.decode("utf-8")
            print(msg2)   

@eel.expose()
def print_msg():
    return msg2

soc.connect((host, port))
threading.Thread(target=listen, daemon=True).start()

soc.send(f'OPEN_TAG:'.encode('utf-8'))

def nickname_func(nickname):
    @eel.expose()
    def send_msg(msg1):
        time2 = datetime.now()
        soc.send(f'[{time2.hour}:{time2.minute}:{time2.second}] {nickname}: {msg1}'.encode('utf-8'))
        return f"{nickname}: {msg1}"


  
def union():
    
    eel.init('web')
    
    @eel.expose
    def sign_up(password, name_sg_up):
        soc.send(f'SIGNUP_TAG: {password} {name_sg_up}'.encode('utf-8'))
        eel.show("main_sign_in.html")
        
    @eel.expose
    def login(password2):
        if not name:
            pass
        soc.send(f'SIGNIN_TAG: {password2}'.encode('utf-8'))        
        nickname_func(name)
        eel.show('main_client.html')
    
    @eel.expose
    def sign_in2():
        eel.start("main_sign_in.html", size=(400, 800))
    eel.start("main_sign_up.html", size=(400, 800), port=0000)

if __name__ == "__main__":
    union()