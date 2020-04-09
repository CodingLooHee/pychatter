import socket
import os
import threading

def connectionHandler(addr, conn):
    print('Connected by:', addr)
    while True:
        try:
            data = conn.recv(1024)
            print(addr, ':', data.decode())
        except ConnectionResetError:
            print(addr, 'disconnected')
            break
        except Exception as err:
            print(addr, err)
            break

if __name__ == '__main__':
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
          f'Port:       {PORT}\n' +\
          '---------------------------\n')







    server.listen()

    connList = []

    while True:
        try:
            conn, addr = server.accept()
            threading.Thread(target=connectionHandler, args=(addr[0], conn,)).start()
        except Exception as err:
            server.close()
            raise(err)

