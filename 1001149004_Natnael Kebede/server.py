# Name:  Natnael Kebede
# ID:    1001149004
# Multithreaded Web Server

# import socket and threading modules
from socket import *
import threading

# specify default values for port and host
HOST = 'localhost'
PORT = 8080

# to lock for other threads access to print() (sys.stdout)
lock = threading.Lock()

class MyServer:
    def __init__(self, host, port):
        """
        Constructor.

        :param host: name of host (str)
        :param port: number of port (int)
        """
        self.host = host
        self.port = port
        # run server
        self.start_server()

    def start_server(self):
        """
        Run server.

        :return: NoneType
        """
        # create socket
        self.server = socket(AF_INET, SOCK_STREAM)
        # self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # bind server
        self.server.bind((self.host, self.port))
        self.listen_connection()

    def listen_connection(self):
        """
        Listen for connection and handle requests.

        :return: NoneType
        """
        print('Ready for connection...')
        # listen for connection from client
        self.server.listen(5)
        # in infinit loop accept connections
        # and redirect them to separate threads
        while True:
            # connection - client socket object,
            # address (client's host and port)
            connection, address = self.server.accept()
            # create and start thread to handle request
            threading.Thread(target=self.run,
                             args=(connection, address,)).start()

    def run(self, connection, address):
        """
        Handle each client's connection.

        :param connection: client socket object
        :param address: client address
        :return: NoneType
        """
        # print address of client
        with lock:
            print('Connected to {}'.format(address))
            # print connection information
            connection_info = '{:>20}:\t{}\n{:>20}:\t{}\n{:>20}:' \
                              '\t{}\n{:>20}:\t{}\n'.format('Socket family',
                                                         connection.family,
                                                         'Socket type', connection.type,
                                                         'Protocol', connection.proto,
                                                         'Timeout', connection.gettimeout(),
                                                         'Pear', connection.getpeername())

            print('-' * 30)
            print(connection_info)
        # receive message from client and decode it from bytes
        message = connection.recv(512).decode()
        # if client does't send any message close connection

        if not message:
            connection.close()
        # print received message
        with lock:
            print(message)

        try:
            # try to get file name from request
            filename = message.split()[1][1:]
            # if it not specified use default file - index.html
            if not filename:
                filename = 'index.html'
            try:
                # try to open requested file and read data
                f = open(filename, 'rb')
                outputdata = f.read()
                f.close()
                # prepare response to client with headers and status code
                # encode it in bytes
                response = """HTTP/1.1 200 OK\r\n\r\n""".encode()
                # send to client headers and data from file
                connection.sendall(response)
                connection.sendall(outputdata)
                print('File sent successfully')
            except (IOError, FileExistsError, FileNotFoundError):
                # if file not exists on server send client
                # headers with status code 404 and message about error
                connection.send("""HTTP/1.1 404 File NotFound\r\n\r\n
                File NotFound""".encode())
                with lock:
                    print('File not found')
            except OSError:
                pass
        except IndexError:
            pass
        with lock:
            print('Server closed connection with {}'.format(address))
        # close connection with client
        connection.close()


if __name__ == '__main__':
    # import argparse module to get argument from command line
    import argparse
    # create parser
    parser = argparse.ArgumentParser()
    # port is optional argument, so if it isn't specified it's OK
    parser.add_argument('-port', help='This should be port number')
    # this line will "collect" arguments from command line
    args = parser.parse_args()
    # if optional argument -port was declared store it's value to PORT
    # if -port not specified will be used default PORT
    if args.port:
        try:
            # if user made mistake and entered something
            # inappropriate for port number (not digits)
            # will be printed error and use default value of PORT
            PORT = int(args.port)
        except IndexError:
            print('Invalid port number!')
    # run server
    MyServer(HOST, PORT)
