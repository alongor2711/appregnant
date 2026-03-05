import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from database import init_db, check_ingredients, get_all_ingredients, add_ingredient, delete_ingredient
from ocr import extract_text

app = Flask(__name__)


@app.before_request
def setup():
    # Runs once on first request to ensure the table exists
    global _db_ready
    if not _db_ready:
        init_db()
        _db_ready = True


_db_ready = False


# ── Main checker page ────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    text = (data or {}).get("ingredients", "").strip()
    if not text:
        return jsonify({"error": "No ingredients provided"}), 400
    results = check_ingredients(text)
    return jsonify({"results": results})


@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    try:
        text = extract_text(file.read())
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Settings page ────────────────────────────────────────────────────────────

@app.route("/settings")
def settings():
    ingredients = get_all_ingredients()
    return render_template("settings.html", ingredients=ingredients)


@app.route("/settings/add", methods=["POST"])
def settings_add():
    name   = request.form.get("name", "").strip()
    status = request.form.get("status", "").strip()
    notes  = request.form.get("notes", "").strip()
    if name and status:
        add_ingredient(name, status, notes)
    return redirect(url_for("settings"))


@app.route("/settings/delete", methods=["POST"])
def settings_delete():
    name = request.form.get("name", "").strip()
    if name:
        delete_ingredient(name)
    return redirect(url_for("settings"))


# ── Health check (for K8s liveness probe) ───────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
