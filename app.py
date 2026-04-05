from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)

DB = "recipes.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            title TEXT,
            image TEXT,
            link TEXT,
            file_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/recipes")
def get_recipes():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM recipes")
    rows = c.fetchall()
    conn.close()

    return jsonify([
        {
            "id": r[0],
            "title": r[1],
            "image": r[2],
            "link": r[3],
            "file": r[4]
        } for r in rows
    ])

@app.route("/api/add", methods=["POST"])
def add_recipe():
    data = request.json

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO recipes (title, image, link, file_path) VALUES (?, ?, ?, ?)",
        (data["title"], data["image"], data["link"], data["file"])
    )
    conn.commit()
    conn.close()

    return {"status": "ok"}

@app.route("/recipes/<path:filename>")
def serve_recipe(filename):
    return send_from_directory("recipes", filename)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
