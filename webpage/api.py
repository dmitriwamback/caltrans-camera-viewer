
from flask import Flask, send_file
import json
import map

app = Flask(__name__)

@app.route("/")
def index():
    return send_file("templates/map.html")


m = map.create_map()

with open("cache/caltrans_cameras.json", "r") as f:
    markers = json.load(f)

print(f"Loaded {len(markers)} cameras")

for i, marker in enumerate(markers):
    print(i, marker["name"])

    map.add_marker(
        m,
        marker["lat"],
        marker["lon"],
        marker["name"],
        marker["url"]
    )

map.save_map(m)

app.run(host="127.0.0.1", port=8080)