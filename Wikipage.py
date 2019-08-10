"""
This module is used to organize the links of the wikipedia pages in an orderly fashion.
"""


class Wikipage():
    # stores a web page and the links in its body
    # title and link will always be in the same place

    def __init__(self, my_url):
        self.my_connections = []  # links of the page
        self.my_url = my_url  # this is the main link
        self.name = my_url  # Used as the name of the wiki page, changed later

    def __repr__(self):
        return "Wikipage()"

    def print_connections(self):
        # prints out titles of the connections
        for connection in self.my_connections:
            print("->", connection)

    def add_connections(self, connections):
        # set my_connections equal to the links page has
        self.my_connections = connections

    def get_connections(self):
        return self.my_connections
