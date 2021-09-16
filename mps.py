from echo_server import BUFFER_SIZE
import socket, time, sys
from multiprocessing import Process

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

#echo connections back to client
def handle_request(addr,conn,proxy_end):
    print("Connected by ", addr)
    full_data = conn.recv(BUFFER_SIZE)
    print(f'Sending received data {full_data} to Google')
    proxy_end.sendall(full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    newdata = proxy_end.recv(BUFFER_SIZE)
    print(f'Sending received data {newdata} to Google') 
    conn.send(newdata)

def main():
    extern_host = 'www.google.com'
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(2)
        while True:
            conn, addr = proxy_start.accept()
            print(conn)
            print("connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("connecting to Google")
                remote_ip = get_remote_ip(extern_host)
            
                #connect proxy_end
                proxy_end.connect((remote_ip, port))

                p = Process(target=handle_request,args=(addr,conn, proxy_end))
                p.daemon = True
                p.start()
                print("Started process ", p)
            conn.close()

if __name__ == "__main__":
    main()

    
        
