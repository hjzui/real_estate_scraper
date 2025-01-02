import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    """Fetch HTML content of a given URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
        
def parse_price(price_str):
    """Cleans and converts the price string to a float."""
    try:
        # Remove currency symbols and other non-numeric characters
        cleaned_price = price_str.replace('€', '').replace('EUR', '').replace('VB', '').replace('.', '').replace(',', '.').strip()
        return float(cleaned_price)
    except ValueError:
        print(f"Could not parse price: {price_str}")
        return None
        
def parse_listing(ad):
    """Parses an individual listing from the main page, then visits the detail page if necessary."""
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
                    details['living_space_qm'] = text.split()[0]
                elif 'Zi' in text:
                    details['count_rooms'] = text.replace('Zi.', '').strip()

        detail_items = detail_soup.find_all('li', class_='addetailslist--detail')
        for item in detail_items:
            item_text = item.get_text(strip=True)
            if 'Grundstücksfläche' in item_text:
                details['land_area_qm'] = item.find('span', class_='addetailslist--detail--value').get_text(strip=True).split()[0]
            elif 'Baujahr' in item_text:
                details['year_construction'] = item.find('span', class_='addetailslist--detail--value').get_text(strip=True)

        # Setting the property type
        property_type = 'Wohnung'

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
        'type': property_type
    } if title and link and price is not None else None


def extract_data_from_page(url, max_entries=None):
    """Extracts data from the main search results page."""
    soup = fetch_page_content(url)
    if not soup:
        return []

    listings = soup.find_all('article', class_='aditem')
    print(f"Found {len(listings)} listings on page.")

    data = []
    for ad in listings[:max_entries]:  # Limit to the given number of max_entries
        parsed_data = parse_listing(ad)
        if parsed_data:
            data.append(parsed_data)
        else:
            print("Skipping listing due to missing critical data")

    return data
