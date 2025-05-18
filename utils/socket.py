import socket, struct, os

def send(file,host='192.168.1.60',port=7771):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,port))
    
    fileSize = os.path.getsize(file)
    fnBytes = file.encode()
    fnLen = len(fnBytes)
    
    client.sendall(struct.pack('!I',fnLen))
    client.sendall(fnBytes)
    client.sendall(struct.pack('!Q',fileSize))
    
    with open (file, 'rb') as f:
        client.sendfile(f)
    
    print('File sent')