from flask import Flask, send_file, jsonify
import json
import map

app = Flask(__name__)

@app.route("/")
def index():
    return send_file("templates/map.html")

m = map.create_map()

markers = []
with open("cache/caltrans_cameras.json", "r") as f:
    markers = json.load(f)

print(len(markers))

i = 0

for marker in markers:
    print(i, marker["name"])
    map.add_marker(m, marker["lat"], marker["lon"], marker["name"])
    i += 1

map.save_map(m)

app.run(host="127.0.0.1", port=8080)