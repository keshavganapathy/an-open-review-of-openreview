import csv

with open('../paperlinks.csv') as infile:
    csv_reader = csv.reader(infile)
    cnt = 1
    for row in csv_reader:
        if len(row[2]) < 6:
            print(str(row[1]), cnt)
        cnt += 1