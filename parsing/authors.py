import csv
from sys import argv
import ast
from datetime import datetime
import editdistance

def net_dist(list1, list2):
	dist = 0
	for i in range(len(list1)):
		dist += editdistance.eval(list1[i].lower(), list2[i].lower())
	return dist

def append(filename, row):
	with open(filename, 'a+', newline='') as write_obj:
		csv_writer = csv.writer(write_obj)
		csv_writer.writerow(row)
def strip_percent(s):
	percents = []
	index = 0
	for c in s:
		if c == '%':
			percents.append(index)
		index += 1
	if len(percents) == 0:
		return s
	if len(percents) % 2 != 0:
		if len(percents) == 1:
			return s
		else:
			percents = percents[:-1]
	copy = ''
	if len(percents) % 2 != 0:
		raise Exception('percent parity error')
	
	for i in range(0, len(percents), 2):
		if i==0:	
			copy += s[:percents[i]]
		elif i == len(percents) - 1:	
			copy += s[percents[-1]:]
		elif i % 2 == 0:
			copy += s[percents[i-1]+1:percents[i]]
	return copy

def reorder(_list1, _list2):
	list1 = _list1.copy()
	list2 = _list2.copy()
	reorder = [None] * len(list2)
	champs = []
	list2_copy = list2.copy()
	for name1 in list1:
		min_dist = 100
		champ = None
		for i in range(len(list2)):
			if list2[i] == '-1':
				dist = 4
			else:
				dist = editdistance.eval(name1.lower(), list2[i].lower())
			if dist < min_dist:
				min_dist = dist
				champ = list2[i]
		champs.append(champ)
		list2.pop(list2.index(champ))
	for i in range(len(champs)):
		reorder[i] = list2_copy[list2_copy.index(champs[i])]
	return reorder

