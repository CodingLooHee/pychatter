import socket
import os
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


while True:
    print('\nPlease enter Host and Port you would like to bind (Press Enter to use default value)')

    HOST = input('Host: ')
    PORT = input('Port: ')

    
    
    print()
    
    try:
        if HOST == '':
            HOST = '0.0.0.0'
        if PORT == '':
            PORT = 12345

        PORT = int(PORT)
        server.bind((HOST, PORT))
        break
    except socket.gaierror:
        print('Invalid Host address')
        continue
    except OSError:
        print('Invalid Host address')
        continue
    except ValueError:
        print('Port must be a number')
        continue
    except OverflowError:
        print('Port must be 0-65535')
        continue
    except Exception as err:
        raise(err)



os.system('cls')
print('------- Server Info -------')
print(f'Address:    {HOST}\n' +\
      f'Port:       {PORT}')


def connectionHandler(conn):
    while True:
        try:
            data = conn.recv(1024)
            print(data)
        except ConnectionResetError:
            print('Connection from', conn, 'reseted')
            break




server.listen()

connList = []

while True:
    conn, addr = server.accept()
    print('Connected by:', addr)
    threading.Thread(target=connectionHandler, args=(conn,)).start()




server.close()
