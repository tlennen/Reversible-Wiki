# Created by Tyler Lennen <tlennen@ucmerced.edu>
# NOT READY YET
# Wikipedia Scrapper that checks reversible links of a web page
# Reversible link means that the page links to the original web page

import requests
from bs4 import BeautifulSoup, SoupStrainer
from Wikipage import Wikipage


def input_start_webpage():
    # Asks the user for input and checks if the input is valid
    check = True
    prefix = "https://en.wikipedia.org/wiki/"
    while check:
        wiki_url = prefix + input("Enter a valid Wikipedia url: https://en.wikipedia.org/wiki/")
        status = requests.get(wiki_url)
        if status.status_code != 200:
            print('Page could not be found')
        else:
            check = False
    return wiki_url


def gather_links_of_page(web_page):
    response = requests.get(web_page, "html.parser").text, "html.parser"

    for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            print(link['href'])












if __name__ =="__main__":
    start_url = input_start_webpage()
    original_wiki = Wikipage(start_url)
    gather_links_of_page(original_wiki)
