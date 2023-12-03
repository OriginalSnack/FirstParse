import requests
from bs4 import BeautifulSoup
import os


def get_cache_filename(url):
    return f"cache/{url.replace('/', '_').replace(':', '_').replace('.', '_')}.html"


def download_url(url):
    if not os.path.exists('cache'):
        os.makedirs('cache')

    cache_filename = get_cache_filename(url)
    if os.path.exists(cache_filename):
        with open(cache_filename, 'r', encoding='utf-8') as file:
            content = file.read()
        print("Using cached content.")
        return content

    response = requests.get(url)

    if response.status_code == 200:
        content = response.content.decode('utf-8')

        with open(cache_filename, 'w', encoding='utf-8') as file:
            file.write(content)

        print("Downloaded and cached content.")
        return content
    else:
        print(f"Failed to download the page. Status code: {response.status_code}")
        return None


if __name__ == '__main__':
    url = "https://ua.sinoptik.ua"
    content = download_url(url)
    if content is None:
        print("ERROR: CONTENT_IS_NONE")
        exit()
    soup = BeautifulSoup(content, "html.parser")

    weather_info = soup.select_one("div.tabs").text

    items = soup.select("div[class='tabs'] > div[class=main]")

    print()
    print("Прогноз на цей тиждень:")
    for item in items:
        print(item.select_one("p").text)
        print(item.select_one("[class='temperature']").text)
        print(item.select_one('div.weatherIco').get('title'))
        print()