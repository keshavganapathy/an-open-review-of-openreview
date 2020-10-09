import csv
import ast

def append(filename, row):
	with open(filename, 'a+', newline='') as infile:
		csv_writer = csv.writer(infile)
		csv_writer.writerow(row)
def getDicts(s):
	dicts = []

	tail = s.find('{')
	head = s.find('}')
	while tail != -1:
		dicts.append(ast.literal_eval('"' + s[tail:head+1] + '"'))
		s = s[head+1:]
		tail = s.find('{')
		head = s.find('}')

	return dicts

with open('../withdrawn_semanticscholar/withdrawn_paperdata.csv', encoding='latin-1') as paperin, open('../withdrawn_semanticscholar/david_check/withdrawn_authordata_david.csv', encoding='latin-1') as authorin, open('../withdrawn_semanticscholar/david_check/withdrawn_openreview_david.csv', encoding='latin-1') as reviewin:
	paper_reader = csv.reader(paperin)
	author_reader = csv.reader(authorin)
	review_reader = csv.reader(reviewin)

	cnt = 2
	next(paper_reader)
	for row in paper_reader:
		links = row[2].strip('][').split(', ')
		dicts = getDicts(row[3])
		if len(links) != len(dicts):
			print(cnt)
		cnt += 1

	cnt = 2
	cnt_review = 2

	next(author_reader)
	next(review_reader)
	for row_author in author_reader:
		row_review = next(review_reader)
		while row_author[1] != row_review[1]:
			row_review = next(review_reader)
			cnt_review += 1
		review_authors = row_review[2].split(';')
		links_authors = row_author[2].strip('][').split(', ')
		if len(review_authors) != len(links_authors):
			data = []
			data.append(cnt_review)
			data.append(review_authors)
			data.append(cnt)
			data.append(links_authors)
			append('../withdrawn_semanticscholar/david_check/david.csv', data)
			print(cnt)
			print(review_authors)
			print(links_authors)
			print()
		cnt += 1
		cnt_review += 1
