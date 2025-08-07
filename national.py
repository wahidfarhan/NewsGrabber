import requests
from bs4 import BeautifulSoup

# Target URL
url = "https://www.jugantor.com/national"

# Make the GET request
response = requests.get(url)
response.encoding = 'utf-8'  # ensure Bangla text displays properly

# Parse with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all news blocks
# Inspecting the site shows news are within divs with class 'thumbnail' or 'media'
# We'll extract both main and list news items

results = []

# For main highlighted news
for item in soup.select('.thumbnail'):
    title_tag = item.find(['h1', 'h3'])
    link_tag = item.find('a', href=True)
    if title_tag and link_tag:
        title = title_tag.get_text(strip=True)
        link = link_tag['href']
        results.append((title, link))

# For listed news items
for item in soup.select('.media'):
    title_tag = item.find(['h4', 'h3'])
    link_tag = item.find('a', href=True)
    if title_tag and link_tag:
        title = title_tag.get_text(strip=True)
        link = link_tag['href']
        results.append((title, link))

# Print the results
for title, link in results:
    print(f"{title} ==> {link}")
    #print(f"{title} ==> {link}")
    from test3 import scrape_jugantor_news
    scrape_jugantor_news(link)

