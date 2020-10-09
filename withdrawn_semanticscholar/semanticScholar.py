import csv
import time
import editdistance
from sys import argv
from itertools import permutations
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located, text_to_be_present_in_element

year = str(argv[1])

# searches and parses for the links associated with a paper title
def search(query):
    title_query = query.replace("\n", "")
    # build search URL from paper title
    url = "http://semanticscholar.org/search?q="
    query = query.replace(",", "").replace("?", "").replace("!", "").replace("\n", "").replace("---", "-")
    url += query.replace(" ", "%20")
    url += "&sort=relevance"

    # instantiate a Chrome driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver = webdriver.Chrome("/Users/david/Desktop/reu-summer-2020/github/withdrawn_semanticscholar/chromedriver", options=chrome_options)

    # wait for at most 15 seconds for anything to load
    wait = WebDriverWait(driver, 15)

    # request for the result page of the search; find all results
    print('Request sent for:\n' + url)
    driver.get(url)
    wait.until(presence_of_element_located((By.CLASS_NAME, 'result-page')))
    results = driver.find_elements(By.CLASS_NAME, 'search-result')

    # check if the servers are busy before scraping
    isError = True
    try:
        driver.find_element(By.CLASS_NAME, 'error-message')
    except:
        isError = False
    if isError:
        raise Exception('Servers are busy!')

    # dismiss the copyright banner if it is on the page
    try:
        banner = driver.find_element(By.CLASS_NAME, 'copyright-banner__dismiss-btn')
        banner.click()
    except:
        banner = None

    # get the paper link for the first result
    champ_result = None
    min_dist = 10000
    for result in results:
        title_candidate = result.find_element(By.CLASS_NAME, 'search-result-title').text.lower()
        dist = editdistance.eval(title_query.lower(), title_candidate)
        if dist < min_dist:
            min_dist = dist
            champ_result = result

    title_webelement_first = champ_result.find_element(By.CLASS_NAME, 'search-result-title')
    title_link_first = title_webelement_first.find_element(By.TAG_NAME, 'a').get_attribute('href')
    title_first = title_webelement_first.text.lower()
    
    # get the full abstract for the first result
    clickable = True
    try:
        more_abstract_first = champ_result.find_element(By.CLASS_NAME, 'mod-clickable')
        more_abstract_first.click()
        wait.until(presence_of_element_located((By.CLASS_NAME, 'full-abstract')))
        abstract_first = champ_result.find_element(By.CLASS_NAME, 'full-abstract').text.lower()
    except:
        clickable = False
        abstract_first = ""


    # expand the first author list if applicable
    try:
        more_authors_first = champ_result.find_element(By.CLASS_NAME, 'more-authors-label')
        more_authors_first.click()
    except:
        more_authors_first = None

    # get the authors for the first result
    authors_first = champ_result.find_element(By.CLASS_NAME, 'author-list').text.lower()

    # close the abstract of the first result if applicable
    if clickable:
        more_abstract_first.click()

    paper_dates = []
    paper_titles = []
    paper_authors = set()

    warnings = 0
    for result in results:
        author_links = []
        
        # get the paper link for the result
        title_webelement = result.find_element(By.CLASS_NAME, 'search-result-title')
        title_link = title_webelement.find_element(By.TAG_NAME, 'a').get_attribute('href')
        title = title_webelement.text.lower()

        # expand the author list if applicable
        try:
            more_authors = result.find_element(By.CLASS_NAME, 'more-authors-label')
            if not (result == champ_result):
                more_authors.click()
        except:
            more_authors = None

        # get the author list if it exists
        try:
            authors = result.find_element(By.CLASS_NAME, 'author-list')
            authors = authors.text.lower()
        except:
            authors = ""

        # get the author links
        author_list = result.find_elements(By.CLASS_NAME, 'author-list__link')
        for link in author_list:
            try:
                author_links.append(link.get_attribute('href'))
            except:
                continue
        
        date = None
        # get the first publication date of the result if it exists
        try:
            items = result.find_elements(By.CLASS_NAME, 'paper-meta-item')
            for item in items:
                text = item.text
                if text.find('First Publication:') != -1:
                    date = text[6:].replace('First Publication: ', '').replace(')', '')
        except:
            date = None

        # expand and get the abstract if it exists
        try:
            more_abstract = result.find_element(By.CLASS_NAME, 'mod-clickable')
            more_abstract.click()
            wait.until(presence_of_element_located((By.CLASS_NAME, 'full-abstract')))
            abstract = result.find_element(By.CLASS_NAME, 'full-abstract')
            abstract = abstract.text.lower()
        except:
            abstract = ""
        
        # update paper data if the paper is the same
        bools = isVersion(title_first, authors_first, abstract_first, title, authors, abstract)
        isSame = bools[0]
        isWarning = bools[1]
        warnings += int(isWarning)
        if isSame:
            paper_titles.append(title_link)
            paper_authors.update(author_links)
            if date is not None:
                paper_dates.append(date)

        isFirst = False

    driver.close()

    
    # package the data and return it
    min_date = minDate(paper_dates)
    data = []
    data.append(min_date)
    data.append(paper_titles)
    data.append(list(paper_authors))
    if warnings > 0:
        append('papers' + year + '_links_warnings.csv', [title_query] + data)
    return data

