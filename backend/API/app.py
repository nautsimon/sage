# app.py
import urllib.request
import urllib
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify
import requests

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from fake_useragent import UserAgent
import tldextract
from urllib.parse import urlparse

# import pandas as pd
# import pickle
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from keras.models import Model, load_model
# import keras
# import tensorflow
import sys
import os
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

app = Flask(__name__)

model = None

whitelist = ["https://www.cnn.com/",
             "https://www.foxnews.com/",
             "https://www.theonion.com/",
             "https://abcnews.go.com/",
             "https://www.nbcnews.com/",
             "https://www.huffpost.com/",
             "https://www.cbsnews.com/",
             "https://www.usatoday.com/",
             "https://www.buzzfeed.com/",
             "https://www.nytimes.com/",
             "https://www.dailymail.co.uk/",
             "https://www.washingtonpost.com/",
             "https://www.businessinsider.com/",
             "https://www.bbc.com/",
             "https://www.cnet.com/",
             "https://www.theguardian.com/us",
             "https://www.msn.com/en-us/news",
             "https://www.npr.org/",
             "https://www.nydailynews.com/",
             "https://www.latimes.com/",
             "https://nypost.com/",
             "https://time.com/",
             "https://mashable.com/",
             "https://www.sfgate.com/",
             "https://news.yahoo.com/",
             "https://www.breitbart.com/",
             "https://slate.com/",
             "https://www.upworthy.com/",
             "https://www.theblaze.com/",
             "https://www.telegraph.co.uk/",
             "https://www.usnews.com/",
             "https://www.vice.com/en_us/",
             "https://www.vox.com/",
             "https://www.chicagotribune.com/",
             "http://www.thedailybeast.com/",
             "https://www.salon.com/",
             "https://www.independent.co.uk/us",
             "https://www.bostonglobe.com/",
             "https://www.theatlantic.com/",
             "http://www.cap-news.com/",
             "https://www.aljazeera.com/",
             "https://empirenews.net/",
             "http://bigamericannews.com/",
             "http://nationalreport.net/",
             "http://www.newsmutiny.com/Index.html",
             "https://www.theonion.com/",
             "https://www.dailysquib.co.uk/",
             "http://farzinews.com/",
             "http://www.newsbiscuit.com/",
             "http://www.theshovel.com.au/",
             "https://www.economist.com/",
             "https://www.politico.com/",
             "https://www.foreignaffairs.com/",
             "https://www.reuters.com/",
             "https://www.forbes.com/",
             "https://time.com/",
             "https://www.nationalgeographic.com/",
             "https://entertainment.theonion.com/",
             "https://local.theonion.com/",
             "https://sports.theonion.com/",
             "https://political.theonion.com/",
             "https://ogn.theonion.com/"
             ]


def getSearch(title):
    # Instantiates a client
    client = language.LanguageServiceClient.from_service_account_json(
        "sage-nlp-93b91d36aae5.json")

    # The text to analyze
    text = title
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    entities = client.analyze_entities(document=document)

    search = ""

    i = 0
    for entity in entities.entities:
        search += entity.name + " "
        i += 1
        if i == 3:
            break

    return search


def searchURL(query):
    query = urllib.parse.quote_plus(query)  # Format into URL encoding
    number_result = 20

    ua = UserAgent()

    google_url = "https://www.google.com/search?q=" + \
        query + "&num=" + str(number_result)
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")

    result_div = soup.find_all('div', attrs={'class': 'ZINbbc'})

    links = []
    titles = []

    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
            title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()

            # Check to make sure everything is present before appending
            if link != '' and title != '':
                links.append(link['href'])
                titles.append(title)
        # Next loop if one element is not present
        except:
            continue

    index = 0
    count = 0
    for link in links:
        if link == query:
            index = count
        count += 1

    return titles[index]


def searchRelated(query, domain, count):

    query = urllib.parse.quote_plus(query)  # Format into URL encoding
    number_result = 20

    ua = UserAgent()

    google_url = "https://www.google.com/search?q=" + \
        query + "&num=" + str(number_result)
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")

    result_div = soup.find_all('div', attrs={'class': 'ZINbbc'})

    links = []
    titles = []
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
            title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()

            # Check to make sure everything is present before appending
            if link != '' and title != '':
                links.append(link['href'])
                titles.append(title)
        # Next loop if one element is not present
        except:
            continue

    results = []

    i = 0
    for link in links:
        link = link[7:]
        o = urlparse(link)

        link_new = o.scheme + "://" + o.netloc + o.path

        ext = tldextract.extract(link_new)

        if ext.domain != domain:
            results.append(link_new)
            i += 1
        if i == count:
            break

    return results


def simon(URL, count):

    ext = tldextract.extract(URL)
    domain = ext.domain

    title = searchURL(URL)
    print(title)
    search = getSearch(title)
    print(search)
    links = searchRelated(search, domain, count)

    links_cleaned = []
    websites = []

    for link in links:
        junk = link.find("&sa=")
        link = link[:junk]
        links_cleaned.append(link)
        ext = tldextract.extract(link)
        websites.append(ext.domain + "." + ext.suffix)

    return links_cleaned, websites


def getModel():
    global model
    model = load_model('sage.h5')


def getPercentage(cleanText):
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    TESTDATA = StringIO()
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

    goodUrl = 0
    if url:
        for link in whitelist:
            print(link + url)
            if (link in url and link != url):
                print("yeeet")
                goodUrl = 1
    if goodUrl == 1:

        rawLink = simon(url, 3)
        fullLink = rawLink[0]
        titleLink = rawLink[1]
        cleanText = getText(url)
        linkPerc = ["10", "30", "20"]
        # percentage = getPercentage(cleanText)
        print(cleanText)
        print("succ")
        return jsonify(
            percentage="92",
            link1=fullLink[0],
            link2=fullLink[1],
            link3=fullLink[2],
            linkTitle1=titleLink[0],
            linkTitle2=titleLink[1],
            linkTitle3=titleLink[2],
            linkPerc1=linkPerc[0],
            linkPerc2=linkPerc[1],
            linkPerc3=linkPerc[2]
            # Add this option to distinct the POST request

        )
    else:
        print("fail")
        return jsonify(
            percentage="fail"
        )

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Sage</h1>"


if __name__ == '__main__':
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    # getModel()
    app.run(threaded=True, port=5000)
