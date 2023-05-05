# igdb-reader
Program to request data on upcoming game releases using the IGDB.com API & its Python wrapper.

## Usage
### Using Twitch Credentials
Set up your Twitch credentials to use the IGDB.com API. 

Instructions to do so can be found here: https://api-docs.igdb.com/#account-creation

Create a .env file to host your Client-ID (CLIENT_ID) and App Access Token (AUTHORIZATION).
```env
CLIENT_ID=Your-Client-ID
AUTHORIZATION=Your-App-Access-Token
```

### Running Python Script
Parameters can be adjusted as needed. 

```current_time``` can be adjusted to output all games releasing in the future.

```limit_value``` can be adjusted to change the number of results returned by the API per POST request.

```total_entries``` can be adjusted to change the overall number of results outputted.

```alltime_entries``` can be used to indicate the starting point of the search since the API orders searches by ID number. Useful to skip entries that have already been outputted onto a csv file.

```want_release_date``` indicates if the outputted results will have games with an announced release date (value of True) or games with TBD as a release date (value of False). 

Running the script will output a timestamped .csv file in the root folder of the repository.
