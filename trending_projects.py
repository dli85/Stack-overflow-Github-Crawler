import requests
from bs4 import BeautifulSoup
import time
import plotly.graph_objects as go
import urllib3
import plotly.graph_objects as go
# import plotly.express as px
import csv

fig = go.Figure()

git_total_count = 0
stack_total_count = 0

git_total_progress = 0
git_current_progress = 0

stack_total_progress = 0
stack_current_progress = 0

git_id = 1

stack_id = 1

github_trending = []


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='¦'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  :z suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    # if iteration == total:
    #    print()


def initialize_twodlist(rows, cols):
    twod_list = []
    new = []
    for i in range(0, rows):
        for j in range(0, cols):
            new.append("0")
        twod_list.append(new)
        new = []
    return twod_list


def github_crawler(pages):
    global github_trending

    names = []

    for i in range(1, pages + 1):
        urlPart1 = "https://github.com/search?p=" + str(i)
        urlPart2 = "&q=tensorflow&ref=simplesearch&type=Repositories&utf8=?"
        super_url = urlPart1 + urlPart2

        source_code = requests.get(super_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html5lib')

        for link in soup.findAll('div', {'class': 'col-12 col-md-8 pr-md-3'}):

            for link2 in link.findAll('a', {'class': 'v-align-middle'}):
                href = "http://github.com/" + link2.get('href')
                names.append(href)

    count = 0

    for i in range(0, len(names)):

        temp = get_graph_data(get_data(names[i]))

        if (len(temp) > 0):
            github_trending.append(temp)

            count += 1
            print("")
            print("")
            print(str(i + 1) + " of " + str(len(names)) + " completed")
            print("")
            print("")

    for i in range(0, len(github_trending)):

        url = github_trending[i][0]
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html5lib')

        score = 0

        for link in soup.findAll('a', {'class': 'social-count'}):
            score += int((' '.join(link.findAll(text=True)).rstrip().lstrip()).replace(",", ""), 10)

        github_trending[i][1].append([24, score])


def get_data(url):
    current_date = "20180101"
    end_date = "20190625"

    returnable = [url]
    url = 'https://web.archive.org/web/' + current_date + "/" + url

    duplicates = set([])

    crash_detect = set([])
    incrament = 0

    while (int(current_date) <= int(end_date)):

        print(url)
        http = urllib3.PoolManager()

        response = http.request('GET', url)

        time.sleep(2)
        soup = BeautifulSoup(response.data, 'lxml')

        if ("The Wayback Machine has not archived that URL." in str(soup)):
            print("Instance failed. Waybackmachine does not have archives on this link")
            return []

        count = 0

        link_date = ""

        month = ""
        day = ""
        year = ""

        count = 0

        for link in soup.findAll('td', {'class': 'c'}):
            if (count == 0):
                month = ' '.join(link.findAll(text=True)).rstrip().lstrip()
                count += 1
            elif (count == 1):
                day = ' '.join(link.findAll(text=True)).rstrip().lstrip()
                count += 1
            elif (count == 2):
                year = ' '.join(link.findAll(text=True)).rstrip().lstrip()
                break
        print("Current: " + get_url_date(url))
        print("Next: " + year + " " + month + " " + day)
        current_date = convert_to_date(month, day, year)

        print(current_date)

        month_year = current_date[0:6]

        count = 0

        if ((month_year not in duplicates) and (int(month_year, 10) >= 201801) and (incrament == 0)):
            print("url added")
            returnable.append(url)

            duplicates.add(month_year)

        for link in soup.findAll('td', attrs={'class': 'f'}):
            if (count == 1):
                if ("href" in str(link)):

                    url = link.find("a")['href']
                    break
                else:
                    return returnable

            count += 1

        if (url in crash_detect):
            current_date = get_next_month(current_date, incrament)
            incrament += 1
            url = 'https://web.archive.org/web/' + current_date + "/" + returnable[0]
            print("Next Date:" + current_date)

        else:
            incrament = 0

        crash_detect.add(url)

    return returnable


def get_graph_data(urls):
    time.sleep(2)
    if len(urls) > 0:
        result = [urls[0], []]

        for url in urls:
            if ("web.archive" in url):
                entry = []
                month = url[32:34]
                year = url[28:32]

                appendable = (int(year) - 2018) * 12 + int(month)

                entry.append(appendable)

                score = 0

                source_code = requests.get(url)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, 'html5lib')

                for link in soup.findAll('ul', {'class': 'pagehead-actions'}):
                    for link2 in link.findAll('a', {'class': 'social-count'}):
                        score += int((' '.join(link2.findAll(text=True)).rstrip().lstrip()).replace(",", ""), 10)

                entry.append(score)
                result[1].append(entry)
        return result
    else:
        return []


def get_url_date(url):
    return url[28:36]


def convert_to_date(month, day, year):
    real_month = ""

    if (month.upper() == "JAN"):
        real_month = "01"
    elif (month.upper() == "FEB"):
        real_month = "02"
    elif (month.upper() == "MAR"):
        real_month = "03"
    elif (month.upper() == "APR"):
        real_month = "04"
    elif (month.upper() == "MAY"):
        real_month = "05"
    elif (month.upper() == "JUN"):
        real_month = "06"
    elif (month.upper() == "JUL"):
        real_month = "07"
    elif (month.upper() == "AUG"):
        real_month = "08"
    elif (month.upper() == "SEP"):
        real_month = "09"
    elif (month.upper() == "OCT"):
        real_month = "10"
    elif (month.upper() == "NOV"):
        real_month = "11"
    elif (month.upper() == "DEC"):
        real_month = "12"

    return year + real_month + day


def get_next_month(date, incrament):
    year = ""
    month = ""
    day = ""
    for i in date:
        if (len(year) < 4):
            year += i
        elif (len(month) < 2):
            month += i
        else:
            day += i

    temp_year = int(year)
    temp_month = int(month)

    temp_month += incrament
    if (temp_month == 13):
        temp_year += 1
        temp_month = temp_month - 12

    if (temp_month < 10):
        temp_month = "0" + str(temp_month)

    return str(temp_year) + str(temp_month) + str("17")


github_crawler(int(input("Enter number of pages")))

# get_data("http://github.com//jikexueyuanwiki/tensorflow-zh")


# run_x_times_git(int(input("Please enter the number of pages that you want to crawl on github: ")))

fig = go.Figure()
name_list = []


def sort_by_second(val):
    return val[1][len(val[1]) - 1][1]


github_trending.sort(key=sort_by_second, reverse=True)

# [link, [[1,2],[1,2],[1,2]]]

with open('trending.csv', mode='w') as writeFile:
    trending_write = csv.writer(writeFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in github_trending:
        result = []
        result.append(i[0])
        result.append(len(i[1]))
        for p in i[1]:
            result.append(p[0])
            result.append(p[1])

        trending_write.writerow(result)

for i in range(0, len(github_trending)):

    xs = []

    ys = []

    name1 = str(str(i + 1) + " " + github_trending[i][0])

    for p in range(0, len(github_trending[i][1])):
        xs.append(github_trending[i][1][p][0])
        ys.append(github_trending[i][1][p][1])

    name_list.append(str(i + 1) + " " + name1)

    fig.add_trace(go.Scatter(
        x=xs,
        y=ys,
        name=name1
    ))

temp = go.Figure(data=[go.Table(header=dict(values=["Name"]),
                                cells=dict(values=[name_list])
                                )])
temp.show()
fig.show()

print('')
print('')

input("Press any key")

