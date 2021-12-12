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

#kenyan coordinates
coordinates=[0.0236,37.9062]
kc_latitude=coordinates[0]
kc_longitude=coordinates[1]


@routes.route("/",methods=["GET"])
def index():
    
    return render_template("index.html")

@routes.route('/map')
def map():
    """Displays visualizations of Hospitals per county."""
    
    operation_status_of_hospitals= gpd.read_file('gdf_operation_status_of_hospitals.geojson')
    operation_status = round(operation_status_of_hospitals, 2)
    operation_status.rename(columns={'size': 'Total_Hospitals','Yes':'%24/7','No':'% Not24/7' }, inplace=True)
    KEN=folium.Map([kc_latitude, kc_longitude], zoom_start=6,tiles="Stamen Terrain")

    choropleth= folium.Choropleth(
        geo_data= operation_status,
        data=operation_status,
        columns=('OBJECTID','% Not24/7'),
        key_on=('feature.properties.OBJECTID'),
        fill_color=('OrRd'),
        fill_opacity=0.8,
        nan_fill_opacity=0.4,
        line_opacity=0.5,
        name='Hospitals',
        show=True,
        overlay=True,
        legend_name=('OPERATION STATUS OF HOSPITALS'),
        highlight=True,
        nan_fill_color = "black",
        reset=True
    ).add_to(KEN)
    # Add hover functionality.
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    # Add dark and light mode. 
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(KEN)
    folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(KEN)

    # We add a layer controller. 
    folium.LayerControl(collapsed=False).add_to(KEN)
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['COUNTY','Total_Hospitals','% Not24/7','%24/7'], labels=True))

    KEN.save("templates/my_map")
    
    return render_template('my_map')

@routes.route('/map1')
def map1():
    #Community health units
    status_of_community_health_units= gpd.read_file('gdf_number_and_status_of_community_health_units.geojson')
    status_of_community = round(status_of_community_health_units, 2)
    status_of_community.rename(columns={'size': 'Total_CH','Fully_functional':'% Fully_functional','Not_fully_functional':'% Not_fully_functional' }, inplace=True)
    
    community_health_units=folium.Map([kc_latitude, kc_longitude], zoom_start=6,tiles="Stamen Terrain")

    choropleth= folium.Choropleth(  
    geo_data=status_of_community,
    data=status_of_community,
    columns=('OBJECTID','% Not_fully_functional'),
    key_on=('feature.properties.OBJECTID'),
    fill_color=('OrRd'),
    fill_opacity=0.8,
    nan_fill_opacity=0.4,
    line_opacity=0.5,
    name='Health units',
    show=True,
    overlay=True,
    legend_name=('Not_fully_functional community health units'),
    highlight=True,
    nan_fill_color = "black",
    reset=True
    ).add_to(community_health_units)
    # Add hover functionality.
    
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    # Add dark and light mode. 
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(community_health_units)
    folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(community_health_units)

    # We add a layer controller. 
    folium.LayerControl(collapsed=False).add_to(community_health_units)
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['COUNTY','Total_CH','% Not_fully_functional','% Fully_functional'], labels=True))
    community_health_units.save("templates/community_h_u")
    return render_template("community_h_u")
    

@routes.route("/map2")
def map2():
    #Mapping internet access
    internet_through_mobile= gpd.read_file('gdf_internet_through_mobile.geojson')
    internet = round(internet_through_mobile, 2)
    internet.rename(columns={'size': 'Total_interviewee','No':'% No access','Yes':'% Access' }, inplace=True)
    
    internet_usage=folium.Map([kc_latitude, kc_longitude], zoom_start=6,tiles="Stamen Terrain")

    choropleth= folium.Choropleth(
        geo_data=internet,
        data=internet,
        columns=('OBJECTID','% No access'),
        key_on=('feature.properties.OBJECTID'),
        fill_color=('OrRd'),
        fill_opacity=0.8,
        nan_fill_opacity=0.4,
        line_opacity=0.5,
        name='Mobile internet',
        show=True,
        overlay=True,
        legend_name=('Internet access through mobile usage'),
        highlight=True,
        nan_fill_color = "black",
        reset=True
    ).add_to(internet_usage)
    # Add hover functionality.
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    # Add dark and light mode. 
    """
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(internet_usage)
    folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(internet_usage)
    """
    # We add a layer controller. 
    folium.LayerControl(collapsed=False).add_to(internet_usage)
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['COUNTY','Total_interviewee','% No access','% Access'], labels=True))
    internet_usage.save("templates/internet_usage")
    
    return render_template("internet_usage")


