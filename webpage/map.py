import folium

def create_map():
    m = folium.Map(location=[37.002, -119.001],  # Center of California
        zoom_start=7,
        tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png",
        attr="© Stadia Maps © OpenMapTiles © OpenStreetMap contributors"
    )

    m.save("templates/map.html")
    return m

def add_marker(m, lat, lon, popup_text):
    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

    #m.save("templates/map.html")

def save_map(m):
    m.save("templates/map.html")