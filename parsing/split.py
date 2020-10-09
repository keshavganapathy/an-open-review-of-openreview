import csv

def append(filename, row):
	with open(filename, 'a+', newline='') as infile:
		csv_appender = csv.writer(infile)
		csv_appender.writerow(row)

with open('../authordata.csv', encoding='latin-1') as authorin, open('../openreview_v8_deletions.csv', encoding='latin-1') as reviewin:
	author_reader = csv.reader(authorin)
	review_reader = csv.reader(reviewin)

	cnt = 1
	for row_author in author_reader:
		row_review = next(review_reader)
		if cnt <= 1250:
			append('../Check_Authors/alex.csv', row_author[:2] + [row_review[3]] + row_author[2:])
		elif cnt <= 2500:
			append('../Check_Authors/raymond.csv', row_author[:2] + [row_review[3]] + row_author[2:])
		elif cnt <= 3750:
			append('../Check_Authors/keshav.csv', row_author[:2] + [row_review[3]] + row_author[2:])
		else:
			append('../Check_Authors/david.csv', row_author[:2] + [row_review[3]] + row_author[2:])
		cnt += 1
