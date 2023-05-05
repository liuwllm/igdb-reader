from igdb.wrapper import IGDBWrapper
from decouple import config
import pandas as pd
import json
import ast
import time

# API authentication configuration
CLIENT_ID = config('CLIENT_ID')
AUTHORIZATION = config('AUTHORIZATION')
wrapper = IGDBWrapper(CLIENT_ID, AUTHORIZATION)

# Current time as unix timestamp; appended to csv name
current_time = 1683225945

# Total entries per POST request (max is 500)
limit_value = 500

# total_entries should be divisible by limit value
# Indicates the total number of entries found overall by running the program once
total_entries = 1000

# Can use as an offset if you don't want to start search from beginning of database
alltime_entries = 0

# List to hold all dataframes to be combined later on
dataframe_list = []

# Checks to see if you want the games outputted to have release dates or have a release date of TBD
# True = release dates, False = TBD
want_release_date = False
if want_release_date:
    release_date = 'release_dates.date > ' + str(current_time) + '; '
else:
    release_date = 'release_dates.category = 7; '

# Sends multiple POST requests using the previously defined parameters
for offset in range(alltime_entries, total_entries, limit_value):

    # POST request for data on upcoming titles on PC including name, publisher, release date, website links
    post_req = 'fields name,involved_companies.company.name,release_dates.human,websites.url; ' \
               'where involved_companies.publisher = true & platforms = 6 & ' + release_date + '' \
               'sort date asc; ' \
               'limit ' + str(limit_value) + '; ' \
               'offset ' + str(offset) + ';'

    # Sends POST request to the games endpoint
    byte_array = wrapper.api_request(
        'games',
        post_req
    )

    # Decodes byte array returned by API wrapper and converts to JSON
    byte_array = bytearray(byte_array)
    req_dict = ast.literal_eval(byte_array.decode('utf8'))
    json_result = json.dumps(req_dict, indent=4, sort_keys=True)

    # Converts JSON to dataframe
    dataframe = pd.read_json(json_result)

    # Cleans up data by inserting only relevant data points into each cell
    for entry in range(len(dataframe)):
        company_list = []
        if type(dataframe['involved_companies'][entry]) == list:
            for company in dataframe['involved_companies'][entry]:
                company_list.append(company['company']['name'])
            dataframe['involved_companies'][entry] = company_list

        dates_list = []
        if type(dataframe['release_dates'][entry]) == list:
            for date in dataframe['release_dates'][entry]:
                dates_list.append(date['human'])
            dataframe['release_dates'][entry] = dates_list

        website_list = []
        if type(dataframe['websites'][entry]) == list:
            for website in dataframe['websites'][entry]:
                website_list.append(website['url'])
            dataframe['websites'][entry] = website_list

    # Appends dataframe to the dataframe list
    dataframe_list.append(dataframe)

# Combines all dataframes into one dataframe
combined_dataframe = pd.concat(dataframe_list)

# Converts to dataframe to csv
csv_name = 'database' + str(time.time()) + '.csv'
outfile = open(csv_name, 'wb')
combined_dataframe.to_csv(outfile, index=False, header=True, sep=',', encoding='utf-8')
outfile.close()



