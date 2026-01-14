import pandas as pd
import psycopg2


conn= psycopg2.connect(
        dbname="travel_ai",
        user="postgres",
        password="mypassword",
        host="localhost",
        port="5432"
    )

cur = conn.cursor()

print("Inserting hotels...")
hotels = pd.read_csv("hotels_extended.csv")
for _, row in hotels.iterrows():
    cur.execute(
        "INSERT INTO hotels (name, location, price, rating) VALUES (%s, %s, %s, %s)",
        (row['name'], row['location'], row['price'], row['rating'])
    )

# insert attractions
print("Inserting attractions...")
attractions = pd.read_csv("attractions_extended.csv")
for _, row in attractions.iterrows():
    cur.execute(
        "INSERT INTO attractions (city, name, type, rating) VALUES (%s, %s, %s, %s)",
        (row['city'], row['name'], row['type'], row['rating'])
    )

# insert flights
print("Inserting flights...")
flights = pd.read_csv("flights_data.csv")
for _, row in flights.iterrows():
    cur.execute(
        "INSERT INTO flights (source, destination, price, airline) VALUES (%s, %s, %s, %s)",
        (row['source'], row['destination'], row['price'], row['airline'])
    )

#insert trains
print("Inserting trains...")
trains = pd.read_csv("trains.csv")
for _, row in trains.iterrows():
    cur.execute(
        "INSERT INTO trains (source, destination, price, train_name) VALUES (%s, %s, %s, %s)",
        (row['source'], row['destination'], row['price'], row['train_name'])
    )

conn.commit()
cur.close()
conn.close()
print("✅ All data inserted successfully!")

