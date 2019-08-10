"""
This module is used to organize the links of the wikipedia pages in an orderly fashion.
"""

__author__ = "Tyler Lennen"
__version__ = "1.0.1"


class Wikipage:
    """
    Wikipage stores the url, name, and the links of a Wikipedia page.
    Organizes the data for wiki_scraper.py.
    """

    def __init__(self, my_url):
        self._my_connections = []  # links of the page
        self.my_url = my_url  # this is the main link
        self.name = my_url  # Used as the name of the wiki page, changed later

    def __repr__(self):
        return "Wikipage()"

    def print_connections(self):
        """Prints all href links of a Wikipage"""
        # prints out titles of the connections
        for connection in self._my_connections:
            print("->", connection)

    @property
    def my_connections(self):
        """Returns list of wikipages links"""
        return self._my_connections

    @my_connections.setter
    def my_connections(self, connections):
        """Sets my_connections equal to a list of links"""
        self._my_connections = connections
