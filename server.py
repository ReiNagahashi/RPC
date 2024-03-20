# import os
import socket
from faker import Faker

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = '127.0.0.1'
server_port = 5000

server_address = ((server_ip, server_port))
print(f"Server is running on {server_ip}:{server_port}")

sock.bind(server_address)


while True:
    print('\nwaiting to recieve massege')
    data, address = sock.recvfrom(4096)


    print('received {} bytes from {}'.format(len(data), address))
    print(data)


    if data:
        fake = Faker()
        response = fake.text().encode('utf-8')
        sent = sock.sendto(response, address)
        print('sent {} bytes back to {}'.format(sent, address))
