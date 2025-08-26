from flask import Flask, jsonify, request
from flask_cors import CORS  
import json
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# Load colleges data
with open("colleges.json", "r") as f:
    colleges = json.load(f)

# -----------------------------
# Routes
# -----------------------------

# Get all colleges (with search + pagination support)
@app.route("/colleges", methods=["GET"])
def get_colleges():
    query = request.args.get("q", "").lower()       # search query
    page = int(request.args.get("page", 1))         # page number
    per_page = int(request.args.get("per_page", 10)) # results per page

    # Filter by search query if provided
    filtered = [c for c in colleges if query in c["name"].lower()]

    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated = filtered[start:end]

    return jsonify({
        "results": paginated,
        "total": len(filtered),
        "page": page,
        "per_page": per_page
    })


# Get single college details
@app.route("/college/<int:college_id>", methods=["GET"])
def get_college(college_id):
    college = next((c for c in colleges if c["id"] == college_id), None)
    if college:
        return jsonify(college)
    return jsonify({"error": "College not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
