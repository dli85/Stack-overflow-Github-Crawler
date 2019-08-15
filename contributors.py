import requests
import plotly as py
import urllib3
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import plotly.graph_objects as go
import csv

cont_data = []

project_data = [] #Project link, #1 commits, Top 10 Commits, Total Commits

final_data = []

def run_x_times(x):
    for i in range(1, x+1):
        crawl(i)

def crawl(page_num):
    link = "https://github.com/search?o=desc&p="  + str(page_num) + "&q=javascript+framework&s=stars&type=Repositories"

    identifier = "repo-list-item d-flex flex-column flex-md-row flex-justify-start py-4 public source"

    list_of_links = get_list_project_links(link)

    for i in range(0,len(list_of_links)):
        get_data(list_of_links[i])



def get_list_project_links(search_page_link):

    results = []

    source_code = requests.get(search_page_link)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html5lib')

    for link in soup.findAll('li', {'class' : "repo-list-item d-flex flex-column flex-md-row flex-justify-start py-4 public source"}):
        for link2 in link.findAll('a', {'class' : "v-align-middle"}):
            results.append("https://github.com" + link2.get('href'))

    return (results)

def get_data(link):
    browser = webdriver.Chrome()
    good_link = link
    global cont_data;


    temp_score = []
    temp_name = []
    temp_link = []

    temp_rank = []

    '''
    #-- FireFox
    caps = webdriver.DesiredCapabilities().FIREFOX
    caps["marionette"] = True
    browser = webdriver.Firefox(capabilities=caps)
    '''

    url = link + "/graphs/contributors"
    browser.get(url)
    #inputElement = browser.find_elements_by_class_name("password-input")[0]
    #inputElement.send_keys("123hello")
    #inputElement.send_keys(Keys.RETURN)
    time.sleep(5)  # seconds

    # Give source code to BeautifulSoup
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()





    count = 0

    stars = 0

    for link in soup.findAll('a', {'class' : 'social-count js-social-count'}):
        stars = int(' '.join(link.findAll(text=True)).rstrip().lstrip().replace(",",""))

    for link in soup.findAll('a', {'data-hovercard-type' : 'user'}):
        if(count % 2 == 0):
            temp_link.append(link.get('href'))
            temp_name.append(link.get('href').replace("https://github.com/",""))
        count+=1

    for link in soup.findAll('a', {'class' : 'link-gray text-normal'}):
      temp_score.append(' '.join(link.findAll(text=True)).rstrip().lstrip())

    first = int(temp_score[0].replace(" ", "").replace("commit", "").replace(",","").replace("s", ""))
    t10 = 0
    total = 0

    for i in range(0, len(temp_score)):
        if (i >= 0 and i < 10):
            t10 += int(temp_score[i].replace(" ", "").replace("commit", "").replace(",","").replace("s", ""))
        total += int(temp_score[i].replace(" ", "").replace("commit", "").replace(",","").replace("s", ""))


    for i in range(0, len(temp_score)):
        temp_score[i] = int(temp_score[i].replace(" ", "").replace("commit", "").replace(",","").replace("s", "")) * stars



    project_data.append([good_link, first, t10, total])

    for i in range(0, len(temp_name)):
        if(i == 0):
            temp_rank.append("Leader")
        elif(i <= 9):
            temp_rank.append("Top 10")
        else:
            temp_rank.append("None")
    for i in range(0, len(temp_score)):
        cont_data.append([str("https://github.com") + temp_link[i], temp_name[i], temp_score[i], temp_rank[i]])




#get_data("https://github.com/vuejs/vue")







run_x_times(1)


def make_big_set():
    global final_data;
    for i in cont_data:

        does_contain = False

        for q in final_data:
            if(q[0] == i[0]):
                does_contain = True
                q[1] += i[2]

                if(q[2] == "Top 10" and i[3] == "Leader"):
                    q[2] = i[3]
                elif(q[2] == "None" and i[3] == "Top 10"):
                    q[2] = i[3]
                elif(q[2] == "None" and i[3] == "Leader"):
                    q[2] = i[3]




        if(does_contain == False):
            final_data.append([i[0], i[2], i[3]])

