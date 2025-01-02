from lib.scraper_utils import extract_data_from_page
from lib.db_utils import save_data_to_db
from config import BASE_URL, PAGE_URL_TEMPLATE

def main(max_entries=3):
    current_page = 1
    total_extracted = 0
    max_page_reached = False

    while not max_page_reached:
        url = BASE_URL if current_page == 1 else PAGE_URL_TEMPLATE.format(page=current_page)
        print(f"Loading page: {url}")  # Debug: Indicate which page is being loaded
        data = extract_data_from_page(url, max_entries=max_entries - total_extracted)
        
        if not data:  # Stop if no more data is returned
            max_page_reached = True
            print("No more data retrieved, stopping.")  # Debug: No listings found
        else:
            save_data_to_db(data)  # Assuming this function saves the data, adjust as necessary
            print(f"Data extracted and saved from page {current_page}.")
            total_extracted += len(data)
            
            if total_extracted >= max_entries:
                print(f"Extraction limit of {max_entries} entries reached.")
                break
            
            current_page += 1

if __name__ == '__main__':
    main(max_entries=3)  # Limit to first 3 entries
