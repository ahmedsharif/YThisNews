import json
import re
import csv

import numpy as np

final_data = {}
final = {}
count = 0
outputFile = open('fileoutput3.csv', 'w')  
output = csv.writer(outputFile) #create a csv.write


with open('finalfull1.json') as json_data:
    all_news = json.load(json_data)
    for page in all_news:
        # parse_individual_news = all_news[page]['news']

        for news in page['news']:
            print("****",page['news'][news])
            final_data = {}
            data = page['news'][news]
            final_data['id'] = news
            final_data['title'] = data['title']
            final_data['date'] = data['date']
            new_list = [word.replace('\xa0','') for word in data['news_detail']]
            final_data['news_detail'] = new_list

            output.writerow(final_data.values())
            # final[count] = [final_data['id'], final_data['title'], final_data['date'], final_data['news_detail']], "|"
            
            count = count + 1

# np.savetxt('firstdata.csv', ("id", "title", "date", "news_detail"), delimiter=',')
# with open('myfinaldata2.txt', 'w') as outfile:  
#     json.dump(final, outfile)

# with open('newsCSV.csv', 'w') as myFile:  
#     writer = csv.writer(myFile)
#     writer.writerows(final_data)



print (final)

