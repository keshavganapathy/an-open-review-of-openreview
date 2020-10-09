import csv


months = {'January': '1', 'February': '2', 'March': '3', 'April': '4', 'May': '5', 'June': '6', 'July': '7', 'August': '8', 'September': '9', 'October': '10', 'November': '11', 'December': '12'}

months_short = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6', 'Jul': '7', 'Aug': '8', 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

def append(filename, row):
	with open(filename, 'a+', newline='') as infile:
		writer = csv.writer(infile)
		writer.writerow(row)

with open('../paperlinks.csv') as infile:
	reader = csv.reader(infile)
	header = next(reader)
	append('../paperlinks_dates.csv', header)
	for row in reader:
		row_new = row
		date = row[2]
		if date == '':
			append('../paperlinks_dates.csv', row)
			continue
		date_split = date.split('-')
		date_new = months_short.get(date_split[1]) + '/' + date_split[0] + '/' + date_split[2]
		row_new[2] = date_new
		append('../paperlinks_dates.csv', row)
