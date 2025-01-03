from lib.scraper_utils import extract_data_from_page
from lib.db_utils import save_data_to_db
from lib.filters import ListingFilter
from config import BASE_URL, PAGE_URL_TEMPLATE

def main(max_entries=float('inf')):
    current_page = 1
    total_extracted = 0
    previous_page_content = None
    max_page_reached = False
    listing_filter = ListingFilter(price_threshold=10000)  # Initialize with a price threshold

    while not max_page_reached:
        url = BASE_URL if current_page == 1 else PAGE_URL_TEMPLATE.format(page=current_page)
        print(f"Loading page: {url}")  # Debug: Indicate which page is being loaded
        data = extract_data_from_page(url, max_entries=None)  # Fetch all entries on the current page

        if not data:  # Stop if no more data is returned
            max_page_reached = True
            print("No more data retrieved, stopping.")
        else:
            # Use the filter class to apply all defined filters
            data = listing_filter.apply_filters(data)

            if not data:
                max_page_reached = True
                print("All entries on this page did not meet the filter criteria, stopping.")
            else:
                current_page_content = [entry['title'] for entry in data]

                if current_page_content == previous_page_content:
                    max_page_reached = True
                    print("No new content found - Assuming last page reached.")
                else:
                    save_data_to_db(data)
                    total_extracted += len(data)
                    print(f"Extracted and saved data from page {current_page}. Total extracted: {total_extracted}.")
                    previous_page_content = current_page_content

            if total_extracted >= max_entries:
                print(f"Extraction limit of {max_entries} entries reached.")
                break

            current_page += 1

if __name__ == '__main__':
    main(max_entries=float('inf'))  # Set to "infinite" to fetch all pages
