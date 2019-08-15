import requests
from bs4 import BeautifulSoup
import time
import plotly.graph_objects as go
import csv
import os

fig = go.Figure()

git_total_count = 0
stack_total_count = 0

git_total_progress = 0
git_current_progress = 0

stack_total_progress = 0
stack_current_progress = 0

git_id = 1

stack_id = 1

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    #if iteration == total:
    #    print()

def write_csv(data_matrix, header, csv_output_name):
    with open(csv_output_name, mode='w') as csv_file:
        data_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data_writer.writerow(header)

        for i in range( len(data_matrix)):
            data_writer.writerow(data_matrix[i])



def run_x_times_stack(x):

    if(x == 0):
        return

    global stack_total_progress
    global stack_current_progress

    stack_total_progress = x
    stack_current_progress = 0

    data_matrix = []

    i = 1
    while i <= x:
        data_matrix = sof_spider(i, data_matrix)
        i+=1
        time.sleep(3)



    write_csv(data_matrix, ['Stack id', 'Question Title', 'Question Link', 'Number of Upvotes', 'Date Created', 'Views', 'Last Active'], 'stack.csv')

    tempList = []
    filler_data_matrix = initialize_twodlist(7, stack_total_count)

    #
    for j in range(len(data_matrix[0])):
        for i in range(len(data_matrix)):
            tempList.append(data_matrix[i][j])

    count = 0

    for i in range(len(filler_data_matrix)):
        for j in range(len(filler_data_matrix[i])):
            filler_data_matrix[i][j] = tempList[count]
            count += 1

    fig = go.Figure(data=[go.Table(header=dict(
        values=['Stack id', 'Question Title', 'Question Link', 'Number of Upvotes', 'Date Created', 'Last Active', 'Views']),
        cells=dict(values=filler_data_matrix)),

    ])
    fig.show()


def run_x_times_git(x):

    if(x == 0):
        return

    data_matrix = []

    global git_total_progress
    global git_current_progress

    git_total_progress = x
    git_current_progress = 0

    i = 1

    while i <= x:
        data_matrix = github_crawler(i, data_matrix)
        i+=1
        time.sleep(3)


    write_csv(data_matrix, ['Project_id', 'Project Name', 'Project Link', 'Project Issues', 'Pull Requests', 'Watch', 'Stars', 'Fork'], 'github.csv')


    tempList = []
    filler_data_matrix = initialize_twodlist(8, git_total_count)
    for j in range(len(data_matrix[0])):
        for i in range(len(data_matrix)):
            tempList.append(data_matrix[i][j])

    print("")
    count = 0

    for i in range(len(filler_data_matrix)):
        for j in range(len(filler_data_matrix[i])):
            filler_data_matrix[i][j] = tempList[count]
            count+=1

    fig = go.Figure(data=[go.Table(
                        header=dict(values=["Project id", "Project Name", "Project Link", "Project Issues", "Pull Requests", "Watch", "Stars", "Fork"]),
                            cells=dict(values=filler_data_matrix))
                          ])
    fig.show()


def initialize_twodlist(rows, cols):
    twod_list = []
    new = []
    for i in range (0, rows):
        for j in range (0, cols):
            new.append("0")
        twod_list.append(new)
        new = []
    return twod_list


