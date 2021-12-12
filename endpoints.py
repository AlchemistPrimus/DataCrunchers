"""This is the app's endpoint that is responsible for rendering data to the html files. Processed data(information) passed through this file to find their way to the web."""
from flask import render_template, Blueprint
import folium
import pandas as pd
import geopandas as gpd
import json
import requests

routes=Blueprint("routes",__name__)

url = (
    "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
)
vis1 = json.loads(requests.get(f"{url}/vis1.json").text)
vis2 = json.loads(requests.get(f"{url}/vis2.json").text)
vis3 = json.loads(requests.get(f"{url}/vis3.json").text)

@routes.route("/",methods=["GET"])
def index():
    df_hospitals = gpd.read_file("gdf_hospitals.geojson")
    #head=df_hospitals.head()
    Shapefiles = gpd.read_file("County.shp")
    
    #kenyan coordinates
    coordinates=[0.0236,37.9062]
    kc_latitude=coordinates[0]
    kc_longitude=coordinates[1]
    
    #creating map object
    KEN=folium.Map([kc_latitude, kc_longitude], zoom_start=6,tiles="Stamen Terrain")
    
    
    choropleth= folium.Choropleth(
    geo_data= df_hospitals,
    data=df_hospitals,
    columns=('OBJECTID','size'),
    key_on=('feature.properties.OBJECTID'),
    fill_color=('PiYG'),
    fill_opacity=0.8,
    nan_fill_opacity=0.4,
    line_opacity=0.2,
    show=True,
    overlay=True,
    legend_name=('NUMBER OF HOSPITALS PER COUNTY'),
    highlight=True,
    nan_fill_color = "White",
    reset=True
    ).add_to(KEN)

    folium.Circle(
        radius=100,
        location=[kc_latitude,kc_longitude],
        popup="Risk Area",
        color="crimson",
        fill=False,
    ).add_to(KEN)

    folium.CircleMarker(
        location=[kc_latitude,kc_longitude],
        radius=40,
        popup="Meru TB",
        color="#3186cc",
        fill=True,
        fill_color="#3186cc",
    ).add_to(KEN)
    
    folium.Marker(
    location=[kc_latitude+0.5, kc_longitude-1],
    popup=folium.Popup(max_width=450).add_child(
        folium.Vega(vis1, width=450, height=250)
    ),
    ).add_to(KEN)

    folium.Marker(
        location=[kc_latitude, kc_longitude],
        popup=folium.Popup(max_width=450).add_child(
            folium.Vega(vis2, width=450, height=250)
        ),
    ).add_to(KEN)

    folium.Marker(
        location=[kc_latitude-1, kc_longitude+1],
        popup=folium.Popup(max_width=450).add_child(
            folium.Vega(vis3, width=450, height=250)
        ),
    ).add_to(KEN)

    # Add dark and light mode. 
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(KEN)
    folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(KEN)

    # We add a layer controller. 
    folium.LayerControl(collapsed=False).add_to(KEN)
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['COUNTY','Shape_Leng'], labels=False))

    KEN.save("templates/my_map")
    return render_template("index.html")

@routes.route('/map')
def map():
    return render_template('my_map')