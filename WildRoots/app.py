"""app.py - Flask backend for WildRoots."""

from flask import Flask, render_template, request, jsonify
from species_data import load_species

app = Flask(__name__)
species_list = load_species()          # the Linked List lives here

VALID = {
    "type": ["Plant", "Animal", "Both"],
    "habitat": ["Forest", "Grassland", "Desert", "Aquatic", "Mountain", "Wetland"],
    "temperature": ["Cold", "Moderate", "Hot"],
    "pollution": ["Low", "Medium", "High"],
    "water": ["Low", "Medium", "High"],
    "climate": ["Tropical", "Temperate", "Dry", "Polar"],
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/classify", methods=["POST"])
def classify():
    env = request.get_json(silent=True) or {}
    for field, options in VALID.items():           # validate every field
        if env.get(field) not in options:
            return jsonify({"error": f"Please choose a valid {field}."}), 400
    matches, visited = species_list.classify(env)
    return jsonify({
        "best": matches[0] if matches else None,
        "others": matches[1:],
        "nodes_traversed": visited,
        "total_matches": len(matches),
    })


@app.route("/species")
def species():
    return jsonify(species_list.display())


@app.route("/search")
def search():
    return jsonify(species_list.search(request.args.get("q", "")))


@app.route("/filter", methods=["POST"])
def filter_species():
    d = request.get_json(silent=True) or {}
    return jsonify(species_list.filter(d.get("type", ""), d.get("habitat", ""), d.get("query", "")))


@app.route("/stats")
def stats():
    items = species_list.display()
    return jsonify({
        "total": species_list.count(),
        "plants": sum(1 for s in items if s["type"] == "Plant"),
        "animals": sum(1 for s in items if s["type"] == "Animal"),
        "head": items[0]["name"] if items else None,
        "tail": items[-1]["name"] if items else None,
        "names": [s["name"] for s in items],
    })


if __name__ == "__main__":
    app.run(debug=True)
