"""
This module is used to organize the links of the wikipedia pages in an orderly fashion.
"""


class Wikipage():
    # stores a web page and the links in its body
    # title and link will always be in the same place

    def __init__(self, href):
        self.my_connections = []  # links of the page
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