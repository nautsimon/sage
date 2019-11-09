# app.py
import urllib.request
from bs4 import BeautifulSoup
import re

from flask import Flask, request, jsonify
app = Flask(__name__)


def getPercentage():
    return 90


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
    linkList = getLinks()
    percentage = getPercentage()
    cleanText = getText(url)
    print(cleanText)
    if url:
        print("succ")
        return jsonify({
            "percentage": f"{percentage}",
            "link1": f"{linkList['link1']}",
            "link2": f"{linkList['link2']}",
            "link3": f"{linkList['link3']}"
            # Add this option to distinct the POST request

        })
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
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
