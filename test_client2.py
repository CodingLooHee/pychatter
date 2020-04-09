import socket
import msvcrt
import threading
from time import sleep


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


def enterHandler(keyStroke, conn, pendingText, needReprint):
    newlined = True
    while True:
        if (keypressed := keyStroke.getData()) != b'':
            if keypressed == b'\x08':   # Backspace
                pendingText.setData(pendingText.getData()[:-1])
                needReprint.setData(True)
            elif keypressed == b'\r':   # Enter
                conn.sendall(pendingText.getData().encode())
                pendingText.setData('')
                newlined = True
            elif keypressed == b'\n':   # Enter after '\r' but ignored
                pass
            else:
                if len(pendingText.getData()) <= 70:    # Limit message
                    pendingText.setData(pendingText.getData() + keypressed.decode())
            keyStroke.setData(b'')
        if pendingText.getData() == '' and newlined == True:    # Prevent oldline overwritten
            needReprint.setData(True)
            newlined = False




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
    isNeedReprint = SharedData(False)


    threading.Thread(target=keyChecker, args=(keyStroke,)).start()
    threading.Thread(target=connHandler, args=(client, sharedRecv,)).start()
    threading.Thread(target=enterHandler, args=(keyStroke, client, pendingText, isNeedReprint)).start()


    while True:
        if (received := sharedRecv.getData()) != '':
            print('\r' + received + ' '*80 + '\n', end='')
            sharedRecv.setData('')
        if isNeedReprint.getData(): # Prevent lag
            print('\r' + ' '*80, end='')
            isNeedReprint.setData(False)
        print('\rEnter: ' + pendingText.getData(), end='')




    client.close()
