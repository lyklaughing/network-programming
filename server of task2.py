import tensorflow as tf
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing import image
import socket
import sys
import logging
import multiprocessing
import os
import random
import requests
import json
from urllib import request
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
print(sys.argv)
port = int(sys.argv[1])
child_process = int(sys.argv[2])
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] : %(message)s',
                    level=logging.INFO)
# 创建logging
l = Lock()

def f(queue):
    graph = tf.get_default_graph()
    model = SqueezeNet()
    executor = ThreadPoolExecutor(max_workers=4)  # 创建线程个数
    while True:
        if not queue.empty():
            l.acquire()
            s = queue.get()
            l.release()
            client_socket, client_address = (s[0], s[1])
            executor.submit(thread_pool, client_socket, client_address, graph, model)

def thread_pool(client_socket, client_address, graph, model):
    data = client_socket.recv(2048)
    logging.info('Received Client (%s , %d).' % (client_address[0], client_address[1]))
    data_second = data.decode('utf-8')
    if '[END]' in data_second:
        data_second = data_second[:-5]
        logging.info('Client submitted URL %s' % data_second)
        # 入线程池
        # 存图片在本地
    url = data_second
    path = 'wahaha'
    if not os.path.exists(path):
        os.mkdir(path)
    r = requests.get(url).content
    name_generate = random.random()
    name_generate = 100000 * name_generate
    name_third = int(name_generate)
    name = str(name_third)
    file_name = path + '/' + name + '.jpg'
    with open(file_name, 'wb') as code:
        code.write(r)
    logging.info('Image saved to ' + file_name)
    # 进行图像处理操作
    with graph.as_default():
        img = image.load_img(file_name, target_size=(227, 227))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        image_process = decode_predictions(preds)
    image_tumple = image_process[0][0]
    image_sectumple = image_tumple[1:]
    image_str = str(image_sectumple)
    logging.info('SqueezeNet result: %s' % image_str)
    image_proce = json.dumps(image_str).encode('utf-8')
    client_socket.sendall(image_proce)
    client_socket.shutdown(2)
    logging.info('Client connection closed')
    client_socket.close()

# 创建主进程
if __name__ == '__main__':
    multiprocessing.freeze_support()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    #之后加port
    server_socket.listen(10)
    logging.info('Start listening for connections on port %d' % port)
    socket_queue = multiprocessing.Queue()
    # 创建一个queue
    processes = []
    # 之后加child_process
    for i in range(child_process):
        p = multiprocessing.Process(target=f, args=(socket_queue,))
        p.start()
        processes.append(p)
        logging.info('Created process Process-%d' % i)

    while True:
        s = (client_socket, address) = server_socket.accept()
        socket_queue.put(s)  # 将queue放进子进程
        logging.info('Client (%s , %d) connected.' % (address[0], address[1]))
        # 链接成功
