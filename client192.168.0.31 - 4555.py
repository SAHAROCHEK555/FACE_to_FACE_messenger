import socket
import threading
import random
import sys
from datetime import datetime
import sqlite3

conn = sqlite3.connect('client&serverDB.db', check_same_thread=False)
cursor = conn.cursor()

host = '192.168.0.31'
port = 4555
    
def db_table_val(user_password: int, user_name: str, color: int):
    cursor.execute('INSERT INTO project (user_password, user_name, color) VALUES (?, ?, ?)', (user_password, user_name, color))
    conn.commit()


max_size = 65535
mesgs = []
def listen(soc: socket.socket):
    while True:
        msg = soc.recv(max_size)
        print('\r\r' + f'\033[{random.randint(31, 37)}m'+ msg.decode('utf-8') + '\n' + f'\033[{col_con1}m{name}: ', end='')
        mesgs.append(msg.decode('utf-8'))
        
def connect1(host: str = host, port: int = port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect((host, port))
    threading.Thread(target=listen, args=(soc,), daemon=True).start()
    name2 = name
    soc.send(f'SIGNUP_TAG:{name2}'.encode('utf-8'))
    
    while True:
        time2 = datetime.now()
        msg = input(f'\033[{col_con1}m{name}: ')
        soc.send(f'[{time2.hour}:{time2.minute}:{time2.second}] {name}: \033[{col_con1}m{msg}'.encode('utf-8'))
        mesgs.append(f'[{time2.hour}:{time2.minute}:{time2.second}] {name}: \033[{random.randint(31, 37)}m {msg}')
        if msg == '@messages':
            print('')
            print('                                          MESSAGES LIST')
            for x in mesgs:
               print(x)
            print('')
        elif msg == '@change_col':
                print('')
                otv1 = input("\033[37m{}".format('Input password: ')) 
                cursor.execute(f"SELECT user_name FROM project WHERE user_password = '{otv1}'")
                user_tipo1 = cursor.fetchone() 
                if not user_tipo1:
                    print('')
                    print("your account not found")
                    print('')
               
                else:    
                    print('')
                    print('red - 31 / green - 32 / yellow - 33 / blue - 34 / purple - 35 / turquoise - 36 / white - 37 ')
                    channge_color1 = int(input("\033[37m{}".format('Select your color(31/32/33/34/35/36/37): ')))
                    print("Your color: ", channge_color1)
                    print('')
                    print('Restart the client for the changes to take effect')
                    cursor.execute(f"UPDATE project SET color == '{channge_color1}' WHERE user_password == '{otv1}'")
                    conn.commit()
                    print('')
        elif msg == '@close':
            soc.shutdown(1)

                   

            
            
            
            
            
            
            
            
            
            
def listen2(soc: socket.socket):
    while True:
        msg = soc.recv(max_size)
        print('\r\r' + f'\033[{random.randint(31, 37)}m'+ msg.decode('utf-8')  + '\n' + f'\033[{col_con2}m{name}: ',end='')
        mesgs.append(msg.decode('utf-8'))
            
def connect2(host: str = host, port: int = port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect((host, port))
    threading.Thread(target=listen2, args=(soc,), daemon=True).start()

    name2 = name
    soc.send(f'SIGNUP_TAG:{name2}'.encode('utf-8'))
    
    while True:
        time2 = datetime.now()
        msg = input(f'\033[{col_con2}m{name}: ')
        soc.send(f'[{time2.hour}:{time2.minute}:{time2.second}] {name}:\033[{col_con2}m {msg}'.encode('utf-8'))
        mesgs.append(f'[{time2.hour}:{time2.minute}:{time2.second}] {name}: \033[{random.randint(31, 37)}m {msg}')
        if msg == '@messages':
            print('')
            print('                                          MESSAGES LIST')
            for x in mesgs:
               print(x)
            print('')
            
        elif msg == '@change_col':
                print('')
                otv1 = input("\033[37m{}".format('Input password: ')) 
                cursor.execute(f"SELECT user_name FROM project WHERE user_password = '{otv1}'")
                user_tipo = cursor.fetchone() 
                if not user_tipo:
                    print('')
                    print("your account not found")
                    print('')
               
                else:    
                    print('')
                    print('red - 31 / green - 32 / yellow - 33 / blue - 34 / purple - 35 / turquoise - 36 / white - 37 ')
                    change_color2 = int(input("\033[37m{}".format('Select your color(31/32/33/34/35/36/37): ')))
                    print("Your color: ", change_color2)
                    print('')
                    print('Restart the client for the changes to take effect')
                    cursor.execute(f"UPDATE project SET color == '{change_color2}' WHERE user_password == '{otv1}'")
                    conn.commit()
                    print('')
                
        elif msg == '@close':
            soc.shutdown(1)
            
            
          
            
            
        
def main_menu():
    print('\033[37m{}'.format('           MAIN MENU'))
    print('\033[37m{}'.format(f'server1: {host} : {port} '))
    print("\033[37m{}".format('Sign up - 1'))
    print("\033[37m{}".format("Sign in - 2"))
    otvet2 = int(input("\033[37m{}".format('1/2: ')))
    if otvet2 == 1:
        print('')
        print('Create account - 3')
        print('Back - 4')
        dt = int(input('3/4: '))
        if dt == 3:
            print('')
            password = input("\033[37m{}".format('Create your password: '))   
            print(f'Your password: {password}')
            print('')
            global name
            name = input("\033[37m{}".format('Create your name: '))
            print(f'Your name: {name}')
            print('')
            print('red - 31 / green - 32 / yellow - 33 / blue - 34 / purple - 35 / turquoise - 36 / white - 37 ')
            global col_con2
            col_con2 = int(input("\033[37m{}".format('Select your color(31/32/33/34/35/36/37): ')))
            print(f'Your color: {col_con2}')            
            db_table_val(user_password= password, user_name= name, color= col_con2)
            print('')
            print("\033[37m{}".format('                                                            Welcome to the chat!'))
            print("\033[37m{}".format('#Command 1: @change_col - change color'))
            print("\033[37m{}".format('#Command 2: @messages - call messages list'))
            print("\033[37m{}".format('#Command 3: @close - close client'))
            print('')
            print('')
            print('                                                                    CHAT')
            print('')
            
            
        elif dt == 4:
            print('')
            main_menu()
            
        else:
            main_menu()
            
            
    elif otvet2 == 2:
            otvet3 = input("\033[37m{}".format('Input password: ')) 
            cursor.execute(f"SELECT user_name FROM project WHERE user_password = '{otvet3}'")
            user_ = cursor.fetchone() 
            if not user_:
                print('Your account not found, please go to main menu')
                print('')
                main_menu()
                    
            else:
                name = user_[0]
                cursor.execute(f"SELECT color FROM project WHERE user_password = '{otvet3}'")
                cl = cursor.fetchone()
                global col_con1
                col_con1 = cl[0]                 
                print(f"Hi {name}!\033[{col_con1}m")
                print('')
                print("\033[37m{}".format('                                                            Welcome to the chat!'))
                print("\033[37m{}".format('#Command 1: @change_col - change color'))
                print("\033[37m{}".format('#Command 2: @messages - call messages list'))
                print("\033[37m{}".format('#Command 3: @close - close client'))
                print('')
                print('')
                print('                                                                    CHAT')
                print('')
                cursor.execute('SELECT soobzenia FROM all_mes')
                chat_story = cursor.fetchmany(100)
                if not chat_story:
                    print('')
                else:
                    for i in chat_story:
                        print(i[0])
                connect1()
    
    else:
        main_menu()
        
if __name__ == '__main__':
    main_menu()            
            
            

            
    