# use the Levenschtein edit distance to determine if two papers are the same from their authors and abstracts
def isVersion(title1, authors1, abstract1, title2, authors2, abstract2):
    authors1_strip = authors1.replace(',', '').replace(' ', '')
    authors2_split = authors2.replace(' ', '').split(',')
    if len(authors2_split) < 8:
        authors_permutations = list(permutations(authors2_split))
        author_dists = []
        for perm in authors_permutations:
            author_dists.append(editdistance.eval(''.join(perm), authors1_strip))

        authors_dist = (min(author_dists) < 10)
    else:
        authors_dist = (editdistance.eval(authors1, authors2) < 10)
    
    abstract_dist = (editdistance.eval(abstract1, abstract2) < 200)

    title_dist = (editdistance.eval(title1, title2) < 10)
    
    tot = int(authors_dist) + int(abstract_dist) + int(title_dist)

    if authors_dist and abstract_dist and title_dist:
        return [True, False]
    elif tot == 2:
        return [True, True]
    else:
        return [False, False]

# find the min of a list of dates of the form "day month year"
def minDate(dates):
    months = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}
    min_year = 10000
    min_month = 100
    min_day = 100
    min_date = ""

    for date in dates:
        date_split = date.split(' ')
        day = int(date_split[0])
        month = int(months.get(date_split[1]))
        year = int(date_split[2])
        if int(year) < int(min_year):
            min_year = date_split[2]
            min_month = months.get(date_split[1])
            min_day = date_split[0]
            min_date = date
        elif int(year) > int(min_year):
            continue
        elif int(month) < int(min_month):
            min_year = date_split[2]
            min_month = months.get(date_split[1])
            min_day = date_split[0]
            min_date = date
        elif int(month) > int(min_month):
            continue
        elif int(day) < int(min_day):
            min_year = date_split[2]
            min_month = months.get(date_split[1])
            min_day = date_split[0]
            min_date = date
    
    return min_date

# add a row to a given csv file
def append(filename, row):
    with open(filename, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(row)

# search each paper title and add the parsed information to a csv file
def main():
    with open('../withdrawn_' + year + '.txt', 'r') as infile:
        try:
            f = open('withdrawn_' + year + '_links.csv')
            csv_reader = csv.reader(f)

            line = infile.readline()
            for row in csv_reader:
                line = infile.readline()
            
            f.close()
        except:
            line = infile.readline()

        while line is not None:
            title = str(line).replace('\n', '')
            try:
                data = search(line)
            except Exception as e:
                print(e)
                print('The above exception occured. Retrying in 5 minutes...')
                time.sleep(300)
                continue
            if len(data[1]) == 0:
                print('Scrape unsuccessful. Retrying in 60 seconds...')
                time.sleep(60)
                continue

            append('withdrawn_' + year + '_links.csv', [title] + data)
            line = infile.readline()
            print('Links scraped! Waiting 40 seconds...')
            time.sleep(40)

    
if __name__ == "__main__":
    main()
