import psycopg2
from config import DATABASE_CONFIG

def get_database_connection():
    return psycopg2.connect(
        host=DATABASE_CONFIG['host'],
        database=DATABASE_CONFIG['database'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        port=DATABASE_CONFIG['port']
    )

def save_data_to_db(data):
    conn = get_database_connection()
    cursor = conn.cursor()
    
    current_timestamp = datetime.now()

    for entry in data:
        # Check for existing entry based on title, PLZ, and link
        cursor.execute("""
            SELECT price FROM listings_apartments WHERE title = %s AND plz = %s AND link = %s
        """, (entry['title'], entry['plz'], entry['link']))
        
        existing_record = cursor.fetchone()
        
        if existing_record:
            existing_price = existing_record[0]
            if existing_price != entry['price']:
                cursor.execute("""
                    UPDATE listings_apartments
                    SET price = %s, living_space_qm = %s, land_area_qm = %s, count_rooms = %s, year_construction = %s, type = %s, "timestamp" = %s
                    WHERE title = %s AND plz = %s AND link = %s
                """, (
                    entry['price'], entry['living_space_qm'], entry['land_area_qm'],
                    entry['count_rooms'], entry['year_construction'], entry['type'],
                    current_timestamp, entry['title'], entry['plz'], entry['link']
                ))
                print(f"Updated entry: {entry['title']} - New price: {entry['price']}")
        else:
            cursor.execute("""
                INSERT INTO listings_apartments (title, link, price, plz, living_space_qm, land_area_qm, count_rooms, year_construction, type, "timestamp")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                entry['title'], entry['link'], entry['price'], entry['plz'],
                entry['living_space_qm'], entry['land_area_qm'], entry['count_rooms'],
                entry['year_construction'], entry['type'], current_timestamp
            ))
            print(f"Added new entry: {entry['title']}")

    conn.commit()
    cursor.close()
    conn.close()
