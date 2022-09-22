#!/usr/bin/env python3
from multiprocessing import Process
import socket
import tarfile
import time
import sys

#define address & buffer size
HOST = ""
PORT = 8002
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    google_host = 'www.google.com'
    port = 80
    payload = f'GET / HTTP/1.0\r\nHost: {google_host}\r\n\r\n'
    buffer_size = 4096
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_proxy:
        print(f'creating a proxy socket')
        s_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s_proxy.bind((HOST, PORT))
        #set to listening mode
        s_proxy.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s_proxy.accept() #
            print("Connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_connect_google:
                print(f"creating google socket")
                remote_ip = get_remote_ip(google_host)

                s_connect_google.connect((remote_ip , port)) #
                print (f'Socket Connected to {google_host} on ip {remote_ip}')
                p = Process(target=handle_echo, args=(s_connect_google, addr, conn))
                p.daemon = True
                p.start()
                print("Started P")
            conn.close()

def handle_echo(proxy_end, addr, conn):
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to google")
    proxy_end.sendall(send_full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    data = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    conn.send(data)


if __name__ == "__main__":
    main()
