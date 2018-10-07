import json
import re

import numpy as np

final_data = {}
final = {}
count = 0

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

            final[count] = final_data
            count = count + 1

# np.savetxt('firstdata.csv', ("id", "title", "date", "news_detail"), delimiter=',')
with open('finaljsondata.txt', 'w') as outfile:  
    json.dump(final, outfile)

print (final)

