# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import urllib
!sudo pip3 install fake_useragent
!sudo pip3 install bs4

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

!sudo pip3 install tldextract
import tldextract

from urllib.parse import urlparse

def getSearch(title):
    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    text = title
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    entities = client.analyze_entities(document=document)

    search = ""

    i = 0;
    for entity in entities.entities:
        search += entity.name + " "
        i += 1
        if i == 3:
            break
    
    return search

def searchURL(query):
    query = urllib.parse.quote_plus(query) # Format into URL encoding
    number_result = 20

    ua = UserAgent()

    google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")

    result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

    links = []
    titles = []

    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href = True)
            title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
        
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
    
    query = urllib.parse.quote_plus(query) # Format into URL encoding
    number_result = 20
    
    ua = UserAgent()

    google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")

    result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

    links = []
    titles = []
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href = True)
            title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
        
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
