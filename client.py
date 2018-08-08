#测试代码时，可以通过thread_pool()子函数修改需要下载的图片个数
import socket
import sys
import logging
from concurrent.futures import ThreadPoolExecutor

print(sys.argv)
host = str(sys.argv[1])
port = int(sys.argv[2])
url = str(sys.argv[3])

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
                    level=logging.INFO)
# 创建logging
def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        soc.connect(('localhost', port))           #之后加host与port
        logging.info('Connected to server at (%s, %d)' % (host, port))      #之后加host与port
        msg_once = url + '[END]'
        msg = msg_once.encode('utf-8')
        soc.send(msg)
        logging.info('URL sent to the server')
        while True:
            re_data = soc.recv(2048)
            if not re_data:
                break
            else:
                data_pro = re_data.decode("utf-8")
        data_pro = data_pro.replace('"','')
        logging.info('Server response: %s' % data_pro)
        soc.close()

    except socket.error:
        soc.close()

def thread_pool():
    with ThreadPoolExecutor(max_workers=20) as executor:
        [executor.submit(main) for _ in range(6)]          #测试时修改需要读取的图片数

if __name__ == '__main__':
    thread_pool()


