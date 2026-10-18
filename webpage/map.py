
import folium
import json

from branca.element import MacroElement
from jinja2 import Template


def create_map():
    m = folium.Map(
        location=[37.002, -119.001],
        zoom_start=7,
        tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png",
        attr="© Stadia Maps © OpenMapTiles © OpenStreetMap contributors"
    )

    # Qt JavaScript bridge
    m.get_root().header.add_child(folium.Element("""
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <script>
            window.qtBridge = null;

            function connectQtBridge() {
                if (typeof QWebChannel === "undefined") {
                    console.error("QWebChannel is not loaded");
                    return;
                }

                if (typeof qt === "undefined" || !qt.webChannelTransport) {
                    console.error("Qt WebChannel transport is unavailable");
                    return;
                }

                new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.qtBridge = channel.objects.bridge;

                    console.log("Qt bridge connected:", window.qtBridge);
                    console.log(
                        "Available bridge methods:",
                        Object.keys(window.qtBridge)
                    );
                    console.log(
                        "OpenCamera:",
                        typeof window.qtBridge.OpenCamera
                    );
                });
            }

            connectQtBridge();
        </script>
    """))

    return m


class CameraClick(MacroElement):
    _template = Template("""
    {% macro script(this, kwargs) %}
        {{ this._parent.get_name() }}.on('click', function(e) {
            if (window.qtBridge) {
                window.qtBridge.OpenCamera({{ this.camera_url | tojson }}, {{ this.camera_name | tojson }});
            } 
            else {
                console.error("Qt bridge not connected");
            }
        });
    {% endmacro %}
    """)

    def __init__(self, camera_url, camera_name):
        super().__init__()
        self._name = "CameraClick"
        self.camera_url = camera_url
        self.camera_name = camera_name


def add_marker(m, lat, lon, popup_text, camera_url, camera_name):

    marker = folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        tooltip=popup_text,
        icon=folium.Icon(color="blue", icon="info-sign")
    )

    marker.add_to(m)
    marker.add_child(CameraClick(camera_url, camera_name))


def save_map(m):
    m.save("templates/map.html")
