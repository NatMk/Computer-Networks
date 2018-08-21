Name: Natnael Kebede
ID: 1001149004

Used IDE: PyCharm
Python: Python 3.6.4

Server.py
	To run server you may use IDE or command line. 
	To run from command line you should enter the following line in formats:

	python server.py
		or
	python server.py 8080 (where 8080 is a port namber, it can be whatever you want)
	the exact command on command line would be python server.py -port 8080

	After this server starts running, it uses the following python modules:
 	- socket (to esteblish server, create socket and connection, handle requests from client (receive requests and send response to browsers or client program).
 	- threading (to redirect request handle in separate threads). 
 	- argparse (to parse and get command line arguments).

Client.py
	To run client you have to use command line. 
	
	Formats of command:

	python client.py localhost (host is positional parameter, so it is required. It can also be 127.0.0.1)
		or
	python client.py localhost 8080 (where 8080 is a port number, It can be whatever you want. It is an optimal argument) 
	the exact command on command line would be python client.py localhost -port 8080 

	If the argument is not specified, client.py will use default port number 8080. Port number must be the same as server's port number.
		or
	python client.py localhost 8080 file.txt
		or 
	python client.py localhost file.txt (where file.txt is name of requested file. It is an optimal argument)
	the exact command on command line would be python client.py localhost -port 8080 -file filename.txt or python client.py localhost -file filename.txt
	
	If the argument is not specified, client.py will use default file name index.html. If the requested file is not in the same folder as
	server.py, you should specify full path to the file (e.g. C:\folder\folder\file.txt)

	After this client starts running, it uses the following python modules:
 	- socket (to create connection via socket, send requests to server and receive response).
 	- argparse (to parse and get command line arguments).

