"""Wiki Scraper is a Python 3 project designed to find a looped link in a given Wikipedia web page.
The user inputs a Wikipedia page, and the program collects all the links from that page. The program
then visits those links to see if they link back to the original page. An example of this is
Apple->Apple sauce->Apple. All wikipedia pages that loop are outputted on the console and the total
number of links is outputted.

Created by: Tyler Lennen in the winter of 2017
Last updated: August 2019
"""

__author__ = "Tyler Lennen"
__version__ = "1.1.0"


import requests
from bs4 import BeautifulSoup
from wikipage import Wikipage


def input_start_wiki_page():
    """
    Takes in a Wikipedia URL and checks that it can be found. Returns valid Wikipedia URL.
    """

    valid_input = True
    prefix = "https://en.wikipedia.org/wiki/"
    while valid_input:
        wiki_url = prefix + input("Enter a valid Wikipedia url(Case Sensitive): https://en.wikipedia.org/wiki/")
        status = requests.get(wiki_url)
        if status.status_code != 200:
            print('Page could not be found')
        else:
            valid_input = False
    return wiki_url


def gather_links_of_page(web_page):
    """
    Scrapes links from the given wikipedia page. Saves the page name and the list of connections
    to the wikipedia object. Returns Wikipage object with updated connections and name.
    """

    html_file = BeautifulSoup(requests.get(web_page.my_url).text, "html.parser")
    links = html_file.find_all("a")
    connections = clean_links(links, web_page.my_url)
    web_page.my_connections = connections
    page_name = str(html_file.find("h1", attrs={"id": "firstHeading"}).contents[0])
    if page_name[0][0] == "<":  # Stops some formatting errors
        page_name = page_name[3:len(page_name) - 4]
    web_page.name = page_name
    return web_page


def clean_links(links, original_url):
    """
    Takes list of links for a wikipedia page and removes unnecessary links. Non-wiki links,
    repeat links, self links, and links to parts of the page are removed. Returns "cleaned" links.
    """

    returned_links = set()
    for link in links:  # adds connections from links to the source_page
        href = str(link.get("href"))
        if str(link.get("title"))[0:24] == "Edit section: References":
            pass
        elif len(href) < 6 or href == "/wiki/Main_Page":
            pass
        elif original_url == "https://en.wikipedia.org"+href:
            pass
        elif href[0:6] == "/wiki/" and href.find(":") == -1:  # Filters non-wiki links
            returned_links.add(href)
    return returned_links


def visit_all_links(links):
    """
    Visits all given links and gathers the links and names of those pages. Wikipage objects are
    created for each visited page and a list of Wikipage objects is returned.
    """

    list_of_wiki_pages = []
    for link in links:
        visited_page = Wikipage("https://en.wikipedia.org"+link)
        visited_page = gather_links_of_page(visited_page)
        list_of_wiki_pages.append(visited_page)
        print("Page added, href:"+link)
    return list_of_wiki_pages


def check_for_loops(list_of_web_pages, start_url):
    """
    Checks all pages to see if they have a link back to the user's wikipedia page.
    Looped pages are saved and outputed to the console.
    """

    looped_links = []
    looped_names = []
    # Checks the list of wikis to see if they loop back
    for web_page in list_of_web_pages:
        for link in web_page.my_connections:
            # all connections of each page, checks for the start_url
            if link == start_url[24:]:
                if web_page.name not in looped_names:
                    looped_links.append(web_page)
                    looped_names.append(web_page.name)

    # Output all looped links
    print("LIST OF LOOPED LINKS")
    for link in looped_links:
        print(" Reversible:", link.name)
    print("Number of reversible links:", len(looped_links))
    print("Out of {num} links.".format(num=len(list_of_web_pages)))


def main():
    """
    Runs main program. Finds the Wikipedia pages that loop back to the user-inputted page.
    """

    original_page_url = input_start_wiki_page()
    original_wiki = Wikipage(original_page_url)

    original_wiki = gather_links_of_page(original_wiki)
    original_wiki.print_connections()

    visited_list = visit_all_links(original_wiki.my_connections)
    check_for_loops(visited_list, original_wiki.my_url)


if __name__ == "__main__":
    main()
