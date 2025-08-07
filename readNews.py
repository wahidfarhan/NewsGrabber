import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin


def scrape_jugantor_news(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    base_url = "https://www.jugantor.com"

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Title
    title_tag = soup.find('h1', class_='title')
    title = title_tag.get_text(strip=True) if title_tag else 'No title found'
    print(f"Title: {title}\n")

    # Main content
    content_div = soup.find('div', class_='desktopDetailBody')
    if not content_div:
        print("Content div not found")
        return

    main_div = content_div.find('div')
    if not main_div:
        print("Main content div not found")
        return

    print("----- NEWS CONTENT -----\n")

    # Loop through all descendants to maintain HTML flow order
    for child in main_div.descendants:
        if not isinstance(child, Tag):
            continue

        # Paragraph text
        if child.name == 'p':
            text = child.get_text(strip=True)
            if text:
                print(text + "\n")

        # List items text
        if child.name == 'li':
            li_text = child.get_text(strip=True)
            if li_text:
                print(" - " + li_text)

        # Image inside <figure> or elsewhere
        if child.name == 'figure':
            img = child.find('img')
            caption = child.find('figcaption')
            if img:
                img_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src') or ''
                img_url = urljoin(base_url, img_url)
            else:
                img_url = 'No image URL'

            caption_text = caption.get_text(strip=True) if caption else ''
            print(f"[Image]: {caption_text}\nURL: {img_url}\n")

        elif child.name == 'img' and not child.find_parent('figure'):
            # Images outside figure (eg: nested in <p> or <div>)
            img_url = child.get('src') or child.get('data-src') or ''
            img_url = urljoin(base_url, img_url)
            alt = child.get('alt') or ''
            print(f"[Image] {alt}\nURL: {img_url}\n")
if __name__ == "__main__":
    url = "https://www.jugantor.com/national/981883"  # Replace with your target article
    scrape_jugantor_news(url)
