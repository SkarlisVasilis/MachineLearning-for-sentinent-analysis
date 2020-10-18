import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import io
import os


all_urls = []
filenames = []

pages = []
page_numbers = list(range(15, 26))
for page_number in page_numbers :
    page = "https://pubmed.ncbi.nlm.nih.gov/?term=" + "Death+rate+due+to+road+traffic+injuries" + "&page=" + str(page_number)
    pages.append(page)

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



titles = []
abstracts = []


for url in all_urls :
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    try :
        title = soup.find("h1", class_="heading-title").text
        title = title.replace("\n", "").lstrip().rstrip()
        titles.append(title)
    except:
        title = "NO TITLE"
        titles.append(title)

    try :
        abstract = soup.find("div", class_="abstract-content selected").text
        abstract = abstract.replace("\n", "").lstrip().rstrip()
        abstracts.append(abstract)
    except:
        abstract = "NO ABSTRACT"
        abstracts.append(abstract)
    sleep(1)

Articles_Batch_Metadata = pd.DataFrame({'Filename': filenames,'Url': all_urls,'Title': titles})
Articles_Batch_Metadata.to_excel (r'batch_temp_index.xlsx', index = False, header=True)

print(Articles_Batch_Metadata[['Url', 'Filename']])

# Write txt files.
# Create folder that contains the txt files
if not os.path.exists('batch_temp'):
    os.makedirs('batch_temp')

for url in all_urls:
    path = r"batch_temp/" + filenames[all_urls.index(url)]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(titles[all_urls.index(url)] + "\n\n")
        f.write(abstracts[all_urls.index(url)])
        sleep(1)
