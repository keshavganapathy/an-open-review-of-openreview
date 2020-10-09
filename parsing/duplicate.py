from sys import argv
import csv
import ast
import editdistance

year = str(argv[1])

with open('../authordata' + year + '.csv') as infile:
	csv_reader = csv.reader(infile)
	
	cnt = 1 
	for row in csv_reader:
		author_dicts = []

		s = row[2]
		tail = s.find('{')
		head = s.find('}')
		while tail != -1:
			dict = ast.literal_eval(s[tail:head+1])		
			s = s[head+1:]
			author_dicts.append(dict)
			tail = s.find('{')
			head = s.find('}')

		links = row[1].strip('][').split(', ')
		names = []
		for link in links:
			l = link.find('author')
			l += 7
			r = link[l:].find('/')
			r += l
			name = link[l:r]
			names.append(name)

		for i in range(len(names)):
			name_1 = names[i]
			
			for j in range(i+1, len(names)):
				name_2 = names[j]
				dist = editdistance.eval(name_1.lower().replace('-', ''), name_2.lower().replace('-', ''))
				if dist < 6:
					print(str(cnt) + ': ', name_1 + ',', name_2)

		cnt += 1
