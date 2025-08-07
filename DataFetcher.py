import requests
from bs4 import BeautifulSoup

from readNews import scrape_jugantor_news
links = []
newss = []
def FetchNews(url):
    #url = "https://www.jugantor.com/campus"

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
    emtrystring = ""
    for title, link in results:
        #print(f"{title} ==> {link}")
        #print(f"{title} ==> {link}")
        from reader import scrape_jugantor_news
        news,imageslinks = scrape_jugantor_news(link)
        newss.append(news)
        links.append(imageslinks)



national = "https://www.jugantor.com/national"
latest = "https://www.jugantor.com/latest"
political = "https://www.jugantor.com/politics"
economics = "https://www.jugantor.com/economics"
international = "https://www.jugantor.com/international"
country_news = "https://www.jugantor.com/country-news"
entertainment = "https://www.jugantor.com/entertainment"
job_seek = "https://www.jugantor.com/job-seek"
education = "https://www.jugantor.com/campus"
technology ="https://www.jugantor.com/tech"
lifestyle = "https://www.jugantor.com/lifestyle"
islam = "https://www.jugantor.com/islam-life"
various = "https://www.jugantor.com/various"
sociaMedia ="https://www.jugantor.com/social-media"
interview = "https://www.jugantor.com/interview"
corporateNews = "https://www.jugantor.com/corporate-news"
litareture = "https://www.jugantor.com/literature"
bichchu = "https://www.jugantor.com/bicchu"
FetchNews(interview)
