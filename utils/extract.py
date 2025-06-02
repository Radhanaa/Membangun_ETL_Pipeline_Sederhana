import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36 Edg/124.0.2478.80"
    )
}


def extract_product_data(card):
    """Ekstrak data dari satu kartu produk"""
    def get_text(tag): return tag.text.strip() if tag else 'N/A'

    return {
        'title': get_text(card.find('h3', class_='product-title')),
        'price': get_text(card.find('div', class_='price-container')),
        'rating': get_text(card.find('p', string=lambda t: t and 'Rating' in t)),
        'colors': get_text(card.find('p', string=lambda t: t and 'Colors' in t)),
        'size': get_text(card.find('p', string=lambda t: t and 'Size' in t)),
        'gender': get_text(card.find('p', string=lambda t: t and 'Gender' in t)),
        'timestamp': datetime.now().isoformat()
    }

def fetch_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Gagal mengakses {url}: {e}")

def scrape_all_pages(base_url, max_pages=5, delay=1):
    """Scrape seluruh halaman koleksi dengan pembatasan halaman maksimal"""
    all_products = []

    for page in range(1, max_pages + 1):
        if page == 1 :
            url = f"{base_url}"
        else :
            url = f"{base_url}/page{page}"
        print(f"📄 Mengambil halaman ke-{page}: {url}")
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        cards = soup.find_all('div', class_='collection-card')
        if not cards:
            print(f"⚠️ Tidak ada produk ditemukan di halaman {url}")
            continue

        for card in cards:
            product = extract_product_data(card)
            all_products.append(product)

        print(f"✅ {len(cards)} produk berhasil diambil dari halaman {page}")
        time.sleep(delay)

    print(f"🎯 Total produk diambil: {len(all_products)}")
    return all_products
'''

import requests
from bs4 import BeautifulSoup
import time

MAX_PAGE = 50  # Jumlah halaman maksimum yang akan di-scrape

def extract_product_data(card):
    """Ekstraksi data produk dari elemen kartu HTML."""
    title = card.find('h3', class_='product-title')
    price = card.find('div', class_='price-container')
    rating = card.find('p', string=lambda t: t and 'Rating' in t)
    colors = card.find('p', string=lambda t: t and 'Colors' in t)
    size = card.find('p', string=lambda t: t and 'Size' in t)
    gender = card.find('p', string=lambda t: t and 'Gender' in t)

    return {
        'title': title.text.strip() if title else 'Unknown Title',
        'price': price.text.strip() if price else 'Price Not Available',
        'rating': rating.text.strip() if rating else 'No Rating',
        'colors': colors.text.strip() if colors else 'No Color Info',
        'size': size.text.strip() if size else 'No Size Info',
        'gender': gender.text.strip() if gender else 'No Gender Info',
    }

def fetch_page_content(url):
    """Mengambil HTML dari URL yang diberikan tanpa headers tambahan."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as error:
        raise Exception(f"Gagal mengambil konten dari {url}: {error}")

def scrape_website(url, delay=1):
    """Mengambil data dari beberapa halaman website tanpa menggunakan headers."""
    data = []

    for page_number in range(1, MAX_PAGE + 1):
        page_url = f"{url}page{page_number}" if page_number > 1 else url
        print(f"🔍 Scraping halaman ke-{page_number}: {page_url}")

        try:
            html = fetch_page_content(page_url)
            soup = BeautifulSoup(html, 'html.parser')
            product_elements = soup.find_all('div', class_='collection-card')

            if not product_elements:
                print(f"Tidak ada produk ditemukan di halaman {page_url}")
                break  # Stop jika tidak ada produk ditemukan

            for card in product_elements:
                product = extract_product_data(card)
                data.append(product)

            print(f"✅ {len(product_elements)} produk berhasil diambil dari halaman {page_number}")

            time.sleep(delay)  # Delay antar halaman agar tidak dianggap spam

        except Exception as e:
            print(f"❌ Gagal memproses halaman ke-{page_number}: {e}")
            break

    return data
'''