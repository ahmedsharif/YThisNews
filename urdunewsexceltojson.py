import csv

with open('TransliteratedSentenceSaperateFileCSV.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("row",row)
            line_count += 1
        line_count += 1
    print(f'Processed {line_count} lines.')