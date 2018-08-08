import sys
import json
import socket
import requests

host = str(sys.argv[1])
port = int(sys.argv[2])
arg3 = str(sys.argv[3])
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    soc.connect((host, port))
    print('connected to server.')
    if arg3 == 'search':
        query = sys.argv[4]
        attribute = sys.argv[5]
        sortby = sys.argv[6]
        order = sys.argv[7]
        r = requests.get("http://%s:%s/search?query=%s&attribute=%s&sortby=%s&order=%s" % (host, port, query, attribute, sortby, order))
        formatted_json = json.dumps(r.json(), indent=4, sort_keys=True)
        print("Request: /search?query={}&attribute={}&sortby={}&order={}".format(query, attribute, sortby, order))
        print("\r")
        print("Response: ")
        print(formatted_json)

    elif arg3 == 'movie':
        movie_id = sys.argv[4]
        r = requests.get("http://%s:%s/movie/%d" % (host, port, movie_id))
        formatted_json = json.dumps(r.json(), indent=4, sort_keys=True)
        print("Request: /movie/{}".format(movie_id))
        print("\r")
        print("Response:")
        print(formatted_json)

    elif arg3 == 'comment':
        username = sys.argv[4]
        movie_id = sys.argv[5]
        comment = input('Please input your comment: ')
        req = 'http://{}:{}/comment'.format(host, port)
        user = {'user_comment': comment, 'user_name':username, 'movie_id':movie_id}
        r = requests.post(req, data=user)
        formatted_json = json.dumps(r.json(), indent=4, sort_keys=True)
        print("Request: /comment")
        print("user_name = ", username)
        print("movie_id = ", movie_id)
        print("comment = ", comment)
        print("\r")
        print("Response: ")
        print(formatted_json)

except socket.error:
    print('Cannot connect to server at <%s>:<%d>' % (host,port))
    soc.close()

