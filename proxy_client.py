#!/usr/bin/env python3
import socket, sys
#define address info, payload, and buffer size
host = 'localhost'
port = 8002 #c
payload = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
buffer_size = 1024
#edited

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    #connect(('127.0.0.1',8002))
    try:
        

        #make the socket, get the ip, and connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        remote_ip = get_remote_ip(host)

        s.connect((remote_ip , port)) #
        print (f'Socket Connected to {host} on ip {remote_ip}')
        
        #send the data and shutdown
        send_data(s, payload)
        s.shutdown(socket.SHUT_WR)

        #continue accepting data until no more left
        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                 break
            full_data += data
        print(full_data)
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        s.close()
if __name__ == "__main__":
    main()