def github_crawler(page, data_matrix):

    global git_total_progress
    global git_current_progress

    global git_id

    urlPart1 = "https://github.com/search?p=" + str(page)
    urlPart2 = "&q=tensorflow&ref=simplesearch&type=Repositories&utf8=✓"
    super_url = urlPart1 + urlPart2

    source_code = requests.get(super_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html5lib')
    count = 0

    project_count = 0

    for link in soup.findAll('div', {'class': 'col-12 col-md-8 pr-md-3'}):
        project_count+=1

    if(project_count == 0):
        print("You have accessed the website too many times")


    increase = 1 / project_count


    global git_total_count
    git_total_count+= project_count

    for link in soup.findAll('div', {'class': 'col-12 col-md-8 pr-md-3'}):

        for link2 in link.findAll('a', {'class': 'v-align-middle'}):

            pretty_name = ""
            pretty_link = ""
            pretty_issues = ""
            pretty_pull_requests = ""
            pretty_watch = ""
            pretty_stars = ""
            pretty_fork = ""




            href = "http://github.com/" + link2.get('href')
            project_title = ' '.join(link2.findAll(text=True))
            project_link = href
            project_soup = BeautifulSoup(requests.get(project_link).text, 'html5lib')
            counter = 0 #0 for issues, 1 for pull requests
            git_id = git_id



            pretty_name = project_title
            pretty_link = href

            for link3 in project_soup.findAll('span', {'class': 'Counter'}):
                if(counter == 0):
                    project_issues = ' '.join(link3.findAll(text=True))

                    pretty_issues = project_issues

                if(counter == 1):
                    project_pull_requests = ' '.join(link3.findAll(text=True))

                    pretty_pull_requests = project_pull_requests

                    break
                counter+=1







            counter = 0 #0 == watch, 1 == stars, 2 == fork

            for link3 in project_soup.findAll('a', {'class': 'social-count'}):
                if(counter == 0):
                    project_social_count = ' '.join(link3.findAll(text=True)).lstrip().rstrip()

                    pretty_watch = project_social_count

                if(counter == 1):
                    project_stars = ' '.join(link3.findAll(text=True)).lstrip().rstrip()

                    pretty_stars = project_stars

                if(counter == 2):
                    project_fork = ' '.join(link3.findAll(text=True)).lstrip().rstrip()

                    pretty_fork = project_fork

                counter+=1

            data_matrix.append([git_id, pretty_name, pretty_link, pretty_issues, pretty_pull_requests, pretty_watch, pretty_stars, pretty_fork])

            git_current_progress += increase

            git_id += 1

            printProgressBar(git_current_progress, git_total_progress)
            #print(git_current_progress, end='\r')


    return data_matrix





def sof_spider(page, data_matrix):
    global stack_total_progress
    global stack_current_progress

    global stack_id


    urlPart1 = "https://stackoverflow.com/search?page=" + str(page)
    urlPart2 = "&tab=Relevance&q=%5btensorflow%5d%20tensorflow"
    super_url = urlPart1 + urlPart2



    source_code = requests.get(super_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html5lib')

    question_count = 0

    for link in soup.findAll('a', {'class': 'question-hyperlink'}):
        identifier = link.get('class')
        if(len(identifier) == 1):
            question_count+=1

    if(question_count == 0):
        print("You have accessed the website too many times")


    increase = 1 / question_count


    global stack_total_count

    stack_total_count += question_count

    count = 0

    for link in soup.findAll('a', {'class': 'question-hyperlink'}):
        #sees if the class is ONLY question-hyperlink
        identifier = link.get('class')
        #only get the questions
        if(len(identifier) == 1):
            href = link.get('href')
            question_title = ' '.join(link.findAll(text=True))
            question_title = question_title.lstrip().rstrip()

            data_question_title = ""
            data_question_link = ""
            data_question_upvotes = ""
            data_question_date_created = ""
            data_question_views = ""
            data_question_last_active = ""
            stack_id = stack_id


            data_question_title = question_title


            question_link = "http://stackoverflow.com" + href
            data_question_link = question_link
            question_soup = BeautifulSoup(requests.get(question_link).text, 'html5lib')

            for question_link in question_soup.findAll('div', {'class': "js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center"}):
                num_upvotes = ' '.join(question_link.findAll(text=True))
                data_question_upvotes = num_upvotes
                break

            counter = 0;

            for question_link in question_soup.findAll('div', {'class': "grid fw-wrap pb8 mb16 bb bc-black-2"}):
                for question_link2 in question_link.findAll('div'):
                    if(counter == 0):
                        date_created = ' '.join(question_link2.findAll(text=True)).replace("Asked", "").lstrip().rstrip()
                        data_question_date_created = date_created
                    if(counter == 1):
                        view_count = ' '.join(question_link2.findAll(text=True)).replace("Active","").lstrip().rstrip()
                        data_question_views = view_count
                    if(counter == 2):
                        last_active = ' '.join(question_link2.findAll(text=True)).replace("Viewed","").replace("times", "").lstrip().rstrip()
                        data_question_last_active = last_active

                    counter+=1


            data_matrix.append([stack_id, data_question_title, data_question_link, data_question_upvotes, data_question_date_created, data_question_views,data_question_last_active])
            count += 1

            stack_current_progress += increase

            stack_id+=1

            printProgressBar(stack_current_progress, stack_total_progress)

    return data_matrix


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

createFolder("csv_files")

run_x_times_git(int(input("Please enter the number of pages that you want to crawl on github: ")))



run_x_times_stack(int(input("Please enter the number of pages that you want to crawl on Stack Overflow: ")))

