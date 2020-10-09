import csv
from datetime import date

def append(filename, row):
	with open(filename, 'a+', newline='') as infile:
		writer = csv.writer(infile)
		writer.writerow(row)

with open('paperdata_full_flat.csv') as paperin, open('authordata_reordered_flat.csv') as authorin, open('../openreview/openreview.csv') as reviewin, open('../paperlinks_full.csv') as linksin:
	paper_reader = csv.reader(paperin)
	author_reader = csv.reader(authorin)
	review_reader = csv.reader(reviewin)
	links_reader = csv.reader(linksin)
	header_paper = next(paper_reader)
	header_author = next(author_reader)
	header_review = next(review_reader)
	next(links_reader)

	append('dataset_final.csv', header_review + ['earliest_appearance_date'] + header_paper[2:] + header_author[1:])

	for row_review in review_reader:
		row_paper = next(paper_reader)
		row_author = next(author_reader)
		row_links = next(links_reader)	

		review_date = row_review[12].split('/')
		links_date = row_links[2].split('/')
		if len(links_date) != 3:
			min_date = row_review[12]
		else:
			dates = []
			dates.append(date(int('20' + review_date[2]), int(review_date[0]), int(review_date[1])))
			dates.append(date(int('20' + links_date[2]), int(links_date[0]), int(links_date[1])))
			min_index = dates.index(min(dates))
			if min_index == 0:
				min_date = row_review[12]
			else:
				min_date = row_links[2]
		append('dataset_final.csv', row_review + [min_date] + row_paper[2:] + row_author[1:]) 
