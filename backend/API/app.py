# app.py
import urllib.request
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify

import pandas as pd
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model, load_model
import keras
import tensorflow
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

app = Flask(__name__)

model = None


def getModel():
    global model
    model = load_model('sage.h5')


def getPercentage(cleanText):
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    TESTDATA = StringIO(cleanText)
    data = pd.read_table(TESTDATA, names=('X'))
    data['X'] = data['X'].apply((lambda x: re.sub('[^a-zA-z0-9\s]', '', x)))
    for idx, row in data.iterrows():
        row[0] = row[0].replace('rt', ' ')
    data = data.append(data)
    tokenizer.fit_on_texts(data['X'].values)
    test = tokenizer.texts_to_sequences(data['X'].values)
    test = pad_sequences(test, 5014)
    print(model.predict(test, batch_size=2))


def getLinks():
    links = {"link1": "https://www.pornhub.com/",
             "link2": "https://www.facebook.com/", "link3": "https://www.twitter.com/"}
    return links


def getText(url):
    articleText = ""

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"

    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read()

    # parse html
    soup = BeautifulSoup(html, 'html.parser')

    # title of article
    articleText += re.sub('<[^<]+?>', '', str(soup.title))

    # extract text from paragraphs
    for paragraph in soup.find_all('p', recursive=True):
        # strip html, byte symbols, whitespace
        articleText += str(re.sub('(<[^<]+?>)|\t|\n|(var.+;)|(jQuery.+;)|(else.+;)|(cta.+;)|(inline_)|(if[(].+[)])',
                                  '', str(paragraph)).encode('ascii', 'ignore').decode("utf-8")).replace('{', '').replace('}', '')

    # less than 2 sentences returned, likely title/not article
    if articleText.count(".") <= 2:
        return ""

    return articleText


@app.route('/getcheck/', methods=['POST'])
def getCheck():
    content = request.json
    url = content['url']
    print(url)

    if url:
        linkList = getLinks()

        cleanText = getText(url)
        # percentage = getPercentage(cleanText)
        print(cleanText)
        print("succ")
        return jsonify(
            percentage="ssasaasas",
            link1=linkList['link1'],
            link2=linkList['link2'],
            link3=linkList['link3']
            # Add this option to distinct the POST request

        )
    else:
        print("fail")
        return jsonify({
            "none"
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Sage</h1>"


if __name__ == '__main__':
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    # getModel()
    app.run(threaded=True, port=5000)
