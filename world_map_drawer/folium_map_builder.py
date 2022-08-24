"""Build a map using Foliums"""
from typing import List
import logging
import folium
import pandas
from world_map_drawer.processor import Capital, parse_capitals, get_population_size_color


def __get_capitals_map(capitals: List[Capital]) -> folium.FeatureGroup:
    popup_text_template = """<a href = "https://en.wikipedia.org/wiki/Special: Search/{city_name}"
    target = "_blank">{city_name}</a>"""

    capitals_layer = folium.FeatureGroup(name="Capitals")
    for capital in capitals:
        capitals_layer.add_child(folium.Marker(
            location=[capital.latitude, capital.longitude], popup=popup_text_template.format(
                city_name=capital.name)))

    return capitals_layer


def __get_population_layer(population_geojson: str) -> folium.FeatureGroup:
    population_layer = folium.FeatureGroup(name="Population")

    population_layer.add_child(folium.GeoJson(
        data=population_geojson,
        style_function=get_population_size_color))

    return population_layer


def build_world_map(
        dataframe: pandas.DataFrame, population_geojson: str,
        start_latitude: float, start_longitude: float) -> folium.Map:
    """Build a map"""
    world_map = folium.Map(
        location=[start_latitude,
                  start_longitude],
        zoom_start=5, tiles="Stamen Terrain")

    # improved: moved "add child" to corresponding data preparations
    capitals: List[Capital] = parse_capitals(dataframe)
    capitals_layer = __get_capitals_map(capitals)
    world_map.add_child(capitals_layer)
    logging.debug("Added Capitals layer")

    population_layer = __get_population_layer(population_geojson)
    world_map.add_child(population_layer)
    logging.debug("Added population layer")

    world_map.add_child(folium.LayerControl())
    logging.debug("Added layer control")

    return world_map
