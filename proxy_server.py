import socket
import time
import sys

#define global address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    #Q6
     extern_host = 'www.google.com'
     port = 80

     #create socket
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:

        print('Starting proxy server')
        #allow reused addresses, bind, and set to listening mode.
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(1)
        
        #continuously listen for connections
        while True:
            #connect proxy_start
            conn, addr = proxy_start.accept()
            print("connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("connecting to Google")
                remote_ip = get_remote_ip(extern_host)
            
                #connect proxy_end
                proxy_end.connect((remote_ip, port))

                #send data
                send_full_data = conn.recv(BUFFER_SIZE)
                print(f'Sending received data {send_full_data} to google')

                proxy_end(send_full_data)

                #remember to shutdown!
                #shutdown() is different to close(), shutdown is a flexible way
                # to block communication in one or both directions. When the second parameter
                # is SHUT_RDWR, it will block both sending and receiving (like close).
                # However, close is the way to actually destroy a socket.
                #https://stackoverflow.com/questions/4160347/close-vs-shutdown-socket, answed by Mattew Flaschen.
                proxy_end.shutdown(socket.SHUT_WR)

                data = proxy_end.recv(BUFFER_SIZE)
                print(f'Sending received data {data} to client')
                #send data back
                conn.send(data)

            conn.close()

if __name__ == "__main__":
    main()