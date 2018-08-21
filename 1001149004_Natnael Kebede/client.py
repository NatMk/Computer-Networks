# Name:  Natnael Kebede
# ID:    1001149004
# Simple Web Client

# import socket and time modules
from socket import *
import time

# default values for host, port and file
HOST = 'localhost'
PORT = 8080
FILENAME = 'index.html'

def connect_to_server(host, port, file):
    """
    Connect to server, make request and get data back.

    :param host: host name (str)
    :param port: port number (int)
    :param file: requested file name (str)
    :return: NoneType
    """
    # create socket
    client = socket(AF_INET, SOCK_STREAM)
    # connect to given host-port
    client.connect((host, port))
    # start timing from start request to server
    start_time = time.time()
    print('connected to {}'.format(host))

    # send GET request to the server with headers specifying content type
    # data which is sent with sockets should be in bytes so it is needed to encode
    client.sendall("""GET /{}\r\nContent-Type: text/html\r\n\r\n""".
                   format(file).encode())

    # declare variable data to store received data from server
    data = ''
    # start receiving data from server
    while True:
        # receive data from server (with headers) and decode bytes
        outputdata = client.recv(512).decode()

        # if not data (server sent all) stop while loop
        if not outputdata:
            break
        # add part of received data
        data += outputdata

    # collect connection information
    connection_info = '{:>20}:\t{}\n{:>20}:' \
                      '\t{}\n{:>20}:\t{}\n' \
                      '{:>20}:\t{}'.format('Socket family',
                                           client.family,
                                           'Socket type', client.type,
                                           'Protocol', client.proto,
                                           'Timeout', client.gettimeout(),
                                           'Pear', client.getpeername())
    # count and print time of receiving response from server in seconds
    print('Time for request: {}'.format((time.time() - start_time) * 1000))
    # print connection info
    print('-' * 30)
    print(connection_info)
    print('Received response from {}:'.format(host))

    # separate headers from data
    headers, data = data.split('\r\n', 1)
    # get status code of response
    status_code = ' '.join(headers.split()[1:])

    # print status code, headers and file content
    # (or server response if there is no requested file on server
    print('{:>20}:\t{}\n{:>20}:\t{}\n{}:'.format('Status code', status_code,
                                                 'Headers', headers, 'Content'))
    print(data.strip())
    client.close()


if __name__ == '__main__':
    # import argparse module to get argument from command line
    import argparse
    # create parser
    parser = argparse.ArgumentParser()
    # add arguments
    # host is positional argument so it is
    # required for running client
    parser.add_argument('host', help ='This should be host name')
    # port and file are optional arguments,
    # so if they are not specified it's OK
    parser.add_argument('-port', help ='This should be port number')
    parser.add_argument('-file', help ='This should be filename')

    # this line will collect arguments from command line
    args = parser.parse_args()
    # store positional first argument host to variable HOST
    HOST = args.host

    # if optional argument -port was declared store its value to PORT
    # if -port is not specified we will use the default PORT
    if args.port:
        # if user made mistake and entered something inappropriate for port number (not digits)
        # we print and error and use the default value of PORT
        try:
            PORT = int(args.port)
        except IndexError:
            print('Invalid port number!')

    # if user specified requested file, it will be stored in the variable FILENAME
    if args.file:
        FILENAME = args.file

    # connect to server
    connect_to_server(HOST, PORT, FILENAME)
