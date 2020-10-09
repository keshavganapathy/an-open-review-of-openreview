import csv

def append(filename, row):
	with open(filename, 'a+', newline='') as write_obj:
		csv_writer = csv.writer(write_obj)
		csv_writer.writerow(row)

with open('dataset.csv') as infile:
	csv_reader = csv.reader(infile)
	for row in csv_reader:
		index = row[16].find(' ')
		row_new = row
		row_new[16] = row[16][:index]
		append('dataset_clean.csv', row_new)
	
