import csv
import ast

def append(filename, row):
	with open(filename, 'a+', newline='') as write_obj:
		csv_writer = csv.writer(write_obj)
		csv_writer.writerow(row)


with open('authordata_reordered.csv') as infile:
	author_reader = csv.reader(infile)

	header = next(author_reader)
	line = 2
	for row_author in author_reader:
		print(line)
		authors_data = []

		s = row_author[2]
		tail = s.find('{')
		head = s.find('}')
		while tail != -1:
			authors_data.append(ast.literal_eval('"' + s[tail:head+1] + '"'))
			s = s[head+1:]
			tail = s.find('{')
			head = s.find('}')
		
		stats = []
		dicts = []
		for j in range(len(authors_data)):
			citations = 0
			publications = 0
			h_index = 0
			highly_influential_citations = 0
			dict = ast.literal_eval(authors_data[j])
			dicts.append(dict)
			try:
				citations = int(dict['Citations'].replace(',', ''))
			except:
				citations = 0
			try:
				publications = int(dict['Publications'].replace(',', ''))
			except:
				publications = 0
			try:
				h_index = int(dict['h-index'].replace(',', ''))
			except:
				h_index = 0
			try:
				highly_influential_citations = int(dict['Highly Influential Citations'].replace(',', ''))
			except:
				highly_influential_citations = 0
			
			author_data = [str(citations), str(publications), str(h_index), str(highly_influential_citations)]
			stats.append(author_data)

			cits = ''
			pubs = ''
			h_inds = ''
			h_cits = ''
	
			for author in stats:
				h_cits += author[3] + ';'
				cits += author[0] + ';'		
				pubs += author[1] + ';'
				h_inds += author[2] + ';'
			cits = cits[:-1]
			pubs = pubs[:-1]
			h_inds = h_inds[:-1]
			h_cits = h_cits[:-1]

		append('authordata_reordered_flat.csv', [row_author[1]] + [cits, pubs, h_inds, h_cits])

		line += 1
