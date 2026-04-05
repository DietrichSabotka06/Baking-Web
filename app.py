from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB = "recipes.db"
RECIPE_FOLDER = "recipes"

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
    data = c.fetchall()
    conn.close()

    recipes = []
    for r in data:
        recipes.append({
            "id": r[0],
            "title": r[1],
            "image": r[2],
            "link": r[3],
            "file": r[4]
        })
    return jsonify(recipes)

@app.route("/api/add", methods=["POST"])
def add_recipe():
    data = request.json

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO recipes (title, image, link, file_path) VALUES (?, ?, ?, ?)",
              (data["title"], data["image"], data["link"], data["file"]))
    conn.commit()
    conn.close()

    return {"status": "ok"}

@app.route("/recipes/<path:filename>")
def serve_recipe(filename):
    return app.send_static_file(f"../recipes/{filename}")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
