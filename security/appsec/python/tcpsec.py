import socket

def target(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client.connect((host, port))
    
    client.send(b'GET / HTTP/1.1\r\nHost: ' + host.encode() + b'\r\n\r\n')
    
    response = client.recv(4096)
    
    print(response.decode())
    client.close()
    
if __name__ == '__main__':
    target(host='0.0.0.0', port=9999)