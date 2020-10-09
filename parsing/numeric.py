import csv

def append(filename, row):
	with open(filename, 'a+', newline='') as write_obj:
		csv_writer = csv.writer(write_obj)
		csv_writer.writerow(row)

with open('dataset_clean.csv') as infile:
	csv_reader = csv.reader(infile)
	
	next(csv_reader)
	for row in csv_reader:
		decision = row[7]
		if decision == 'Reject':
			numeric_decision = -1
		elif decision == 'Invite to Workshop Track':
			numeric_decision = 0
		elif decision == 'Accept (Poster)':
			numeric_decision = 1
		elif decision == 'Accept (Oral)' or decision == 'Accept (Talk)':
			numeric_decision = 2
		elif decision == 'Accept (Spotlight)':
			numeric_decision = 3
		else:
	 		raise Exception('invalid decision')
		blind = row[11]
		if blind == 'no':
			blind_numeric = 0
		elif blind == 'yes':
			blind_numeric = 1
		else:
			raise Exception('invalid blind')

		row_new = [row[1], row[2]] + [row[5], row[6], numeric_decision] + [row[8], row[9], row[10], blind_numeric] + [row[13], row[14], row[16]] + row[17:]
		append('dataset_numeric.csv', row_new)
