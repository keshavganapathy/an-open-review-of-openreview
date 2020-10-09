import csv
import editdistance

def append(filename, row):
	with open(filename, 'a+', newline='') as infile:
		writer = csv.writer(infile)
		writer.writerow(row)

with open('../authordata_combined.csv') as authorin, open('../openreview/openreview.csv') as reviewin:
	author_reader = csv.reader(authorin)
	review_reader = csv.reader(reviewin)

	next(review_reader)
	header = next(author_reader)
	append('authordata_full.csv', header)

	for row in author_reader:
		row_review = next(review_reader)
		while editdistance.eval(row[1].lower(), row_review[2].lower()) > 5:
			filler = [row_review[1], row_review[2], ['-1'], [{'Publications': '-1', 'Citations': '-1', 'h-index': '-1', 'Highly Influenced Papers': '-1'}]]
			append('authordata_full.csv', filler)
			row_review = next(review_reader)
		row_new = row
		if row[2] == '[]':
			row_new[2] = ['-1']
			row_new[3] = [{'Publications': '-1', 'Citations': '-1', 'h-index': '-1', 'Highly Influenced Papers': '-1'}]
		append('authordata_full.csv', row_new)

with open('../paperdata_combined.csv') as paperin, open('../openreview/openreview.csv') as reviewin:
	paper_reader = csv.reader(paperin)
	review_reader = csv.reader(reviewin)

	next(review_reader)
	header = next(paper_reader)
	append('paperdata_full.csv', header)

	for row in paper_reader:
		row_review = next(review_reader)
		while editdistance.eval(row[1].lower(), row_review[2].lower()) > 5:
			filler = [row_review[1], row_review[2], ['-1'], [{'Citations': '-1', 'Highly Influenced Papers': '-1', 'Cite Background': '-1', 'Cite Methods': '-1', 'Cite Results': '-1', 'Twitter Mentions': '-1'}]]
			append('paperdata_full.csv', filler)
			row_review = next(review_reader)
		append('paperdata_full.csv', row)

with open('../paperlinks_combined.csv') as linksin, open('../openreview/openreview.csv') as reviewin:
	links_reader = csv.reader(linksin)
	review_reader = csv.reader(reviewin)

	next(review_reader)
	header = next(links_reader)
	append('paperlinks_full.csv', header)

	for row in links_reader:
		row_review = next(review_reader)
		while editdistance.eval(row[1].lower(), row_review[2].lower()) > 5:
			filler = [row_review[1], row_review[2], '', ['-1'], ['-1']]
			append('paperlinks_full.csv', filler)
			row_review = next(review_reader)
		append('paperlinks_full.csv', row)
