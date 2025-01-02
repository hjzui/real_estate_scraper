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

    for entry in data:
        cursor.execute("""
            INSERT INTO listings_apartments (title, link, price, plz, living_space_qm, land_area_qm, count_rooms, year_construction) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (entry['title'], entry['link'], entry['price'], entry['plz'], entry['living_space_qm'], entry['land_area_qm'], entry['count_rooms'], entry['year_construction']))
    
    conn.commit()
    cursor.close()
    conn.close()
