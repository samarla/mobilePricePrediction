import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


url = "https://phonedb.net/index.php?m=device&s=list&filter=0"
response = requests.get(url=url)
html = BeautifulSoup(response.text, 'html.parser')

crawl_url_list = []
url_list = html.css.select('.container:nth-child(9) > a')
for url in url_list:
    crawl_url_list.append(url['href'])

df = pd.DataFrame(crawl_url_list)
df.to_excel('pages_url_list.xlsx', )

# with open('urls_list', 'w') as f:
#   write = csv.writer(f)
#  write.writerow(crawl_url_list)
