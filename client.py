import socket
import threading
from datetime import datetime
import sqlite3
import eel
conn = sqlite3.connect('client&serverDB.db', check_same_thread=False)
cursor = conn.cursor()
def db_table_val(user_password: str, user_name: str):
    cursor.execute('INSERT INTO project (user_password, user_name) VALUES (?, ?)', (user_password, user_name))
    conn.commit()
messages = []
host = '192.168.0.31'
port = 8000
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg2 = ''
def listen():
    global msg2
    while True:
        msg = soc.recv(1024)
        msg2 = msg.decode("utf-8")
        print(msg2)
    
@eel.expose
def print_msg():
    return msg2
soc.connect((host, port))
threading.Thread(target=listen, daemon=True).start()
soc.send(f'SIGNUP_TAG:'.encode('utf-8'))
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
        db_table_val(user_password=password, user_name=name_sg_up)
        eel.show("main_sign_in.html")
    @eel.expose
    def login(password2):
        cursor.execute(f"SELECT user_name FROM project WHERE user_password == '{password2}'")
        user_ = cursor.fetchone()
        name = user_[0]
        if not user_:
            eel.show("main_sign_in.html")
        else:
            nickname_func(nickname=name)
            eel.show('main_client.html')
    @eel.expose
    def sign_in2():
        eel.start("main_sign_in.html", size=(400, 800))
    eel.start("main_sign_up.html", size=(400, 800), port=0000)
if __name__ == "__main__":
    union()