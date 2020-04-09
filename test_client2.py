import socket
import msvcrt
import threading


class SharedData:
    def __init__(self, data=None):
        self.__value = [data]
    def setData(self, data):
        self.__value[0] = data
    def getData(self):
        return self.__value[0]


def keyChecker(dataPasser):
    while True:
        if msvcrt.kbhit():
            dataPasser.setData(msvcrt.getch())

def connHandler(conn, sharedRecv):
    while True:
        sharedRecv.setData(conn.recv(1024).decode())


def enterHandler(keyStroke, conn, pendingText):
    while True:
        if (keypressed := keyStroke.getData()) != b'':
            if keypressed == b'\x08':   # Backspace
                pendingText.setData(pendingText.getData()[:-1])
            elif keypressed == b'\r':
                conn.sendall(pendingText.getData().encode())
                pendingText.setData('')
            elif keypressed == b'\n':
                pass
            else:
                pendingText.setData(pendingText.getData() + keypressed.decode())
            keyStroke.setData(b'')



if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        print('\nEnter host and port you want to connect')
        HOST = input('Host: ')
        PORT = input('PORT: ')

        print()

        try:
            if HOST == '':
                    HOST = '127.0.0.1'
            if PORT == '':
                PORT = 12345
            
            PORT = int(PORT)

            client.connect((HOST, PORT))
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
    

    keyStroke = SharedData(b'')
    sharedRecv = SharedData('')
    pendingText = SharedData('')

    threading.Thread(target=keyChecker, args=(keyStroke,)).start()
    threading.Thread(target=connHandler, args=(client, sharedRecv,)).start()
    threading.Thread(target=enterHandler, args=(keyStroke, client, pendingText)).start()


    while True:
        if (received := sharedRecv.getData()) != '':
            print('\r' + received + ' '*80)
            sharedRecv.setData('')
        print('\rEnter: ' + pendingText.getData(), end='')




    client.close()
