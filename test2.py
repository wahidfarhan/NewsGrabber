import requests
from bs4 import BeautifulSoup

# Target URL
url = 'https://www.jugantor.com/'

# Headers spoofing to avoid bot block
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# Send GET request
response = requests.get(url, headers=headers)

# Parse with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all divs with the target class
divs = soup.find_all('div', class_='thumbnail marginB15')

# Loop through each div and extract h3 text and a href
for div in divs:
    a_tag = div.find('a')
    h3_tag = div.find('h3')

    if a_tag and h3_tag:
        link = a_tag['href']
        text = h3_tag.get_text(strip=True)
        print(f"{text} ==> {link}")
