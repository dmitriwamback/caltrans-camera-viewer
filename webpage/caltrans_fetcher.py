import os, re, json, csv, io, shutil, subprocess, requests
from concurrent.futures import ThreadPoolExecutor

# constants
UA = {"User-Agent": "Mozilla/5.0 (personal-project)"}
M3U8 = re.compile(r'https?://[^\s"\'<>\\]+?\.m3u[^\s"\'<>\\]*', re.I)

# helpers
LAT = ("latitude", "lat", "y")
LON = ("longitude", "lon", "lng", "long", "x")
NAME = ("locationname", "name", "title", "displayname", "description", "roadway", "location")
 
def num(v):
    if isinstance(v, bool):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None
 

# ======================= extractors =======================
def own_geo(low):

    # find lat/lon from any of the known field names, or from geometry{} or x/y
    lat = next((num(low[k]) for k in LAT if k in low and num(low[k]) is not None), None)
    lon = next((num(low[k]) for k in LON if k in low and num(low[k]) is not None), None)

    # if not lat or not lon, try geometry{} or x/y
    g = low.get("geometry")

    # if geometry is a dict, check for coordinates or x/y
    if isinstance(g, dict):
        c = g.get("coordinates") # GeoJSON style

        # if coordinates is a list of at least 2 numbers, use them
        if isinstance(c, list) and len(c) >= 2 and num(c[0]) is not None and num(c[1]) is not None:
            lon, lat = num(c[0]), num(c[1])

        # if geometry has x and y, use them
        elif num(g.get("x")) is not None and num(g.get("y")) is not None:
            lon, lat = num(g["x"]), num(g["y"])

    if lat is None or lon is None:
        # if lat is None and lon is not None:
        return None

    if abs(lat) > 90 and abs(lon) <= 90:
        # swap lat/lon if lat is out of range and lon is in range
        lat, lon = lon, lat

    if abs(lat) > 90 or abs(lon) > 180 or (lat == 0 and lon == 0):
        # invalid coordinates, return None
        return None

    # round to 6 decimal places for consistency
    return (round(lat, 6), round(lon, 6))
 
 
def own_name(low):
    # find name from any of the known field names, ignoring empty strings and URLs
    for k in NAME:

        # get the value for the key, if it exists
        v = low.get(k)

        # if the value is a non-empty string that does not start with "http", return it stripped of whitespace
        if isinstance(v, str) and v.strip() and not v.lower().startswith("http"):
            return v.strip()

    # if no name is found, return None
    return None
 
 
def scan(node, source):

    # initialize empty lists and sets for streams, geos, and names
    streams, geos, names = [], set(), []

    # if the node is a string, search for M3U8 URLs and add them to streams
    if isinstance(node, str):
        for m in M3U8.findall(node.replace("\\/", "/")):
            streams.append({"name": None, "kind": "hls", "url": m, "lat": None, "lon": None, "source": source})
        return streams, geos, names

    # if the node is a list, recursively scan each element and accumulate streams, geos, and names
    if isinstance(node, list):
        for v in node:
            s, g, n = scan(v, source)
            streams += s; geos |= g; names += n
        return streams, geos, names

    # if the node is a dict, process it to extract geo coordinates and names, and recursively scan its values
    if isinstance(node, dict):

        # convert keys to lowercase for consistent access
        low = {str(k).lower(): v for k, v in node.items()}

        # extract geo coordinates and names from the current node
        g0, n0 = own_geo(low), own_name(low)

        # if geo coordinates are found, add them to the geos set; if a name is found, add it to the names list
        if g0:
            geos.add(g0)
        if n0:
            names.append(n0)

        # recursively scan the values of the dict and accumulate streams, geos, and names
        for v in node.values():
            s, g, n = scan(v, source)
            streams += s; geos |= g; names += n

        # if there is exactly one unique geo coordinate, assign it to any streams that lack coordinates
        if len(geos) == 1:
            lat, lon = next(iter(geos))
            for st in streams:
                if st["lat"] is None:
                    st["lat"], st["lon"] = lat, lon

        # if there is exactly one unique name, assign it to any streams that lack a name
        pick = n0 or (names[0] if len(set(names)) == 1 else None)
        if pick:
            for st in streams:
                if st["name"] is None:
                    st["name"] = pick

    # return the accumulated streams, geos, and names
    return streams, geos, names
 

def extract(data, source):
    # extract streams from the data using the scan function
    streams, _, _ = scan(data, source)

    # assign a default name "camera" to any streams that lack a name
    for s in streams:
        s["name"] = s["name"] or "camera"
    return streams
 
 
