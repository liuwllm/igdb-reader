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
# Total entries per json request (max is 500)

total_entries = 500
# total_entries should be divisible by limit value

alltime_entries = 0
# Can use as an offset if you don't want to start search from beginning of database

for i in range(alltime_entries, total_entries, limit_value):
    offset = i

    post_req = 'fields name,involved_companies.company.name,release_dates.human,websites.url; ' \
               'where involved_companies.publisher = true & platforms = 6 & release_dates.date > ' + str(current_time) + '; ' \
               'sort date asc; ' \
               'limit ' + str(limit_value) + '; ' \
               'offset ' + str(offset) + ';'

    byte_array = wrapper.api_request(
        'games',
        post_req
    )

    byte_array = bytearray(byte_array)
    req_dict = ast.literal_eval(byte_array.decode('utf8'))
    json_result = json.dumps(req_dict, indent=4, sort_keys=True)

    dataframe = pd.read_json(json_result)

    print(dataframe)

    csv_name = 'database' + str(time.time()) + '.csv'
    outfile = open(csv_name, 'wb')
    dataframe.to_csv(outfile, index = False, header = True, sep = ',', encoding = 'utf-8')
    outfile.close()

