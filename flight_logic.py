from db_connect import get_connection

def get_cheapest_flight(source, destination, budget):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT source, destination, price, airline
        FROM flights
        WHERE source=%s AND destination=%s AND price <= %s
        ORDER BY price ASC LIMIT 2;
    """, (source, destination, budget))

    flight = cur.fetchone()
    cur.close()
    conn.close()

    if flight:
        return {"source": flight[0], "destination": flight[1], "price": flight[2], "airline": flight[3]}
    else:
        return {"message": "No flights found"}



