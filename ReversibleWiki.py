# Created by Tyler Lennen <tlennen@ucmerced.edu>
# Last Checked: 8/9/2019
# Wikipedia Scrapper that checks reversible links of a web page
# Reversible link means that the page links to the original web page

import requests
from bs4 import BeautifulSoup
from Wikipage import Wikipage


def input_start_wiki_page():
    # Asks the user for input and checks if the input is valid
    valid_input = True
    prefix = "https://en.wikipedia.org/wiki/"
    while valid_input:
        wiki_url = prefix + input("Enter a valid Wikipedia url: https://en.wikipedia.org/wiki/")
        status = requests.get(wiki_url)
        if status.status_code != 200:
            print('Page could not be found')
        else:
            valid_input = False
    return wiki_url


def gather_links_of_page(web_page):
    html_file = BeautifulSoup(requests.get(web_page.my_url).text, "html.parser")
    links = html_file.find_all("a")
    connections = clean_links(links, web_page.my_url)
    web_page.add_connections(connections)
    page_name = str(html_file.find("h1", attrs={"id": "firstHeading"}).contents[0])
    if page_name[0][0] == "<":  # Stops some formatting errors
        page_name = page_name[3:len(page_name) - 4]
    web_page.name = page_name
    return web_page


def clean_links(links, original_url):
    returned_links = []
    for link in links:  # adds connections from links to the source_page
        href = str(link.get("href"))
        if str(link.get("title"))[0:24] == "Edit section: References":  # Removes links from the tables below the page
            pass
        elif len(href) < 6 or href == "/wiki/Main_Page":
            pass
        elif original_url == "https://en.wikipedia.org"+href:
            pass
        elif href[0:6] == "/wiki/" and href.find(":") == -1:  # Filters non-wiki links
            returned_links.append(href)
    return returned_links


def visit_all_links(links):
    list_of_wiki_pages = []
    for link in links:
        visited_page = Wikipage("https://en.wikipedia.org"+link)
        visited_page = gather_links_of_page(visited_page)
        list_of_wiki_pages.append(visited_page)
        print("Page added, href:"+link)
    return list_of_wiki_pages


def check_for_loops(visited_list, start_url,num_links):
    looped_links = []
    looped_names = []
    # Checks the list of wikis to see if they loop back
    for web_page in visited_list:
        for link in web_page.my_connections:
            # all connections of each page, checks for the start_url
            if link == start_url[24:]:
                if web_page.name not in looped_names:
                    looped_links.append(web_page)
                    looped_names.append(web_page.name)
    print("LIST OF REVERSES")
    for x in looped_links:
        print(" Reversible:", x.name)
    print("REVERSE SIZE IS:", len(looped_links))
    print("Out of this many links:", len(visited_list))


if __name__ == "__main__":
    start_url = input_start_wiki_page()
    original_wiki = Wikipage(start_url)
    original_wiki = gather_links_of_page(original_wiki)
    original_wiki.print_connections()
    visited_list = visit_all_links(original_wiki.get_connections())
    check_for_loops(visited_list, original_wiki.my_url,len(original_wiki.get_connections()))
