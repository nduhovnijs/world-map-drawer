"""Build a map"""
from typing import Dict, List, NamedTuple
import pandas
import folium


class __Capital(NamedTuple):
    name: str
    latitude: float
    longitude: float


def __parse_capitals(dataframe: pandas.DataFrame) -> List[__Capital]:
    capitals: List[__Capital] = []
    for _, capital in dataframe.iterrows():
        capitals.append(__Capital(
            name=capital["Capital"],
            latitude=capital["Latitude"],
            longitude=capital["Longitude"],
        ))
    return capitals


def __get_capitals_map(capitals: List[__Capital]) -> folium.FeatureGroup:
    popup_text_template = '<a href = "https://en.wikipedia.org/wiki/Special: Search/{}" target = "_blank">{}</a>'

    capitals_layer = folium.FeatureGroup(name="Capitals")
    for capital in capitals:
        capitals_layer.add_child(folium.Marker(
            location=[capital.latitude, capital.longitude], popup=popup_text_template.format(
                capital.name, capital.name)))

    return capitals_layer


def __population_size_color(country_data) -> Dict[str, str]:
    population = country_data['properties']['POP2005']

    population_volumes = {
        1000000: 'grey',
        5000000: 'blue',
        10000000: 'green',
        100000000: 'yellow',
        1000000000: 'orange',
    }

    color = 'red'  # default color, for largest countries
    for population_threshold, threshold_color in population_volumes.items():
        if population < population_threshold:
            color = threshold_color
            break

    return {'fillColor': color}


def __get_population_layer(population_geojson: str) -> folium.FeatureGroup:
    population_layer = folium.FeatureGroup(name="Population")

    population_layer.add_child(folium.GeoJson(
        data=population_geojson,
        style_function=__population_size_color))

    return population_layer


def get_world_map(config, logger):
    """Build a map"""
    dataframe = pandas.read_csv(config.capitals_filepath)
    world_map = folium.Map(
        location=[config.starting_point_latitude,
                  config.starting_point_longitude],
        zoom_start=5, tiles="Stamen Terrain")

    capitals: List[__Capital] = __parse_capitals(dataframe)
    capitals_layer = __get_capitals_map(capitals)
    logger.debug("Prepared Capitals layer")

    population_geojson = open(
        config.population_filepath, 'r', encoding='utf-8-sig').read()
    population_layer = __get_population_layer(population_geojson)
    logger.debug("Prepared population layer")

    world_map.add_child(capitals_layer)
    world_map.add_child(population_layer)
    world_map.add_child(folium.LayerControl())

    return world_map
