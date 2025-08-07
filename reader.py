import requests
from bs4 import BeautifulSoup, Tag, NavigableString
from urllib.parse import urljoin

def scrape_jugantor_news(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    base_url = "https://www.jugantor.com"

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize outputs
    news_text = ""
    image_links = []

    # Title
    title_tag = soup.find('h1', class_='title')
    #title = title_tag.get_text(strip=True) if title_tag else 'No title found'
    #news_text += f"{title}\n\n"

    content_div = soup.find('div', class_='desktopDetailBody')
    if content_div:
        main_div = content_div.find('div')
        if main_div:
            for child in main_div.descendants:
                if isinstance(child, Tag):
                    if child.name == 'p':
                        text = child.get_text(strip=True)
                        if text:
                            news_text += text + "\n\n"

                    elif child.name == 'li':
                        li_text = child.get_text(strip=True)
                        if li_text:
                            news_text += " - " + li_text + "\n"

                    elif child.name == 'figure':
                        img = child.find('img')
                        caption = child.find('figcaption')
                        if img:
                            img_url = img.get('src') or img.get('data-src') or ''
                            img_url = urljoin(base_url, img_url)
                            image_links.append(img_url)
                        else:
                            pass

                        caption_text = caption.get_text(strip=True) if caption else ''
                        news_text += f"[Image]: {caption_text}\nURL: {img_url}\n\n"

                    elif child.name == 'img' and not child.find_parent('figure'):
                        img_url = child.get('src') or child.get('data-src') or ''
                        img_url = urljoin(base_url, img_url)
                        alt = child.get('alt') or ''
                        news_text += f"[Image] {alt}\nURL: {img_url}\n\n"
                        image_links.append(img_url)

                    elif child.name == 'div':
                        div_text = ''.join(s.strip() for s in child.strings if isinstance(s, NavigableString) and s.strip())
                        if div_text:
                            news_text += div_text + "\n\n"

    # Grab images from top photo div also
    photo_div = soup.find('div', class_='desktopDetailPhotoDiv')
    if photo_div:
        img_tag = photo_div.find('img')
        caption_tag = photo_div.find('figcaption')
        if img_tag:
            img_url = img_tag.get('src') or img_tag.get('data-src') or ''
            img_url = urljoin(base_url, img_url)
            caption_text = caption_tag.get_text(strip=True) if caption_tag else ''
            news_text += f"{caption_text}\nURL: {img_url}\n\n"
            image_links.append(img_url)

    # Return as tuple
    return news_text.strip(), image_links