from lib.scraper_utils import extract_data_from_page
from lib.db_utils import save_data_to_db
from config import BASE_URL, PAGE_URL_TEMPLATE

def main(max_entries=float('inf')):
    current_page = 1
    total_extracted = 0
    max_page_reached = False

    while not max_page_reached:
        url = BASE_URL if current_page == 1 else PAGE_URL_TEMPLATE.format(page=current_page)
        print(f"Loading page: {url}")  # Debug: Indicate which page is being loaded
        data = extract_data_from_page(url, max_entries=None)  # Fetch all entries on the current page
        
        if not data:  # Stop if no more data is returned
            max_page_reached = True
            print("No more data retrieved, stopping.")
        else:
            save_data_to_db(data)
            total_extracted += len(data)
            print(f"Extracted and saved data from page {current_page}. Total extracted: {total_extracted}.")
            
            if total_extracted >= max_entries:
                print(f"Extraction limit of {max_entries} entries reached.")
                break  # Break the loop if the max_entries limit is reached, although this will not trigger with inf
            
            current_page += 1

if __name__ == '__main__':
    main(max_entries=float('inf'))  # Set to "infinite" to fetch all pages
