# Stack-overflow-Github-Crawler
crawl.py: Crawls some number of pages on github and stackoverflow. Fetches data from projects from github that include keyword "tensorflow". Fetches data from questions on stackoverflow that contain keyword "tensorflow". Takes the input of number of pages to crawl on github and number of pages to crawl on stack overflow(Each github page has 10 projects, each stackoverflow page has 15 questions). When finished, the code will display a table of the results from github and stackoverflow. Will also create csv files with the data in the table. Preferably, this and all other code should be run through command prompt instead of just opening the python file(So any error message will persist). If any error occurs while the code is running(will be displayed in command prompt) it is due to the fact that your ip has accessed stackoverflow or github too many times within a short period, causing either website to temporarily block your ip. If this happens, wait a bit before running the code again.


trending_projects.py: Crawls the waybackmachine archive for the scores of past github projects which include keyterm "tensorflow". The score of each project is calculated by adding the watch, stars, and fork count of each project. Then the projects are plotted on a graph. The X axis represents the number of months after the start of 2018(An x coordinate of 4 would represent 04/2018, and an X coordinate of 14 would represent 02/2019). The Y axis represents the score. Takes the input of number of pages to search through on github(1 page = 10 projects). This program will take a long time to run(input of 1 page takes about 20 minutes to run. To save the graph that the program produces, simply save the html file that the program displays. 



contributors.py: Crawls the top 10 github projects(Sorted by stars) that are about "Javascript Framework". Then the code takes the top 100 contributors of each project and gives them a score(Stars of project * commits of contributor), then ranks all the contributors which is displayed as a table and outputted as a csv file. Then, the projects are outputted as a csv file. Each line of the project csv file will contain the project link, the percent of all commits made by the top 10 contributors, and the percent of the top 10 contribtor's commits made by the to contributor. This data is then saved as a csv file. Finally, the code takes the input of number of users(starting from the highest score and descending) to create profiles for. Each profile contains the user's name, username, website, github profile, and number of followers on github. The user profile data is outputted as a csv.


Crawler Files: Contains all the output files all of all three programs. The files in "Crawler Files" are the outputs of the three programs that were executed on 8/15/2019.



Overall, there should not be any errors. Only a few errors are common:
1. Not all the prerequisites are installed
2. A invalid input is entered(All inputs must be positive integers)
3. "Chromedriver" not in path. If this is the case(only for the third program), you download chrome driver for your version of chrome and add it to path. Instructions should be in the error message.
4. The program "contributors.py" may freeze or crash. If the output log of the program stop outputting lines, this means that program has frozen. Simply run the program again to resolve the issue. If the program stops and does not display a table or output any csv files, this means the program has crashed while running. Simply reopen command prompt and run the program again. This is simply due to the nature of the selenium library.
5. All other errors are because you have acecessed a website too many times and the crawler is unable to fetch any data from the website because the website has temporary blocked your ip. This causes the code to fail as certain values will be set to empty string or 0, causing functions to fail. If this is the case, wait a few minutes before running the program again.





Prerequisites(NEED THESE TO WORK). On the left of the colon is the name of the library and on the right of the colon is the pip command to install said library. If for any reason you had downloaded all the prerequisites but a program crashes with the error message that "xxxx" was missing and you may need to download a library, simply download and install the library detailed in the error message with pip: 

Python 3.6(Not a library)(Must be added to PATH)

Requests: pip install requests

BeautifulSoup: pip install beautifulsoup4

plotly: pip install plotly

urllib3: pip install urllib3

lxml(parser): pip install lxml

html5lib(parser): pip install html5lib

Selenium: pip install selenium(Only used for contributors.py Most likely you will get an error message saying chromedriver needs to be added to PATH. If this is the case, download the chrome web driver for your version of chrome and add it to PATH)

The Prerequisities must be installed or else the code will not work.