def fetch_json(url, params=None, headers=None):
    # fetch JSON data from the specified URL with optional query parameters and headers
    r = requests.get(url, params=params, headers={**UA, **(headers or {})}, timeout=60)

    # raise an exception if the request was unsuccessful
    r.raise_for_status()
    return r.json()
 
 
def fetch_csv(url):
    # fetch CSV data from the specified URL and return it as a list of dictionaries
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    return list(csv.DictReader(io.StringIO(r.text)))
 
 
def fetch_arcgis(layer_url, page=1000):

    # fetch all features from an ArcGIS layer by querying the layer's REST API in pages
    rows, offset = [], 0
    while True:

        # fetch a page of features from the ArcGIS layer using the query endpoint
        d = fetch_json(layer_url.rstrip("/") + "/query", 
                       params={
                            "where": "1=1", 
                            "outFields": "*", 
                            "outSR": 4326, 
                            "f": "json",
                            "resultOffset": offset, 
                            "resultRecordCount": page
                            })

        # extract the features from the response and add them to the rows list
        feats = d.get("features", [])
        rows += feats
        if not d.get("exceededTransferLimit") or not feats:
            return rows
        offset += len(feats)

 
def key(env):
    return os.environ.get(env, "")
 
 
SOURCES = [
    # Caltrans: 12 districts, no key (verify URL pattern against their docs)
    *[{"id": f"CA-D{d}", "type": "json", "url": f"https://cwwp2.dot.ca.gov/data/d{d}/cctv/cctvStatusD{d:02d}.json"} for d in range(1, 13)],
]
 
 
def collect(src):
    t = src["type"]

    if t == "json":
        data = fetch_json(src["url"], src.get("params"), src.get("headers"))

    elif t == "csv":
        data = fetch_csv(src["url"])

    elif t == "arcgis":
        data = fetch_arcgis(src["url"])

    else:
        raise ValueError(f"unknown source type: {t}")
    
    return extract(data, src["id"])
 
def is_live(url, referer="", timeout=15):
    # check if a stream URL is live by using ffprobe to probe the stream and check for a video codec
    h = "User-Agent: Mozilla/5.0\r\n" + (f"Referer: {referer}\r\n" if referer else "")

    try:
        # run ffprobe with the specified headers and timeout, capturing the output
        p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "csv=p=0", "-headers", h, url], capture_output=True, text=True, timeout=timeout)

        # return True if the output is non-empty (indicating a video stream), otherwise return False
        return bool(p.stdout.strip())
    
    except subprocess.TimeoutExpired:
        # if the ffprobe command times out, return False
        return False
 

def validate(cams, workers=32):
    # validate a list of camera streams by checking if they are live using a thread pool for concurrent processing
    with ThreadPoolExecutor(workers) as pool:

        # use the thread pool to map the is_live function over the list of camera streams, checking each stream's URL and referer
        ok = list(pool.map(lambda c: is_live(c["url"], c.get("referer", "")), cams))
    return [c for c, good in zip(cams, ok) if good]
 
 
if __name__ == "__main__":
    # check if ffprobe is available on the system PATH, and exit with an error message if not
    if not shutil.which("ffprobe"):
        raise SystemExit("ffprobe not found on PATH (install ffmpeg)")

    # collect and validate camera streams from the defined SOURCES, handling any exceptions that occur during the collection process
    all_cams = []
    for src in SOURCES:
        try:
            # collect camera streams from the source and add them to the all_cams list
            found = collect(src)

        except Exception as e:
            # print an error message indicating that the collection failed for the source, and continue to the next source
            print(f"{src['id']} failed: {e}")
            continue

        # count how many of the found streams have valid coordinates (lat/lon) and print a summary of the results
        geo = sum(1 for c in found if c["lat"] is not None)

        # print a summary of the number of streams found and how many have valid coordinates, and provide a warning if no coordinates were matched
        print(f"{src['id']}: {len(found)} streams listed, {geo} with coordinates")

        # if no coordinates were matched, print a warning message suggesting to check the feed's field names
        if found and geo == 0:
            print(f"  ! {src['id']}: no coordinates matched, check this feed's field names")

        # add the found streams to the all_cams list for further processing
        all_cams += found
 
    # dedupe by URL
    seen, uniq = set(), []

    # iterate over all collected camera streams and create a list of unique streams based on their URLs, using a set to track seen URLs
    for c in all_cams:
        if c["url"] not in seen:
            seen.add(c["url"])
            uniq.append(c)

    # print a message indicating the number of unique streams found and that they are being validated
    print(f"{len(uniq)} unique, validating...")

    # validate the unique camera streams to check which ones are live, and store the result in the 'live' variable
    live = validate(uniq)
    print(f"{len(live)} live")

    # save to cams.json
    with open("cache/caltrans_cameras.json", "w") as f:
        json.dump(live, f, indent=1)