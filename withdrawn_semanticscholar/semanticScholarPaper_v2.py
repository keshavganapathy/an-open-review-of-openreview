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

    main_content = soup.find_all("div", class_="main_content")
    if main_content is None:
        return None

    stats = {}

    # Total citations

    #citations = soup.find(class_='scorecard_stat__headline')
    citations = soup.findAll("a", {"data-heap-nav" : "citing-papers"})

    if not citations:
        
        # No scorecard

        stats['Citations'] = 0
    else:
        citations = citations[0].text.split()
        stats['Citations'] = int(citations[0])
    """
    # Semantic Scholar's other citation stats
    
    other_citation_stats = soup.find_all("div", class_="scorecard__description-line")
    for citation_stat in other_citation_stats:
        try:
            split_text = citation_stat.text.split()
            label = " ".join(split_text[1:])
            value = int(split_text[0])
            stats[label] = value
        except:
            pass

    # In case Twitter mentions are counted

    try:
        twitter_mentions = int(soup.find(class_="scorecard__stat__v2 scorecard__tweet").text.replace('Twitter Mentions',''))
        stats['Twitter Mentions'] = twitter_mentions
    except:
        pass
    """
    return stats

def append(filename, row):
    with open(filename, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(row)

def main():
    links_new = open('withdrawn_' + year + '_links.csv', 'r')
    try:
        paperdata = open('withdrawn_paperdata' + year + '.csv', 'r')
        link_csv_reader_new = csv.reader(links_new)
        paper_csv_reader = csv.reader(paperdata)
        for line in paper_csv_reader:
            row_new = next(link_csv_reader_new)
        paperdata.close()
    except:
        link_csv_reader_new = csv.reader(links_new)
    row_new = next(link_csv_reader_new)
    while row_new is not None:
        key_value_pairs = []

        paper_urls = row_new[2].strip('][').split(', ')
        l = len(paper_urls)
        counter = 1
        
        print('Request sent for:\n' + row_new[0])

        for paper_url in paper_urls:
            try:
                paper_dict = search(paper_url[1:-1])

                # Check if blocked
                if paper_dict is None:
                    print("The request was blocked. Retrying in 10 minutes...")
                    time.sleep(600)
                    continue

                key_value_pairs.append(paper_dict)
                print("Successfully scraped paper {} of {}".format(counter, l))
                time.sleep(40)
                counter += 1

            except Exception as e:
                # Failed to scrape

                print(e)
                print('The above exception occured. Retrying in 5 minutes...')
                time.sleep(300)
                continue

        append('withdrawn_paperdata' + year + '.csv', [row_new[0], row_new[2], key_value_pairs])
        print("Successfully appended row")

        row_new = next(link_csv_reader_new)

   
    links_new.close()
    paperdata.close()
main()
