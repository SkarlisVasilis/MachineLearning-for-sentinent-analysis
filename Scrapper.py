import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import io
import os

# To later store the url for each abstract page
all_urls = []
# To later store the filename for each abstract page
filenames = []

# Keep the full urls for each abstract page
pages = []
# Check the pages 15 to 25, of the search results from the query: Death rate due to road traffic+injuries
page_numbers = list(range(15, 26))
for page_number in page_numbers :
    page = "https://pubmed.ncbi.nlm.nih.gov/?term=" + "Death+rate+due+to+road+traffic+injuries" + "&page=" + str(page_number)
    pages.append(page)

# For each page url, keep the id of the page.
for page in pages :
    html = requests.get(page).content
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find("div",{"class":"search-results"})

    for i in articles.find_all("a", class_= "docsum-title"):
        if i["href"] is not None:
            id = i['href'].replace("/", "")
            filename = "PMID-" + id + ".txt"
            url = "https://pubmed.ncbi.nlm.nih.gov" + i['href']
            filenames.append(filename)
            all_urls.append(url)

    sleep(1)


# Extract Titles and Abstracts from each page
titles = []
abstracts = []


for url in all_urls :
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

# Try to find title of page. If not keep value "NO TITLE"
    try :
        title = soup.find("h1", class_="heading-title").text
        title = title.replace("\n", "").lstrip().rstrip()
        titles.append(title)
    except:
        title = "NO TITLE"
        titles.append(title)

    # Try to find content text of page. If not keep value "NO ABSTRACT"
    try :
        abstract = soup.find("div", class_="abstract-content selected").text
        abstract = abstract.replace("\n", "").lstrip().rstrip()
        abstracts.append(abstract)
    except:
        abstract = "NO ABSTRACT"
        abstracts.append(abstract)
    sleep(1)

# Create a Metadata dataframe that contains the filename, url and title of each page we extracted information from.
# We then export it as an excel file.
Articles_Batch_Metadata = pd.DataFrame({'Filename': filenames,'Url': all_urls,'Title': titles})
Articles_Batch_Metadata.to_excel (r'batch_temp_index.xlsx', index = False, header=True)

print(Articles_Batch_Metadata[['Url', 'Filename']])

# Create batch_temp folder that contains the txt files. Each txt file will contain the title of each page and its equivalent abstract.
if not os.path.exists('batch_temp'):
    os.makedirs('batch_temp')

# Write txt files on folder batch_temp.
for url in all_urls:
    path = r"batch_temp/" + filenames[all_urls.index(url)]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(titles[all_urls.index(url)] + "\n\n")
        f.write(abstracts[all_urls.index(url)])
        sleep(1)
