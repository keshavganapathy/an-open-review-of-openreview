import csv
import time
from bs4 import BeautifulSoup
import requests

year = "2019"

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
    links = open('papers' + year + '_links.csv', 'r')
    links_new = open('papers' + year + '_links_new.csv', 'r')
    authordata = open('authordata' + year + '.csv', 'r')
    try:
        authordata_new = open('authordata' + year + '_new.csv', 'r')
        link_csv_reader = csv.reader(links)
        link_csv_reader_new = csv.reader(links_new)
        author_csv_reader = csv.reader(authordata)
        author_csv_reader_new = csv.reader(authordata_new)
        for line in author_csv_reader_new:
            row = next(link_csv_reader)
            row_new = next(link_csv_reader_new)
        authordata_new.close()
    except:
        link_csv_reader = csv.reader(links)
        link_csv_reader_new = csv.reader(links_new)
        author_csv_reader = csv.reader(authordata)
    authordata_new = open('authordata' + year + '_new.csv', 'a+')
    row = next(link_csv_reader)
    row_new = next(link_csv_reader_new)
    row_author = next(author_csv_reader)
    while row is not None:

        # Check if old and new links are identical
        if set(row[3]) == set(row_new[3]):
            append('authordata' + year + '_new.csv', row_author)
            row = next(link_csv_reader)
            row_new = next(link_csv_reader_new)
            row_author = next(author_csv_reader)
            continue

        key_value_pairs = []

        author_urls = row_new[3].strip('][').split(', ')
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
                time.sleep(30)
                counter += 1

            except Exception as e:
                # Failed to scrape

                print(e)
                print('The above exception occured. Retrying in 5 minutes...')
                time.sleep(300)
                continue

        append('authordata' + year + '_new.csv', [row[0], row[3], key_value_pairs])
        print("Successfully appended row")

        row = next(link_csv_reader)
        row_new = next(link_csv_reader_new)
        row_author = next(author_csv_reader)

    links.close()
    links_new.close()
    authordata.close()

main()
