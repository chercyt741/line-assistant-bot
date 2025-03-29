import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

BASE_URL = 'https://owt.com.tw/funeral-encyclopedia/27/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_url_once(url, headers, timeout=10):
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an error for HTTP issues
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}. Skipping...")
        return None

def get_all_article_links():
    """從百科主頁抓出所有文章的連結（限定在文章卡片區）"""
    response = fetch_url_once(BASE_URL, HEADERS)
    if response is None:
        return []  # Skip if the request fails

    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    titles = soup.find_all('h3', class_='elementor-post__title')
    for title in titles:
        a = title.find('a', href=True)
        if a:
            href = urljoin(BASE_URL, a['href'])  # Convert relative URLs to absolute
            links.append(href)

    print(f"共找到 {len(links)} 篇文章連結")
    return list(set(links))

def extract_article_content(url):
    """從單篇文章中萃取主要段落內容"""
    response = fetch_url_once(url, HEADERS)
    if response is None:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    containers = soup.find_all('div', class_='elementor-widget-container')
    paragraphs = []

    for container in containers:
        for p in container.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 10:
                paragraphs.append(text)

    if len(paragraphs) < 1:  # Allow articles with at least 1 paragraph
        print(f"內容太少，跳過：{url}")
        return None

    return '\n'.join(paragraphs)

def save_article(content, url):
    """儲存成 .txt 檔，檔名根據網址最後段"""
    os.makedirs('owt_articles', exist_ok=True)
    filename = url.replace(BASE_URL, '').strip('/').replace('/', '_') + '.txt'
    filepath = os.path.join('owt_articles', filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"已儲存：{filename}")

def main():
    article_links = get_all_article_links()
    for link in article_links:
        print(f"處理中：{link}")
        content = extract_article_content(link)
        if content:
            save_article(content, link)
        time.sleep(1)  # Add delay between requests

if __name__ == '__main__':
    main()