# Reversible-Wiki

Reversible Wiki is a Python web scraper that reads in a Wikipedia url and reads all of its links. It then checks if any of those links go back to the original page. Python packages used are BeautifulSoup4 and requests. 

When first running the program, you will be met with the following line:

Enter a valid wikipedia url: https://en.wikipedia.org/wiki/

Simply enter the last part of the url in order to find a specific Wikipedia page. If the page is not found, you will be prompted again.
It is recommended that the url is directly taken from the wikipedia page. Redirects will cause the program to not detect reversible links.
The program may take a while to run, as it is collecting the html files from these pages. Smaller wikipedia pages are recommended because of this, but larger ones will still work. Examples of smaller Wikipedia pages are below.

https://en.wikipedia.org/wiki/Apple_sauce

https://en.wikipedia.org/wiki/Nutella
