"""Build a map"""
from typing import Dict, List, NamedTuple
import pandas
import folium


class __Capital(NamedTuple):
    name: str
    latitude: float
    longitude: float


def __parse_capitals(dataframe: pandas.DataFrame) -> List[__Capital]:
    # improved: use list comprehension
    return [
        __Capital(
            name=capital["Capital"],
            latitude=capital["Latitude"],
            longitude=capital["Longitude"],
        ) for _, capital in dataframe.iterrows()]


def __get_capitals_map(capitals: List[__Capital]) -> folium.FeatureGroup:
    # improved: use named parameter
    popup_text_template = '<a href = "https://en.wikipedia.org/wiki/Special: Search/{city_name}" target = "_blank">{city_name}</a>'

    capitals_layer = folium.FeatureGroup(name="Capitals")
    for capital in capitals:
        capitals_layer.add_child(folium.Marker(
            location=[capital.latitude, capital.longitude], popup=popup_text_template.format(
                city_name=capital.name)))

    return capitals_layer


def __get_population_layer(population_geojson: str) -> folium.FeatureGroup:
    # improved: moved __population_size_color inside __get_population_layer
    def __population_size_color(country_data) -> Dict[str, str]:
        population = country_data['properties']['POP2005']

        population_volumes: Dict[int, str] = {
            1000000: 'grey',
            5000000: 'blue',
            10000000: 'green',
            100000000: 'yellow',
            1000000000: 'orange',
        }

        color = 'red'  # default color, for largest countries

        # improved: previous implmentation likely didn't work due to lack of guarantees in dict key order
        keys_sorted = sorted(population_volumes.keys())
        for population_threshold in keys_sorted:
            if population < population_threshold:
                color = population_volumes[population_threshold]
                break

        return {'fillColor': color}

    population_layer = folium.FeatureGroup(name="Population")

    population_layer.add_child(folium.GeoJson(
        data=population_geojson,
        style_function=__population_size_color))

    return population_layer


def get_world_map(dataframe, population_geojson, start_latitude, start_longitude, logger):
    """Build a map"""
    world_map = folium.Map(
        location=[start_latitude,
                  start_longitude],
        zoom_start=5, tiles="Stamen Terrain")

    # improved: moved "add child" to corresponding data preparations
    capitals: List[__Capital] = __parse_capitals(dataframe)
    capitals_layer = __get_capitals_map(capitals)
    world_map.add_child(capitals_layer)
    logger.debug("Added Capitals layer")

    population_layer = __get_population_layer(population_geojson)
    world_map.add_child(population_layer)
    logger.debug("Added population layer")

    world_map.add_child(folium.LayerControl())
    logger.debug("Added layer control")

    return world_map