with open('../authordata_full.csv') as authorin, open ('../openreview/openreview.csv') as reviewin, open('../paperlinks_full.csv') as linksin:
	csv_reader_author = csv.reader(authorin)
	csv_reader_review = csv.reader(reviewin)
	csv_reader_links = csv.reader(linksin)
	next(csv_reader_author)
	next(csv_reader_review)
	next(csv_reader_links)
	line = 1 
	error = 0
	for row_author in csv_reader_author:
		row_links = next(csv_reader_links)
		row_review = next(csv_reader_review)
		authors_review = str(row_review[3]).split(';')
		authors_links = str(row_author[2]).strip('][').split(', ')
		diff = len(authors_review) - len(authors_links)
		
		if row_review[3] == 'Anonymous' or row_review[3] == 'withdrawn' or row_review[3] == 'withdrawn.' or row_review[3] == '':
			#if line <= 2500:
				#append('authordata_flat_check_alex.csv', [row_review[3], ['-1']] + [str({'Publications': '-1', 'h-index': '-1', 'Citations': '-1', 'Highly Influenced Papers': '-1'})])
			#else:
				#append('authordata_flat_check_david.csv', [row_review[3], ['-1']] + [str({'Publications': '-1', 'h-index': '-1', 'Citations': '-1', 'Highly Influenced Papers': '-1'})])
				
			line += 1
			#append('authordata_flat_check.csv', [row_review[3], ['-1']] + [str({'Publications': '-1', 'h-index': '-1', 'Citations': '-1', 'Highly Influenced Papers': '-1'})])
			continue
		extra = []
		if diff > 0:
			for i in range(diff):
				extra.append('-1')
		if len(authors_review) >= len(authors_links):
			names = []
			if authors_links[0] == "\'-1\'":
				authors_links[0] = '-1'
			for link in authors_links:
				name = link[40:]
				slash = name.find('/')
				name = name[:slash]
				try:
					name = strip_percent(name)
				except:
					print(name)
					exit(0)
				names.append(name)
			names_fixed1 = []
			for name in names:
				name_split = name.split('-')
				if len(name_split) > 1:
					names_fixed1.append(name_split[0][:min(4, len(name_split[0]))] + name_split[-1][:min(4, len(name_split[-1]))])
				else:
					names_fixed1.append(name)
			
			if authors_links[0] == '-1':
				names_fixed1 = ['-1']
			names_fixed1 += extra
			authors_links += extra
			names_fixed2 = []
			for name in authors_review:
				name_split = name.split(' ')
				if len(name_split) > 1:
					names_fixed2.append(name_split[0][:min(4, len(name_split[0]))] + name_split[-1][:min(4, len(name_split[-1]))])
				else:
					names_fixed2.append(name)

			reordered = reorder(names_fixed2, names_fixed1)
			reordered_dist = net_dist(names_fixed2, reordered)
			reordered_alpha = sorted(names_fixed1)
			names_fixed2_copy = sorted(names_fixed2.copy())

			reordered_alpha_dist = net_dist(names_fixed2_copy, reordered_alpha)
			if reordered_alpha_dist < reordered_dist:
				for i in range(len(reordered)):
					reordered[i] = reordered_alpha[names_fixed2_copy.index(names_fixed2[i])]
			dists = []
			for i in range(len(reordered)):
				if reordered[i] == '-1':
					dist = 0
				else:
					dist = editdistance.eval(names_fixed2[i].lower(), reordered[i].lower())
				dists.append(dist)
			
			links_reordered = []
			for i in range(len(names_fixed1)):
				links_reordered.append(authors_links[names_fixed1.index(reordered[i])])
			for i in range(len(links_reordered)):
				if links_reordered[i] != '-1':
					links_reordered[i] = links_reordered[i][1:-1]
			
			names_reordered = []
			for link in links_reordered:
				name = link[39:]
				slash = name.find('/')
				name = name[:slash]
				names_reordered.append(name)

			if max(dists) > 4:
				error += 1
				print('************************************************' + '\n')
				if line <= 2500:
					append('alex_check.csv', [line, row_review[3], links_reordered])
				else:
					append('david_check.csv', [line-2499, row_review[3], links_reordered])
				print(line)
				print(row_review[3])
				print(links_reordered)
			#else:
				#print('------------------------------------------------' + '\n')
		line += 1
		authors_data = []
		
		s = row_author[3]
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
		extra_stats = []
		for i in range(len(extra)):
			extra_stats.append(['-1', '-1', '-1', '-1']) 
			dicts.append({'Publications': '-1', 'h-index': '-1', 'Citations': '-1', 'Highly Influenced Papers': '-1'})

		stats += extra_stats

		stats_copy = stats.copy()
		for i in range(len(stats_copy)):
			stats_copy[i] = stats[names_fixed1.index(reordered[i])]
	
		stats = stats_copy.copy()

		dicts_copy = dicts.copy()
		for i in range(len(dicts_copy)):
			dicts_copy[i] = dicts[names_fixed1.index(reordered[i])]

		dicts = dicts_copy.copy()

		cits = ''
		pubs = ''
		h_inds = ''
		h_cits = ''

		for author in stats:
			if authors_links[0] == '-1':
				h_cits += '-1;'
			else:
				h_cits += author[3] + ';'
				
			cits += author[0] + ';'		
			pubs += author[1] + ';'
			h_inds += author[2] + ';'
		cits = cits[:-1]
		pubs = pubs[:-1]
		h_inds = h_inds[:-1]
		h_cits = h_cits[:-1]
		#author_stats = [cits, pubs, h_inds, h_cits]
		
		#print(line)
		#print(row_review[3])
		#print(links_reordered)
		#print(author_stats)
		#print()
		

		#if line <= 2500:
			#append('authordata_flat_check_alex.csv', [row_review[3]] + [str(links_reordered)] + [str(dicts)])
		#else:
			#append('authordata_flat_check_david.csv', [row_review[3]] + [str(links_reordered)] + [str(dicts)])
			
		#append('authordata_flat_check.csv',[row_review[3]] + [str(links_reordered)] + [str(dicts)])
print(error)
