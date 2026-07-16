from flask import Flask, request, jsonify
import os

app = Flask(__name__)

notes = []

@app.route("/")
def home():
    return {
        "application": "GKE Notes API",
        "version": "1.0.0",
        "hostname": os.getenv("HOSTNAME", "local")
    }

@app.route("/health")
def health():
    return {"status": "healthy"}

@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)

@app.route("/notes", methods=["POST"])
def create_note():

    body = request.get_json()

    if not body:
        return {"error": "Body required"}, 400

    note = {
        "id": len(notes) + 1,
        "title": body.get("title"),
        "content": body.get("content")
    }

    notes.append(note)

    return jsonify(note), 201


@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):

    global notes

    notes = [n for n in notes if n["id"] != id]

    return {"message": "Deleted"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)