from lib.scraper_utils import extract_data_from_page
from lib.db_utils import save_data_to_db
from config import BASE_URL

def main():
    current_page = 1
    max_page_reached = False
    
    while not max_page_reached:
        url = BASE_URL if current_page == 1 else f"{BASE_URL}seite:{current_page}/"
        print(f"Loading page: {url}")  # Debug print for current page
        data = extract_data_from_page(url)
        
        if not data:  # Stop if no more data is returned
            max_page_reached = True
            print("No more data retrieved, stopping.")  # Debug print
        else:
            save_data_to_db(data)
            print(f"Data from page {current_page} saved to database.")  # Debug print
            current_page += 1

if __name__ == '__main__':
    main()
