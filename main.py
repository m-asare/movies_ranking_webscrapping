"""
You have been hired by an institution to extract the information of the top 50 movies
with the best average ratings from a specified webpage. The information required is Average Rank, Film, Year
and the film's rank on IMDb's Top 250. Filter the information to contain only films released in the 2000s
(year 2000 included). Extract the information and save it to a csv file and database.
"""

import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup


# Initializing known entities
url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
csv_path = 'Top50_Movies.csv'
table_name = 'Top50_Movies'
db_name = 'Top50_Movies.db'
df = pd.DataFrame(columns=['Average Rank', 'Film', 'Year', 'IMDb Top 250 Rank'])
count = 0

# Loading the webpage for webscraping
web_page = requests.get(url, timeout=10).text
page_data = BeautifulSoup(web_page, 'html5lib')

# Scraping for required information
tables = page_data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
    if count < 50:
        colm = row.find_all('td')
        if len(colm) != 0:
            data = {'Average Rank': colm[0].contents[0],
                    'Film': colm[1].contents[0],
                    'Year': colm[2].contents[0],
                    'IMDb Top 20 Rank': colm[4].contents[0]}
            new_df = pd.DataFrame(data, index=[0])
            df = pd.concat([df, new_df], ignore_index=True)
            count += 1
    else:
        break

# Filtering only movies released in the 2000s
df = df[df['Year'] >= '2000']

# Storing data to csv file
df.to_csv(csv_path)

# Storing data in a database
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()
