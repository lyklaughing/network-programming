# network-programming
Here are three tasks related network programming, including POS, Multi-process, HTTP-based Movie Search Engine

Task 1: The server provides a service that assigns part-of-speech tags to a sentence received from the client, and sends the results back to the client.
The client reads a English sentence that is stored in a text file, and then send the sentence to the server. Upon receiving the results, it should print in to the standard output.

Task 2: In this assignment, I implement a TCP server that can handle multiple clients at the same time using the pre-fork worker model. The server provides an object recognition function, i.e. the client will send an image to the server, and the server will attempt to recognize what is inside the picture and send back the answer to the client.

Task 3: In this assignment, I implement a simple movie search engine with some social functions. The server will provide APIs (application programming interfaces) for clients to use functions such as searching for a movie or leaving a comment. Both the server and the client program should be implemented in Python.
In this assignment, I use a dataset from the Internet Movie Database (IMDb) to populate the content of our search engine. The dataset can be found on Kaggle (https://www.kaggle.com/PromptCloudHQ/imdb-data/data). A copy of the data in CSV format can also be found here: http://iems5703.albertauyeung.com/files/imdb_top1000.csv.
