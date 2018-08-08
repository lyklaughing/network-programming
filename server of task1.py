import socket
import sys
import nltk
import json

print(sys.argv)
port = int(sys.argv[1])
# create an INET socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the host and a port
server_socket.bind(("localhost", port))

# Listen for incoming connections from clients
print('Listening for incoming connections on port %d' % port)
server_socket.listen(10)

# A indefinite loop
while True:
# accept connections from outside
    data_total = []
    try:
        (client_socket, address) = server_socket.accept()
        print ("client %s connected." % address[0])
# Read data from client and send it back
        while True:
            data = client_socket.recv(2048)
            data_four = data.decode("utf-8")
            data_total.append(data_four)
            if "<END>" in data_four:break
        
        tokens_once =''.join(data_total)
        tokens_second = tokens_once[:-5]
        print (tokens_second)
        tokens = nltk.word_tokenize(tokens_second)
        tagged = nltk.pos_tag(tokens)
        re_data = json.dumps(tagged).encode('utf-8')
        client_socket.sendall(re_data)

        # Close the socket
        client_socket.close()
        print ('Client disconnected.')
    except socket.error as error:
        print ('Client disconnected.')
        client_socket.close()
