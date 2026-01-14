from db_connect import get_connection

def get_cheapest_train(source, destination, max_price):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT source, destination, price, train_name
        FROM trains
        WHERE source ILIKE %s
          AND destination ILIKE %s
          AND price <= %s
        ORDER BY price ASC
        LIMIT 1;
    """, (source, destination, max_price))

    train = cur.fetchone()
    cur.close()
    conn.close()

    if train:
        return {
            "source": train[0],
            "destination": train[1],
            "price": train[2],
            "train_name": train[3]
        }
    else:
        return {"message": "No trains found"}

if __name__ == "__main__":
    # Example test
    train = get_cheapest_train("Jaipur", "Manali", 3000)
    print("Cheapest Train:", train) 

