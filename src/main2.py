import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="admin",
    password="admin",
    database="test"
)

cursor = conn.cursor(buffered=True)
cursor.execute("SELECT * FROM customer")
print(cursor.fetchall())
conn.commit()
conn.close()

