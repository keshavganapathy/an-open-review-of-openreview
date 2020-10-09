import csv

with open('dataset_clean.csv') as infile:
	csv_reader = csv.reader(infile)
	
	decisions = []
	for row in csv_reader:
		decision = row[7]
		if decision not in decisions:
			decisions.append(decision)

print(decisions)
