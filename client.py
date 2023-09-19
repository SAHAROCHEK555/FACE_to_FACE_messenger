import socket
import threading
from datetime import datetime
import eel


messages = []

host = '192.168.0.31'
port = 8000

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg2 = ''

class Listen_class: 
    def listen(self):
        global msg2
        while True:
            msg = soc.recv(1024)
            if msg.decode("utf-8").startswith("SIGNIN_TAG:"):
                print(msg.decode("utf-8"))
                name = msg.decode('utf-8')[msg.decode('utf-8').index(':')+1:]      
                sending_messages_class_copy.get_name(name) 
            else:
                msg2 = msg.decode("utf-8")
                print(msg2)    

listen_class_copy = Listen_class()

@eel.expose()
def print_msg():
    return msg2

soc.connect((host, port))
threading.Thread(target = listen_class_copy.listen, daemon=True).start()

soc.send(f'OPEN_TAG:'.encode('utf-8'))

class Sending_messages:
    def get_name(self, nickname_for_listen):
        self.nickname = nickname_for_listen    
    def nickname_func(self):    
        @eel.expose()
        def send_msg(msg1):
            time2 = datetime.now()
            soc.send(f'[{time2.hour}:{time2.minute}:{time2.second}] {self.nickname}: {msg1}'.encode('utf-8'))
            return f"{self.nickname}: {msg1}"
        
sending_messages_class_copy = Sending_messages()

class Connect_to_html:  
    def func_union_html_files(self):
        
        eel.init('web')
        
        @eel.expose
        def sign_up2(password, name_sg_up):
            soc.send(f'SIGNUP_TAG: {password} {name_sg_up}'.encode('utf-8'))
            sending_messages_class_copy.nickname_func()
            soc.send("STORY_TAG".encode('utf-8'))
        @eel.expose
        def login(password2):
            soc.send(f'SIGNIN_TAG: {password2}'.encode('utf-8'))   
            sending_messages_class_copy.nickname_func()
            soc.send("STORY_TAG".encode("utf-8"))
            
        eel.start("main_sign_in.html", size=(420, 800), port=0000)

if __name__ == "__main__":
    connect_to_html_class_copy = Connect_to_html()
    connect_to_html_class_copy.func_union_html_files()