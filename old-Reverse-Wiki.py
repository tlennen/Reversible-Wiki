# Created by Tyler Lennen <tlennen@ucmerced.edu>
# Last checked: March 15, 2018
# Wikipedia Scrapper that checks reversible links of a web page
# Reversible link means that the page links to the original web page

import requests
from bs4 import BeautifulSoup as Soup

class Wikipage(object):
    # stores a web page and the links in its body
    # title and link will always be in the same place

    def __init__(self, href):
        self.my_connections = []  # links of the page
        self.my_titles = []  # titles of the links
        self.href = href  # this is the main link
        self.name = href  # Used as the name of the wiki page, changed later

    def add_connection(self, connect):
        # set my_connections equal to the links page has
        self.my_connections.append(connect)

    def add_titles(self, titles):
        # sets the names of titles
        self.my_titles.append(titles)

    def print_connections(self):
        # prints out titles of the connections
        for x in self.my_titles:
            print(" ->", x)

class ConnectWikis(object):
    def __init__(self):
        self.global_count = 0
        self.start_url = ""
        self.list_of_wikis = []  # Contains all WikiPage Objects
        self.reverses = []

    def wiki_spider(self, my_url):
        # collects the links of a wiki page and stores them
        for x in self.list_of_wikis:  # prevents repeats in the list of wikis
            if str(x.href) == str(my_url):
                return 0

        source_page = Wikipage(my_url)
        html_file = Soup(requests.get(my_url, "html.parser").text, "html.parser")
        links = html_file.find_all("a")
        page_name = str(html_file.find("h1", attrs={"id":"firstHeading"}).contents[0])
        # Above code searches html for titles and links

        if page_name[0][0] == "<":  # Stops some formatting errors
            page_name = page_name[3:len(page_name)-4]
        source_page.name = page_name

        for x in links:  # adds connections from links to the source_page
            href = str(x.get("href"))
            if str(x.get("title"))[0:24] == "Edit section: References":  # Removes links from the tables below the page
                break
            if href[0:6] == "/wiki/" and href.find(":") == -1:  # Filters non-wiki links
                source_page.add_connection(href)
                source_page.add_titles(str(x.get("title")))

        self.list_of_wikis.append(source_page)
        self.global_count += 1
        print("VISITING PAGE OF:", source_page.name)

    def collect_pages(self, my_url):
        # Finds the links of the original url and saves them into Wiki page objects
        self.wiki_spider(my_url)
        self.start_url = my_url
        for x in range(0, len(self.list_of_wikis[0].my_connections)):
            my_url = "https://en.wikipedia.org" + self.list_of_wikis[0].my_connections[x]
            self.wiki_spider(my_url)

    def ask_user_input(self):
        # Asks the user for input and checks if the input is valid
        check = True
        while check:
            wiki_url = input("Enter a valid wikipedia url: https://en.wikipedia.org/wiki/")
            wiki_url = "https://en.wikipedia.org/wiki/" + wiki_url
            request = requests.get(wiki_url)
            if request.status_code != 200:
                print('Page could not be found')
            else:
                check = False
        return wiki_url

    def print_all_connections(self):
        # Prints out all the links of pages in the list
        for x in self.list_of_wikis:
            print(x.print_connections())

    def check_reverse(self):  # "Done"
        # Checks the list of wikis to see if they loop back
        for x in self.list_of_wikis:
            for y in x.my_connections:
                # all connections of each page, checks for the start_url
                if y == self.start_url[24:]:
                    if x not in self.reverses:  # prevents repeats
                        self.reverses.append(x)
        print("LIST OF REVERSES")
        for x in self.reverses:
            print(" Reversible:", x.name)
        print("REVERSE SIZE IS:", len(self.reverses))

def reversible_wiki():
    # runs the program
    connect = ConnectWikis()
    hold = connect.ask_user_input();
    connect.collect_pages(hold)
    connect.print_all_connections()
    connect.check_reverse()
    print("Unique links visited: " + str(connect.global_count))

reversible_wiki()
