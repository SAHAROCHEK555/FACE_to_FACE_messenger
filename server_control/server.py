import socket
import sqlite3
import time

with sqlite3.connect('server.db3') as conn:
    cursor = conn.cursor()

    def db_table_func_insert_login_data(user_pasw: str, user_nm: str):
        cursor.execute('INSERT INTO proj (user_pasw, user_nm) VALUES (?, ?)', (user_pasw, user_nm))
        conn.commit()   
        
    def db_table_func_insert_msg(soobzenia: str):
        cursor.execute('INSERT INTO all_mes (soobzenia) VALUES (?)', (soobzenia,))
        conn.commit()
            
    def db_table_func_select_user_name(user_pasw: str, memb, addr, soc):
        cursor.execute(f'SELECT user_nm FROM proj WHERE user_pasw = {user_pasw}')
        conn.commit()
        user_ = cursor.fetchone()
        print(user_)
        name = user_[0]    
        if memb[-1] == addr:
            soc.sendto(f'SIGNIN_TAG:{name}'.encode("utf-8"), memb[-1])
        
class Listen_server_class: 
    def listen(self, host = 'localhost', port = 8000):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.bind((host, port))
        print(f'Listening at {host} : {port}')
        
        messages = []
        memb = []
        
        while True:
                try:
                    msg, addr = soc.recvfrom(1024)
                except ConnectionResetError:
                    print(f"Connection reset by {addr}")
                    msg, addr = soc.recvfrom(1024)
                    continue
                
                if addr not in memb:
                    memb.append(addr)
                
                if not msg:
                    continue  
                
                        
                if msg.decode('utf-8').startswith('OPEN_TAG:'):
                    name1 = addr[1]
                    print(f'Client {name1} joined chat!')
                    continue
                
                if msg.decode('utf-8').startswith('SIGNUP_TAG:'):
                    my_list = msg.decode("utf-8").split()
                    user_pass = my_list[1]
                    user_nm = my_list[2] 
                    db_table_func_insert_login_data(user_pasw= user_pass, user_nm=user_nm)
                    if memb[-1] == addr:
                        soc.sendto(f'SIGNIN_TAG:{user_nm}'.encode("utf-8"), memb[-1])   
                        continue
                
                if msg.decode("utf-8").startswith("SIGNIN_TAG:"):
                    user_passw = msg.decode('utf-8')[msg.decode('utf-8').index(':')+1:]
                    print(user_passw)
                    db_table_func_select_user_name(user_pasw= user_passw, memb=memb, addr=addr, soc=soc)
                    continue
                
                if msg.decode('utf-8').startswith('STORY_TAG'):
                    cursor.execute('SELECT soobzenia FROM all_mes LIMIT 10 OFFSET (SELECT COUNT(*) FROM all_mes)-10')
                    chat_story = cursor.fetchall()
                    for i in chat_story:
                        g = i[0] 
                        soc.sendto(g.encode('utf-8'), addr)
                        time.sleep(0.5)
                                  
                    continue
                
                for member in memb:
                    if member == addr:
                        continue
                    
                    soc.sendto(msg, member) 
                    
                    messages.append(msg.decode('utf-8'))
                    db_table_func_insert_msg(soobzenia=msg.decode('utf-8'))


if __name__ == '__main__':
    listen_server_class_copy = Listen_server_class()
    listen_server_class_copy.listen()