#for i in cont_data:
#    print(i)


make_big_set()


def sort_by_second(val):
    return val[1]


final_data.sort(key=sort_by_second, reverse=True)

for i in range(0, 25):
    print("")

print("There are " + str(len(final_data)) + " contributors displayed, organized by score. Score for each contributor is calculated by multiplying their commits by the number of stars the project has")





names = []
scores = []
ranks = []
count = 1
for i in final_data:
    names.append(i[0])
    scores.append(i[1])
    ranks.append(i[2])
    count+=1

fig = go.Figure(data=[go.Table(header=dict(values=['Profile', 'Score', 'Rank']),
                 cells=dict(values=[names, scores, ranks]))
                     ])
fig.show()



def write_csv(data_matrix, header, csv_output_name):
    with open(csv_output_name, mode='w') as csv_file:
        data_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data_writer.writerow(header)

        for i in range( len(data_matrix)):
            data_writer.writerow(data_matrix[i])

#write_csv(final_data, ["Profile Link", "Score", 'Rank'], 'contributors.csv')

project_writable = []
for i in project_data:
    result = []
    result.append(i[0]) #project link
    num_1 = i[2] / i[3]
    result.append(str(num_1)) #Top 10 Vs whole
    num_2 = i[1] / i[2]
    result.append(str(num_2)) #Top 1 Vs top 10
    project_writable.append(result)


print("")
print("")
#for i in project_writable:
    #print (i)
print("")
print("")

write_csv(project_writable, ["Project Link", "Top 10 vs Total", "Leader vs Top 10"], "projects.csv")

profiles = [] #Name, Username, email, website, followers,



def get_profiles(num_users):
    count = 0
    for i in final_data:
        global profiles

        link = i[0]
        print (link)
        profile_soup = BeautifulSoup(requests.get(link).text, 'html5lib')

        name = ""
        for faf in profile_soup.findAll('span', {'itemprop' : 'name'}):
            name = ' '.join(faf.findAll(text=True)).rstrip().lstrip().replace(",","")
            print(name)

        username = ""

        for faf in profile_soup.findAll('span', {'itemprop' : 'additionalName'}):
            username = ' '.join(faf.findAll(text=True)).rstrip().lstrip().replace(",","")

        does_email = ""
        does_website = ""

        for faf in profile_soup.findAll('li', {'itemprop' : 'email'}):

            does_email = faf.get('aria-label').replace("Email: ","")

        for faf in profile_soup.findAll('li', {'itemprop' : "url"}):
            for daf in faf.findAll('a'):
                does_website = daf.get('href')

        followers = ""


        rotation = 1 #When rotation is 5, it means we are at the follower tag
        for faf in profile_soup.findAll('a', {'class' : 'UnderlineNav-item mr-0 mr-md-1 mr-lg-3'}):
            if(rotation == 5):
                for daf in faf.findAll('span', {'class' : 'Counter hide-lg hide-md hide-sm'}):
                    followers = ' '.join(faf.findAll(text=True)).rstrip().lstrip().replace(",","")
            rotation += 1




        result = []
        if(name == ""):
            result.append("No Name Listed")
        else:
            result.append(name)


        result.append(username)

        if(does_email == ""):
            result.append("No Email Listed")
        else:
            result.append(does_email)

        if(does_website == ""):
            result.append("No website listed")
        else:
            result.append(does_website)

        result.append(followers)


        if(count >= num_users):
            break
        count+=1

        profiles.append(result)


        print(str(count) + "/" + str(num_users))


        time.sleep(5)




get_profiles(int(input("Input the number of users(starting from the top) to create profiles for")))

write_csv(profiles, ['Name', 'Username', 'Email', 'Website', 'Followers'], 'profiles.csv')

#for i in project_data:
    #print (i)

input()


