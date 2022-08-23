""" Read corresponding CSV/JSON files and return a Folium map with capitals 
marked and countries colored based on population volumes."""
import argparse
import logging
from typing import NamedTuple
import folium
import environs
import pandas
from world_map_drawer.processor import get_world_map


class __Config(NamedTuple):
    capitals_filepath: str
    population_filepath: str
    output_map_filepath: str
    starting_point_latitude: float
    starting_point_longitude: float
    log_level: str


def __get_config(
    env: environs.Env, commandline_arguments: argparse.Namespace
) -> __Config:
    return __Config(
        capitals_filepath=env.str("CAPITALS_FILEPATH"),
        population_filepath=env.str("POPULATION_FILEPATH"),
        output_map_filepath=commandline_arguments.OUTPUT_PATH,
        starting_point_latitude=env.float("STARTING_POINT_LATITUDE"),
        starting_point_longitude=env.float("STARTING_POINT_LONGITUDE"),
        log_level=env.str("LOG_LEVEL")
    )


def __save_map(world_map: folium.Map, path: str) -> None:
    world_map.save(path)


def __get_commandline_arguments():
    parser = argparse.ArgumentParser(
        description="""Creates an HTML map with color-coded population
        volume and marked locations of capitals."""
    )
    parser.add_argument("OUTPUT_PATH", help="Output filepath")
    commandline_arguments = parser.parse_args()
    return commandline_arguments


def main():
    """Set up environment, invoke processor, save map"""
    env = environs.Env()
    env.read_env()  # Read .env file if exists
    commandline_arguments = __get_commandline_arguments()
    config = __get_config(env, commandline_arguments)

    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s [%(levelname)s/%(threadName)s] %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.debug("Configuration OK")

    dataframe = pandas.read_csv(config.capitals_filepath)
    population_geojson = open(
        config.population_filepath, 'r', encoding='utf-8-sig').read()
    world_map = get_world_map(dataframe, population_geojson,
                              config.starting_point_latitude, config.starting_point_longitude, logger)

    logger.info("Saving map")
    __save_map(world_map, config.output_map_filepath)
