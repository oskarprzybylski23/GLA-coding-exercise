# This file is a demo limited to first 10 links to cut down on processing time

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
first_ten_urls = urls[:10]


data = [] # placeholder for data

# Ask user for the phrase to search, ensuring it is not empty
while True:
    search_phrase = input("Enter the search phrase (e.g., 'mayor of London'): ").strip()
    if search_phrase:  # Checks if the string is not empty
        break
    else:
        print("The search phrase cannot be empty. Please enter a valid phrase.")

pattern = re.compile(search_phrase, re.IGNORECASE) # search pattern

# search through each web page, count matching patterns and append output to the data object
for url in tqdm(first_ten_urls, desc='Searching in progress: ', leave=False, colour='green'):
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

print("\n")
print(df)
df.to_csv("report_demo.csv", index=False)
print("\n"+"search results have been saved to ./report_demo.csv")