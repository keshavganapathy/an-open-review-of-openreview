import csv
import time
from bs4 import BeautifulSoup
import requests
from sys import argv

year = str(argv[1])

def search(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    # Check if page displays correctly (i.e. not blocked)

    author_card = soup.find_all("div", class_="author-detail-card")
    if author_card is None:
        return None

    # Retrieve author stats

    stats = {}
    results = soup.find_all("div", class_="author-detail-card__stats-row")

    for result in results:
        label = result.find(class_="author-detail-card__stats-row__label").text
        value = result.find(class_="author-detail-card__stats-row__value").text
        stats[label] = value
    return stats

def append(filename, row):
    with open(filename, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(row)

def main():
    links = open('withdrawn_' + year + '_links.csv', 'r')
    try:
        authordata = open('withdrawn_authordata' + year + '.csv', 'r')
        link_csv_reader = csv.reader(links)
        author_csv_reader = csv.reader(authordata)
        for line in author_csv_reader:
            row = next(link_csv_reader)
        authordata.close()
    except:
        link_csv_reader = csv.reader(links)
    row = next(link_csv_reader)
    authordata = open('withdrawn_authordata' + year + '.csv', 'a+')
    while row is not None:

        key_value_pairs = []

        author_urls = row[3].strip('][').split(', ')
        l = len(author_urls)
        counter = 1

        print('Request sent for:\n' + row[0])

        for author_url in author_urls:
            try:
                author_dict = search(author_url[1:-1])
                
                # Check if blocked
                if author_dict is None:
                    print("The request was blocked. Retrying in 10 minutes...")
                    time.sleep(600)
                    continue

                key_value_pairs.append(author_dict)
                print("Successfully scraped author {} of {}".format(counter, l))
                time.sleep(40)
                counter += 1

            except Exception as e:
                # Failed to scrape

                print(e)
                print('The above exception occured. Retrying in 5 minutes...')
                time.sleep(300)
                continue

        append('withdrawn_authordata' + year + '.csv', [row[0], row[3], key_value_pairs])
        print("Successfully appended row")

        row = next(link_csv_reader)

    links.close()
    authordata.close()

main()
