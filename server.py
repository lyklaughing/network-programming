import pandas as pd
import nltk
from flask import Flask, current_app, request
import json
import nltk
import time
from operator import itemgetter
import sys

#port = int(sys.argv[1])
df = pd.read_csv("D:/pycharm/assignment3/imdb_top1000.csv")
#movies = df.to_dict(orient='records')
movies = df.to_dict(orient='Rank')
list_title = []
list_actor = []
all_title = {}
all_actor = {}
for dict in range(len(movies)):
    list_title = nltk.word_tokenize(movies[dict].get('Title'))
    #id = movies[dict].get('Rank')
    for word in list_title:
        all_title[word.lower()] = []

for dict in range(len(movies)):
    list_actor = nltk.word_tokenize(movies[dict].get('Actors'))
    for word in list_actor:
        all_actor[word.lower()] = []

for dict in movies:
    dict['ID'] = dict['Rank'] - 1
    for word in nltk.word_tokenize(dict['Title']):
        all_title[word.lower()].append(dict['ID'])

for dict in movies:
    dict['comment'] = []
    dict['ID'] = dict['Rank'] - 1
    for word in nltk.word_tokenize(dict['Actors']):
        all_actor[word.lower()].append(dict['ID'])


print(all_title)
print(all_actor)
print(movies)

app = Flask(__name__)
app.movies = movies
app.title_index = all_title
app.actor_index = all_actor

@app.route('/movie/<int:id>', methods = ['GET'])
def get_movie(id):
	movies = current_app.movies
	data = json.dumps(movies[(id-1)])
	return(data)

@app.route('/comment', methods=['POST'])
def comment():
    name = request.values.get('username', type=str, default=None)
    id = request.values.get('id', type=int, default=None)
    id = int(id)
    comment_content = request.values.get('comment', type=str, default=None)
    movies = current_app.movies
    title_index = current_app.title_index
    actor_index = current_app.actor_index
    dict={'comment':comment_content,'timestamp':time.strftime("%y:%m:%d %H:%M:%S",time.localtime()),'username':name}
    if ('comment' in movies[(id)]):
        movies[(id)]['comment'].append(dict)
    else:
        movies[(id)]['comment'] = [dict]
    msg = json.dumps(movies[(id)])
    return (msg)

@app.route('/search', methods = ['GET'])
def search_movie():
	movies = current_app.movies
	title_index = current_app.title_index
	actor_index = current_app.actor_index
	data = []
	query = request.values.get('query', type = str, default = None)
	attribute = request.values.get('attribute', type = str, default = 'title')
	sortby = request.values.get('sortby', type = str, default = 'rating')
	order = request.values.get('order', type = str, default = 'ascending')
	if (attribute == 'title'):
		for i in title_index[query]:
			data.append(movies[(i-1)])
	else:
		for i in actor_index[query]:
			data.append(movies[(i-1)])
	if (sortby == 'year'):
		if (order == 'descending'):
			msg = json.dumps(sorted(data, key = itemgetter('Year'),reverse = True)[0:10])
			return(msg)
		elif (order == 'ascending'):
			msg = json.dumps(sorted(data, key = itemgetter('Year'))[0:10])
			return(msg)
		else:
			msg = json.dumps('invalid order!')
			return(msg)
	elif (sortby == 'rating'):
		if (order == 'descending'):
			msg = json.dumps(sorted(data, key = itemgetter('Rating'),reverse = True)[0:10])
			return(msg)
		elif (order == 'ascending'):
			msg = json.dumps(sorted(data, key = itemgetter('Rating'))[0:10])
			return(msg)
		else:
			msg = json.dumps('invalid order!')
			return(msg)
	elif (sortby == 'rank'):
		if (order == 'descending'):
			msg = json.dumps(sorted(data, key = itemgetter('Rank'),reverse = True)[0:10])
			return(msg)
		elif (order == 'ascending'):
			msg = json.dumps(sorted(data, key = itemgetter('Rank'))[0:10])
			return(msg)
		else:
			msg = json.dumps('invalid order!')
			return(msg)
	elif (sortby == 'runtime'):
		if (order == 'descending'):
			msg = json.dumps(sorted(data, key = itemgetter('Runtime'),reverse = True)[0:10])
			return(msg)
		elif (order == 'ascending'):
			msg = json.dumps(sorted(data, key = itemgetter('Runtime'))[0:10])
			return(msg)
		else:
			msg = json.dumps('invalid order!')
			return(msg)
	elif (sortby == 'votes'):
		if (order == 'descending'):
			msg = json.dumps(sorted(data, key = itemgetter('Votes'),reverse = True)[0:10])
			return(msg)
		elif (order == 'ascending'):
			msg = json.dumps(sorted(data, key = itemgetter('Votes'))[0:10])
			return(msg)
		else:
			msg = json.dumps('invalid order!')
			return(msg)
	elif (sortby == 'revenue'):
		if (order == 'descending'):
			msg = json.dumps(sorted(data, key = itemgetter('Revenue'),reverse = True)[0:10])
			return(msg)
		elif (order == 'ascending'):
			msg = json.dumps(sorted(data, key = itemgetter('Revenue'))[0:10])
			return(msg)
		else:
			msg = json.dumps('invalid order!')
			return(msg)
	elif (sortby == 'metascore'):
		if (order == 'descending'):
			msg = json.dumps(sorted(data, key = itemgetter('Metascore'),reverse = True)[0:10])
			return(msg)
		elif (order == 'ascending'):
			msg = json.dumps(sorted(data, key = itemgetter('Metascore'))[0:10])
			return(msg)
		else:
			msg = json.dumps('invalid order!')
			return(msg)
	else:
		msg = json.dumps('invalid sortby!')
		return(msg)

@app.route('/')
def hello_world():
	return 'Hello World!'

if __name__ == "__main__":
    app.run()



