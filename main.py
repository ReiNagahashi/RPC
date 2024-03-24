from server import Server
import socket

server = Server(socket.AF_INET, socket.SOCK_DGRAM, '127.0.0.1', 5000)

server.bind()

server.receiveRequest()