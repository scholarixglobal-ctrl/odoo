import psycopg2

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="odoo_db",
    user="odoo",
    password="odoo"
)

# Create cursor
cur = conn.cursor()

# Update password
password_hash = "$pbkdf2-sha512$25000$bK0VolQqxViLcc55j5Gy9g$BIwMVhygH5T.szyv5hQu2qqc9Jznkjb9.Pp9zcHP4SuH3GJLxNDqrFWf8VNRtcbcWQjgYKYzZIBnnr6k5bgANQ"
cur.execute("UPDATE res_users SET password = %s WHERE login = 'admin'", (password_hash,))

# Commit changes
conn.commit()

# Check update
cur.execute("SELECT login, id FROM res_users WHERE login = 'admin'")
result = cur.fetchone()
print(f"Updated user: {result[0]} (ID: {result[1]})")

# Close connection
cur.close()
conn.close()

print("Password updated successfully!")
