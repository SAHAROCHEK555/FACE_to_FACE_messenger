import socket
import sqlite3
import random
max_size = 65535

conn = sqlite3.connect('client&serverDB.db', check_same_thread=False)
cursor = conn.cursor()
def db_table_val(soobzenia: str):
    cursor.execute('INSERT INTO all_mes (soobzenia) VALUES (?)', (soobzenia,))
    conn.commit()
    
def cvet(text):
    print("\033[34m\033[45m{}".format(text))

def listen(host: str = '192.168.0.31', port: int = 4555):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    soc.bind((host, port))
    print(f'Listening at {host}:{port}')
    

    messages = []
    memb = []
    
    while True:
            msg, addr = soc.recvfrom(max_size)
            
            if addr not in memb:
                memb.append(addr)
            
            if not msg:
                continue  
             

                     
            if msg.decode('utf-8').startswith('SIGNUP_TAG:'):
                name1 = msg.decode('utf-8')[msg.decode('utf-8').index(':')+1:]
                print(f'Client {name1} joined chat!')


            
            else:    
                for member in memb:
                    if member == addr:
                        continue
                    soc.sendto(msg, member)
                    messages.append(msg.decode('utf-8'))
                    db_table_val(soobzenia=msg.decode('utf-8'))
                    
if __name__ == '__main__':
    listen()