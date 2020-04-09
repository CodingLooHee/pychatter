import socket








if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        print('Enter host and port you want to connect')
        HOST = input('Host: ')
        PORT = input('PORT: ')

        try:
            if HOST == '':
                    HOST = '0.0.0.0'
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
            print(err)
    


    client.close()
