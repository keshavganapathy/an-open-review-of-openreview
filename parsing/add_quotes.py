import csv
import ast

def append(filename, row):
	with open(filename, 'a+', newline='') as write_obj:
		csv_writer = csv.writer(write_obj)
		csv_writer.writerow(row)

def find_int(s):
	x = -1
	y = -1
	for i in range(len(s)):
		if s[i].isdigit():
			x = i
			digit = s[i]
			j = i
			while digit.isdigit():
				j += 1
				digit = s[j]
			y = j-1
			break

	return x, y

def quote(s, x, y):
	a = s[:x] + "'"
	b = s[x:y] + "'"
	c = s[y:]
	return a + b + c

def insert_quotes(s):
	c = s[0]
	x = []
	y = []
	inNum = False
	for i in range(len(s)):
		if s[i].isdigit() or (s[i] == ',' and s[i+1].isdigit()):
			if not inNum:
				x.append(i)
			inNum = True
		else:
			if inNum:
				y.append(i)
				inNum = False
	for i in range(len(x)):
		s = quote(s, x[i] + (2*i), y[i] + (2*i))
	return s

with open('../paperdata_full.csv') as infile:
	csv_reader = csv.reader(infile)
	next(csv_reader)
	line = 2
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
		highly_influenced_papers = 0
		twitter_mentions = 0
		
		row_new = row
		for stat in stats:
			dict_stat = stat						   
			try:										
				citations += int(dict_stat['Citations'].replace(',', ''))
			except Exception as e:
				row_new[3] = insert_quotes(row[3])
				break
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
				twitter_mentions += int(dict_stat['Twitter Mentions']).replace(',', '')
			except:
				twitter_mentions += 0
			try:
				highly_influenced_papers += int(dict_stat['Highly Influenced Papers'].replace(',', ''))
			except:
				highly_influenced_papers += 0
		append('paperdata_full_quoted.csv', row_new)
		#append('paperdata_full_flat.csv',[row[0], row[1]] + [citations, cite_background, cite_methods, twitter_mentions, highly_influenced_papers])

