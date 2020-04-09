import socket
import os
import threading

def connectionHandler(addr, conn, all_conn):
    print('Connected by: ' + f'{addr[0]}: {addr[1]}')
    while True:
        try:
            data = conn.recv(1024).decode()
            print(f'<{addr[0]}| {addr[1]}> : ' + data)
            for each_conn in all_conn:
                try:
                    each_conn.sendall((f'<{addr[0]}| {addr[1]}> : ' + data).encode())
                except:
                    pass
        except ConnectionResetError:
            print(f'{addr[0]}: {addr[1]}' + ' disconnected')
            break
        except Exception as err:
            print(addr[0], err)
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
            connList.append(conn)
            threading.Thread(target=connectionHandler, args=(addr, conn, connList)).start()
        except Exception as err:
            server.close()
            raise(err)

