import concurrent.futures
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import tqdm

df = pd.read_excel('mobileUrlsList.xlsx', index_col=0)

root_url = "https://phonedb.net/"

# with open('mobileSpecs.html') as f:
#   soup = BeautifulSoup(f, 'html.parser')

mobile_db = pd.DataFrame()


def scrape_mobile(url):
    ''' This function takes url as input and return specification type and specification
    detail as key-value pair of dict.
    '''
    response = requests.get(url=url)
    # make a soup out of it
    soup = BeautifulSoup(response.text, 'html.parser')
    # find the table in the soup
    table = soup.find('table')
    # get the table data row wise
    table_data = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all('td'):
            row_data.append(cell.get_text(strip=True))
        table_data.append(row_data)

    # create an empty dict to add all the specs as key-value pair
    d = {}
    c = 0
    for row in table_data:
        if len(row) > 1:
            d[row[0]] = row[1:]
        else:
            d[c] = row[0]
            c += 1
    return d
    # except Exception as e:
    #   print(f'error scraping {url}: {e}')
    #  return None


num_workers = 8
results = []
# iterate through urls over the dataframe
for mobile_url in tqdm.tqdm(df.iloc[10000:15000].itertuples(), desc="Scraping Mobile URLs"):
    # concat to get complete url of a mobile
    url = root_url+str(mobile_url[1])
    # print(url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        result = executor.submit(scrape_mobile, url)
        results.append(result)


scraped_data_list = [result.result()
                     for result in results if result.result() is not None]
mobile_db = pd.DataFrame(scraped_data_list)
mobile_db.to_excel('mobileDB_10000_to_15000.xlsx', index=False)

# parallel_dicts = {}
# for i in range(8):
#     if results[i] is not None:
#         #specs_dict = scrape_mobile(url)
#         # dump the dict to pandas dataframe
#         df_name = f'scrape_df_{i}'
#         parallel_dicts[df_name] = pd.DataFrame([results[i]])
#         # concat with the already existing dataframe
#         mobile_db = pd.concat([mobile_db, current_mobile_db], ignore_index=True)
#         mobile_db.to_excel('mobileDB.xlsx')
