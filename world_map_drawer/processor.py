"""Build a map"""
from typing import Dict, List, NamedTuple
import pandas


class Capital(NamedTuple):
    """Info about Capital"""
    name: str
    latitude: float
    longitude: float


def parse_capitals(dataframe: pandas.DataFrame) -> List[Capital]:
    """Based on supplied Pandas dataframe, return list of Capitals"""
    # improved: use list comprehension
    return [
        Capital(
            name=capital["Capital"],
            latitude=capital["Latitude"],
            longitude=capital["Longitude"],
        ) for _, capital in dataframe.iterrows()]


def get_population_size_color(country_data) -> Dict[str, str]:
    """Based on country size, return corresponding color"""
    population = country_data['properties']['POP2005']

    population_volumes: Dict[int, str] = {
        5000000: 'cyan',
        10000000: 'blue',
        50000000: 'green',
        100000000: 'yellow',
        1000000000: 'orange',
    }
    # keys = (list(filter(lambda x: population < x,
    #                    sorted(population_volumes.keys()))))
    # color = 'red' if len(keys) == 0 else population_volumes[min(keys)]

    # Functional style implementation may be poorly readable if done
    # with native Python tools alone. Thus using imperative below instead.

    color = 'red'
    keys_sorted = sorted(population_volumes.keys())
    for population_threshold in keys_sorted:
        if population < population_threshold:
            color = population_volumes[population_threshold]
            break

    return {'fillColor': color}
