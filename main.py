from igdb.wrapper import IGDBWrapper
import json
import pandas as pd
import ast
import time
from decouple import config

CLIENT_ID = config('CLIENT_ID')
AUTHORIZATION = config('AUTHORIZATION')
wrapper = IGDBWrapper(CLIENT_ID, AUTHORIZATION)

csv_columns = ['id', 'involved_companies', 'name', 'release_dates', 'websites']

current_time = 1683225945
# Current time as unix timestamp; appended to csv name

limit_value = 100
# Total entries per POST request (max is 500)

total_entries = 100
# total_entries should be divisible by limit value
# Indicates the total number of entries found overall by running the program once

alltime_entries = 0
# Can use as an offset if you don't want to start search from beginning of database

for i in range(alltime_entries, total_entries, limit_value):
    offset = i

    post_req = 'fields name,involved_companies.company.name,release_dates.human,websites.url; ' \
               'where involved_companies.publisher = true & platforms = 6 & release_dates.date > ' + str(current_time) + '; ' \
               'sort date asc; ' \
               'limit ' + str(limit_value) + '; ' \
               'offset ' + str(offset) + ';'
    # POST request for data on upcoming titles on PC including name, publisher, release date, website links

    byte_array = wrapper.api_request(
        'games',
        post_req
    )
    # Sends POST request to the games endpoint

    byte_array = bytearray(byte_array)
    req_dict = ast.literal_eval(byte_array.decode('utf8'))
    json_result = json.dumps(req_dict, indent=4, sort_keys=True)
    # Decodes byte array returned by API wrapper and converts to JSON

    dataframe = pd.read_json(json_result)
    # Converts JSON to dataframe

    print(len(dataframe))
    print(dataframe['websites'][0][1]['url'])

    for entry in range(len(dataframe)):
        company_list = []
        for company in dataframe['involved_companies'][entry]:
            company_list.append(company['company']['name'])
        dataframe['involved_companies'][entry] = company_list

        dates_list = []
        for date in dataframe['release_dates'][entry]:
            dates_list.append(date['human'])
        dataframe['release_dates'][entry] = dates_list

        website_list = []
        for website in dataframe['websites'][entry]:
            website_list.append(website['url'])
        dataframe['websites'][entry] = website_list

    csv_name = 'database' + str(time.time()) + '.csv'
    outfile = open(csv_name, 'wb')
    dataframe.to_csv(outfile, index=False, header=True, sep=',', encoding='utf-8')
    outfile.close()


