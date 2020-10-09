import csv

def append(filename, row):
	with open(filename, 'a+', newline = '') as infile:
		csv_writer = csv.writer(infile)
		csv_writer.writerow(row)

with open('../dataset_final.csv') as finalin, open('../dataset_gender.csv') as genderin:
	final_reader = csv.reader(finalin)
	gender_reader = csv.reader(genderin)

	authors = []
	stats = []
	for row in gender_reader:
		authors.append(row[0])
		stats.append(row[1])

	cnt = 0

	for row in final_reader:
		if row[3] in authors:
			cnt +=1
			append('dataset_final_v2.csv', row + [stats[authors.index(row[3])]])
		else:
			if len(row[3].split(';')) == 1:
				append('dataset_final_v2.csv', row + ['-1'])			
			else:
				append('dataset_final_v2.csv', row + ['-1;-1'])

print(cnt)
