
import sqlite3

# ❌ UNSAFE EXAMPLE (Vulnerable to injection if used with raw input)
def get_user_vulnerable(conn, userInput):
    query = f"SELECT * FROM users WHERE username = '{userInput}'"
    print("Running query:", query)
    cursor = conn.cursor()
    cursor.execute(query)  # Unsafe if userInput contains malicious SQL
    return cursor.fetchall()

# ✅ SAFE EXAMPLE (Using parameterized queries)
def get_user_secure(conn, userInput):
    query = "SELECT * FROM users WHERE username = ?"
    print("Running secure query with parameters.")
    cursor = conn.cursor()
    cursor.execute(query, (userInput,))
    return cursor.fetchall()

if __name__ == "__main__":
    # Demo setup
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
    conn.execute("INSERT INTO users (username) VALUES ('akarsh')")
    conn.commit()

    # Run both examples
    print(get_user_vulnerable(conn, "akarsh"))
    print(get_user_secure(conn, "akarsh"))
