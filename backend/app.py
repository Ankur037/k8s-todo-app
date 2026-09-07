from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["tododb"]
items_collection = db["items"]


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Flask backend running"})


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json(silent=True) or request.form

    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name:
        return jsonify({"status": "error", "message": "itemName is required"}), 400

    item = {"itemName": item_name, "itemDescription": item_description}
    result = items_collection.insert_one(item)

    return jsonify({
        "status": "success",
        "id": str(result.inserted_id),
        "item": item
    }), 201


@app.route("/items", methods=["GET"])
def get_items():
    items = []
    for doc in items_collection.find():
        items.append({
            "id": str(doc["_id"]),
            "itemName": doc.get("itemName"),
            "itemDescription": doc.get("itemDescription")
        })
    return jsonify(items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
