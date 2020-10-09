import csv
from sys import argv
import editdistance

with open('../withdrawn_semanticscholar/withdrawn_paperdata.csv') as infile:
    csv_reader = csv.reader(infile)
    cnt = 0
    for row in csv_reader:
        cnt += 1

        title = row[1]
        links = row[2].strip('][').split(', ')
        title = title.replace('-', ' ')
        title_words = title.split(' ')
        cutoff = min(5, len(title_words))
        title_words = title_words[:cutoff]
        title_dash = ''
        for word in title_words:
            title_dash += word + '-'
        title_dash = title_dash[:-1].lower()
        for link in links:
            link_title = link[39:39 + len(title_dash)].lower()
            dist = editdistance.eval(title_dash, link_title)
            if dist > 5:
                print(cnt, ':', title, ':', link[39:])
