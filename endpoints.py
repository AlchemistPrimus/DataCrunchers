from flask import render_template, Blueprint
import folium
import pandas as pd
import geopandas as gpd
routes=Blueprint("routes",__name__)


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
    KEN=folium.Map([kc_latitude, kc_longitude], zoom_start=6)
    
    
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