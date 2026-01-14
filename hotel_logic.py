from db_connect import get_connection

def choose_best_hotel(location, budget):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, price, rating
        FROM hotels
        WHERE location ILIKE %s AND price <=%s
        ORDER BY rating DESC
        LIMIT 2;
    """, (location, budget))

    hotel = cur.fetchone()
    cur.close()
    conn.close()

    if hotel:
        return {"name": hotel[0], "price": hotel[1], "rating": hotel[2]}
    else:
        return {"message": "No hotels found"}




