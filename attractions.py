from db_connect import get_connection

def get_top_attractions(city, limit=1):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name,type,rating
        FROM attractions
        WHERE city=%s
        ORDER BY rating DESC
        LIMIT %s;
    """, (city, limit))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [{'name': r[0], 'type': r[1], 'rating': r[2]} for r in rows]
    

    









