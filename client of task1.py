import socket
import sys
import codecs
import json

print(sys.argv)
host = str(sys.argv[1])
port = int(sys.argv[2])
path_to_file = sys.argv[3]

# create an INET TCP socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server (change localhost to an IP address if necessary)
try:
    soc.connect((host, port))
    print('connected to server.')
    with open(path_to_file,"r",encoding="utf-8") as f:
        msg_once = f.read()
    msg_second = msg_once + "<END>"

    i = len(msg_second)//2048+1
    for i in range(0,i):
        msg_third = msg_second[i*2048:(i+1)*2048]
        msg = msg_third.encode("utf-8")
        soc.send(msg)

    data_total = []
    while True:
        re_data = soc.recv(2048)
        data_pro = re_data.decode("utf-8")
        data_total.append(data_pro)
        if not data_pro:break

    data_third =''.join(data_total)
    data_sec = json.loads(data_third)
    info_start = []
    chara_start = []
    for i in range(len(data_sec)):
        info_start.append(data_sec[i][0])
        chara_start.append(data_sec[i][1])
    info = ' ; '.join(info_start)
    chara = ' ; '.join(chara_start)
    print(info)
    print(chara)
    soc.close()

except socket.error:
    print('Cannot connect to server at <%s>:<%d>' % (host,port))
    soc.close()
