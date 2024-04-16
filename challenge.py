from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from tqdm import tqdm

# access the source with links to extract
source_url = "https://www.london.gov.uk/sitemap.xml?page=1"
source_page = requests.get(source_url)
soup_source = BeautifulSoup(source_page.text, 'xml')

# exctract links
urls = [loc.text for loc in soup_source.find_all("loc")]

data = [] # placeholder for data

search_phrase = 'mayor of London'
pattern = re.compile(search_phrase, re.IGNORECASE) # search pattern

# search through each web page, count matching patterns and append output to the data object
for url in tqdm(urls, desc='Searching in progress: ', leave=False, colour='green'):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    body_content = soup.find('body')
    strings_containing_pattern = body_content.find_all(string = pattern)
    mention_count = len(strings_containing_pattern)
    
    data.append({
            "URL": url,
            "Mention Count": mention_count
        })

# create and output the dataframe
df = pd.DataFrame(data)
print(df)
df.to_csv("report.csv", index=False)