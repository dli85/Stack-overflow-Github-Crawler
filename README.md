# Stack-overflow-Github-Crawler
Crawl.py: Crawls some number of pages on github and stackoverflow. Fetches data from projects from github that include keyword "tensorflow". Fetches data from questions on stackoverflow that contain keyword "tensorflow". Takes the input of number of pages to crawl on github and number of pages to crawl on stack overflow(Each github page has 10 projects, each stackoverflow page has 15 questions). When finished, the code will display a table of the results from github and stackoverflow. Will also create csv files with the data in the table. Preferably, this and all other code should be run through command prompt instead of just opening the python file(So any error message will persist). If any error occurs while the code is running(will be displayed in command prompt) it is due to the fact that your ip has accessed stackoverflow or github too many times within a short period, causing either website to temporarily block your ip. If this happens, wait a bit before running the code again.




Prerequisites: 



Requests: pip install requests

BeautifulSoup: pip install beautifulsoup4

plotly: pip install plotly

Selenium: pip install selenium

The Prerequisities must be installed or else the code will not work.
