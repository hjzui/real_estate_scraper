import re
import requests
from bs4 import BeautifulSoup
from config import BASE_URL, HEADERS

def fetch_page_content(url):
    """Fetch HTML content of a given URL using configured headers."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.content.decode('utf-8', errors='ignore'), 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def parse_price(price_str):
    """Cleans and converts the price string to a float."""
    try:
        prices = re.findall(r'\d+\.?\d*', price_str.replace('.', '').replace(',', '.'))
        if prices:
            most_recent_price = prices[0]
            return float(most_recent_price)
        return None
    except ValueError:
        print(f"Could not parse price: {price_str}")
        return None
        
def parse_listing(ad):
    """Parses an individual listing to extract relevant data."""
    try:
        link_tag = ad.get('data-href')
        link = f"https://www.kleinanzeigen.de{link_tag}" if link_tag else None
        if not link:
            print("Link not found in listing.")
            return None

        detail_soup = fetch_page_content(link)
        if not detail_soup:
            return None

        title_meta = ad.find('meta', itemprop='name')
        title = title_meta['content'] if title_meta else None

        price_tag = ad.find('p', class_='aditem-main--middle--price-shipping--price')
        raw_price = price_tag.get_text(strip=True) if price_tag else None
        price = parse_price(raw_price)

        plz_tag = ad.find('div', class_='aditem-main--top--left')
        plz = plz_tag.get_text(strip=True).split()[0] if plz_tag else None

        details = {
            'living_space_qm': None,
            'land_area_qm': None,
            'count_rooms': None,
            'year_construction': None,
        }

        bottom_section = ad.find('div', class_='aditem-main--bottom')
        if bottom_section:
            tags = bottom_section.find_all('span', class_='simpletag')
            for tag in tags:
                text = tag.get_text(strip=True)
                if f'm\u00b2' in text:
                    # Convert to float-safe format
                    living_space = text.split()[0].replace(',', '.')
                    details['living_space_qm'] = float(living_space)
                elif 'Zi' in text:
                    count_rooms = text.replace('Zi.', '').replace(',', '.').strip()
                    details['count_rooms'] = float(count_rooms) if count_rooms else None

        detail_items = detail_soup.find_all('li', class_='addetailslist--detail')
        for item in detail_items:
            item_text = item.get_text(strip=True)
            if 'Grundstücksfläche' in item_text:
                land_area = item.find('span', class_='addetailslist--detail--value').get_text(strip=True).split()[0].replace(',', '.')
                details['land_area_qm'] = float(land_area)
            elif 'Baujahr' in item_text:
                details['year_construction'] = item.find('span', class_='addetailslist--detail--value').get_text(strip=True)

        # Set the type as "Wohnung"
        type = 'Wohnung'

    except Exception as e:
        print(f"Error parsing listing: {e}")
        return None

    return {
        'title': title,
        'link': link,
        'price': price,
        'plz': plz,
        'living_space_qm': details.get('living_space_qm'),
        'land_area_qm': details.get('land_area_qm'),
        'count_rooms': details.get('count_rooms'),
        'year_construction': details.get('year_construction'),
        'type': type
    } if title and link and price is not None else None
    
def extract_data_from_page(url, max_entries=None):
    """Extracts data from a specified URL page."""
    soup = fetch_page_content(url)
    if not soup:
        return []

    listings = soup.find_all('article', class_='aditem')
    print(f"Found {len(listings)} listings on page.")

    data = []
    for ad in listings[:max_entries]:  # Limit number of entries if max_entries is set
        parsed_data = parse_listing(ad)
        if parsed_data:
            data.append(parsed_data)
        else:
            print("Skipping listing due to missing critical data")

    return data
