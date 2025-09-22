from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Setup database automatically
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'super_secret_flag')")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        # 🚨 Vulnerable SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            result = "Welcome! 🎉 FLAG{super_sql_injection}"
        else:
            result = "Invalid credentials."

    return render_template_string('''
        <h2>Login</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
        <p>{{result}}</p>
    ''', result=result)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
