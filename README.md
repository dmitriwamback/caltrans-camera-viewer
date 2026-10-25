# Caltrans Highway Camera Monitor in Qt

<p><code>caltrans-camera-viewer</code> is a Qt and Flask application that allows the user to view camera feed across highways in California. All data comes directly from a California government site as seen in <code>webpage/caltrans_fetcher.py</code> (https://cwwp2.dot.ca.gov/data).</p>

---

### Technologies:

The app has two different endpoints:
* 1. A custom flask API which is responsible to provide a map with markers of found and working cameras.

* 2. A Qt application which renders that map and opens new tabs for selected cameras.

Additional technologies include:
<p></p>
For the flask side:

* 1. flask
* 2. requests
* 3. folium
* 4. jinja2
* 5. branca

<p></p>
For the Qt side:

* 1. Qt
* 2. Qt WebEngineWidgets
* 3. Qt Multimedia
* 4. Qt MultimediaWidgets
* 5. Qt WebChannel
* 6. cmake

---

### Updating cameras

Sometimes, cameras can go offline but the program cannot tell. So it is ideal to run <code>caltrans_fetcher.py</code> periodically to filter out offline cameras and discover new ones.

<p>To update them:</p>

```
cd webpage
python3 caltrans_fetcher.py
```

This command saves the new found cameras in the <code>webpage/cache/caltrans_cameras.json</code> file so the script does not have to be run again before running the application.

---

### Running the application

At first, run the flask API since this is what the C++ side is dependent on.

```
cd webpage
python3 api.py
```

Secondly, build the c++ app using the CMakeLists.txt (in the root directory):

```
cmake CMakeLists.txt
cmake --build .
./caltrans-highway-viewer
```

---

### Sample

<p>Sample image:</p>

<img width="1506" height="936" alt="Image" src="https://github.com/user-attachments/assets/45b5c87b-ebb9-4e2a-af45-a6d8d9673e53" />