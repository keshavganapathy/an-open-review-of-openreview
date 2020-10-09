import csv
import ast

def append(filename, row):
	with open(filename, 'a+', newline='') as write_obj:
		csv_writer = csv.writer(write_obj)
		csv_writer.writerow(row)


with open('paperdata_full_quoted.csv') as infile:
	csv_reader = csv.reader(infile)
	next(csv_reader)
	append('paperdata_full_flat.csv', ['year', 'title', 'citations', 'cite_background', 'cite_methods', 'cite_results', 'twitter_mentions', 'highly_influenced_papers'])
	for row in csv_reader:
		stats = []
		s = row[3]
		tail = s.find('{')
		head = s.find('}')
		while tail != -1:
			stats.append(ast.literal_eval(s[tail:head+1]))
			s = s[head+1:]
			tail = s.find('{')
			head = s.find('}')
				
		citations = 0
		cite_background = 0
		cite_methods = 0
		cite_results = 0
		twitter_mentions = 0
		highly_influenced_papers = 0
		for stat in stats:
			dict_stat = stat
			try:
				citations += int(dict_stat['Citations'].replace(',', ''))
			except:
				citations += 0
			try:
				cite_background += int(dict_stat['Cite Background'].replace(',', ''))
			except:
				cite_background += 0
			try:
				cite_methods += int(dict_stat['Cite Methods'].replace(',', ''))
			except:
				cite_methods += 0
			try:
				cite_results += int(dict_stat['Cite Results'].replace(',', ''))
			except:
				cite_results += 0
			try:
				twitter_mentions += int(dict_stat['Twitter Mentions'].replace(',', ''))
			except:
				twitter_mentions += 0
			try:
				highly_influenced_papers += int(dict_stat['Highly Influenced Papers'].replace(',', ''))
			except:
				highly_influenced_papers += 0
	
		append('paperdata_full_flat.csv', [row[0], row[1], citations, cite_background, cite_methods, cite_results, twitter_mentions, highly_influenced_papers])

