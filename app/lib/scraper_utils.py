import requests
from bs4 import BeautifulSoup

def extract_data_from_listing(listing_url):
    print(f"Extracting data from listing: {listing_url}")  # Debug print for listing URL
    response = requests.get(listing_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('h1', class_='srh1').get_text(strip=True)
    price = soup.find('span', class_='aditem-main--middle--price-shipping--price').get_text(strip=True)
    
    details = {}
    detail_section = soup.find('div', class_='content')
    if detail_section:
        for detail in detail_section.find_all('li'):
            # Ensure there is a ':' in the text to split on
            if ':' in detail.get_text(strip=True):
                key, value = detail.get_text(strip=True).split(':')
                details[key.strip()] = value.strip()

    print(f"Extracted data: {details}")  # Debug print for extracted details

    return {
        'title': title,
        'link': listing_url,
        'price': price,
        'plz': details.get('PLZ', None),
        'living_space_qm': details.get('Wohnfläche', None),
        'land_area_qm': details.get('Grundstücksfläche', None),
        'count_rooms': details.get('Zimmer', None),
        'year_construction': details.get('Baujahr', None),
    }

def extract_data_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('article', class_='aditem')  # Adjust if necessary

    print(f"Found {len(listings)} listings on page.")  # Debug print for number of listings

    data = []
    for listing in listings:
        try:
            link = listing.find('a', class_='ellipsis')['href']
            full_link = 'https://www.kleinanzeigen.de' + link
            item_data = extract_data_from_listing(full_link)
            data.append(item_data)
        except Exception as e:
            print(f"Error extracting data from listing: {e}")  # Debug print for errors

    return data
