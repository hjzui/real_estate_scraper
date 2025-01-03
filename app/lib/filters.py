class ListingFilter:
    def __init__(self, price_threshold=10000):
        self.price_threshold = price_threshold

    def apply_filters(self, listings):
        """Apply all filtering criteria defined in this class."""
        filtered_listings = self.filter_by_price(listings)
        # You can chain additional filters here, e.g.,
        # filtered_listings = self.filter_by_location(filtered_listings, location)
        return filtered_listings

    def filter_by_price(self, listings):
        """Filter listings based on the price threshold."""
        return [entry for entry in listings if entry['price'] >= self.price_threshold]

    # Additional filtering methods can be added here as needed
    # def filter_by_location(self, listings, location):
    #     # Example method for future location-based filtering
    #     pass