@routes.route("/map3")
def map3():
    #mapping fixed internet at home
    fixed_internet_at_home = gpd.read_file('gdf_fixed_internet_at_home.geojson')
    fixed_internet = round(fixed_internet_at_home, 2)
    fixed_internet.rename(columns={'size':'Total_interviewee','No':'% No fixed internet','Yes':'% fixed internet' }, inplace=True)
    
    internet_fixed=folium.Map([kc_latitude, kc_longitude], zoom_start=6,tiles="Stamen Terrain")

    choropleth= folium.Choropleth(
        geo_data=fixed_internet,
        data=fixed_internet,
        columns=('OBJECTID','% No fixed internet'),
        key_on=('feature.properties.OBJECTID'),
        fill_color=('OrRd'),
        fill_opacity=0.8,
        nan_fill_opacity=0.4,
        line_opacity=0.5,
        name='Fixed internet',
        show=True,
        overlay=True,
        legend_name=('Fixed_internet at home'),
        highlight=True,
        nan_fill_color = "black",
        reset=True
    ).add_to(internet_fixed)
    # Add hover functionality.
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    # Add dark and light mode. 
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(internet_fixed)
    folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(internet_fixed)

    # We add a layer controller. 
    folium.LayerControl(collapsed=False).add_to(internet_fixed)
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['COUNTY','Total_interviewee','% No fixed internet','% fixed internet'], labels=True))
    internet_fixed.save("templates/internet_fixed")
    
    return render_template("internet_fixed")


@routes.route("/map4")
def map4():
    #Mapping health staff percentage change
    health_staff_percentage_change = gpd.read_file('gdf_health_staff_percentage_change.geojson')
    health_staff = round(health_staff_percentage_change, 2)
    health_staff_percentage=folium.Map([kc_latitude, kc_longitude], zoom_start=6,tiles="Stamen Terrain")

    choropleth= folium.Choropleth(
        geo_data=health_staff,
        data=health_staff,
        columns=('OBJECTID','% change per 10000\population'),
        key_on=('feature.properties.OBJECTID'),
        fill_color=('OrRd'),
        fill_opacity=0.8,
        nan_fill_opacity=0.4,
        line_opacity=0.5,
        name='Health staff',
        show=True,
        overlay=True,
        legend_name=('health staff percentage change'),
        highlight=True,
        nan_fill_color = "black",
        reset=True
    ).add_to(health_staff_percentage)
    # Add hover functionality.
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    # Add dark and light mode. 
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(health_staff_percentage)
    folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(health_staff_percentage)

    # We add a layer controller. 
    folium.LayerControl(collapsed=False).add_to(health_staff_percentage)
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['COUNTY','% change per 10000\population'], labels=True))
    health_staff_percentage.save("templates/health_s_percentage")
    
    return render_template("health_s_percentage")
    
    
@routes.route("/map5")
def map5():
    #Mapping internet users
    internet_users = gpd.read_file('gdf_internet_users.geojson')
    net_users = round(internet_users, 2)
    net_users.rename(columns={'size':'Total_users','No':'% No Use','Yes':'% Used','DK':'Don`t know'}, inplace=True)
    
    net_user=folium.Map([kc_latitude, kc_longitude], zoom_start=6,tiles="Stamen Terrain")

    choropleth= folium.Choropleth(
        geo_data=net_users,
        data=net_users,
        columns=('OBJECTID','% No Use'),
        key_on=('feature.properties.OBJECTID'),
        fill_color=('OrRd'),
        fill_opacity=0.8,
        nan_fill_opacity=0.4,
        line_opacity=0.5,
        name='Internet Users',
        show=True,
        overlay=True,
        legend_name=('INTERNET USERS'),
        highlight=True,
        nan_fill_color = "black",
        reset=True
    ).add_to(net_user)
    # Add hover functionality.
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    # Add dark and light mode. 
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(net_user)
    folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(net_user)

    # We add a layer controller. 
    folium.LayerControl(collapsed=False).add_to(net_user)
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['COUNTY','% Used','% No Use','Don`t know'], labels=True))
    net_user.save("templates/net_users")
    
    return render_template("net_users")

@routes.route("/map6")
def map6():
    #Mapping place of birth
    gdf_place_of_birth = gpd.read_file('gdf_place_of_birth.geojson')
    df_place_of_birth = round(gdf_place_of_birth, 2)
    df_place_of_birth.rename(columns={'size':'Total births','In a Health Facility':'% In a Health Facility','Non Health Facility':'% Non Health Facility','DK':'% Don`t know'}, inplace=True)

    place_of_birth=folium.Map([kc_latitude, kc_longitude], zoom_start=6,tiles="Stamen Terrain")

    choropleth= folium.Choropleth(
        geo_data=df_place_of_birth,
        data=df_place_of_birth,
        columns=('OBJECTID','% Non Health Facility'),
        key_on=('feature.properties.OBJECTID'),
        fill_color=('OrRd'),
        fill_opacity=0.8,
        nan_fill_opacity=0.4,
        line_opacity=0.5,
        name='Place of birth',
        show=True,
        overlay=True,
        legend_name=('Place of the last birth since 2014'),
        highlight=True,
        nan_fill_color = "black",
        reset=True
    ).add_to(place_of_birth)
    # Add hover functionality.
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    # Add dark and light mode. 
    folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(place_of_birth)
    folium.TileLayer('cartodbpositron',name="light mode",control=True).add_to(place_of_birth)

    # We add a layer controller. 
    folium.LayerControl(collapsed=False).add_to(place_of_birth)
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['COUNTY','Total births','% Non Health Facility','% In a Health Facility','% Don`t know'], labels=True))
    place_of_birth.save("templates/place_birth")
    
    return render_template("place_birth")
    