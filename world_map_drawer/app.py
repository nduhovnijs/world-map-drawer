""" Read corresponding CSV/JSON files and return a Folium map with capitals
marked and countries colored based on population volumes."""
import argparse
import logging
from typing import NamedTuple
import environs
import pandas
from world_map_drawer.folium_map_builder import build_world_map


class Config(NamedTuple):
    """App configuration"""
    capitals_filepath: str
    population_filepath: str
    output_map_filepath: str
    starting_point_latitude: float
    starting_point_longitude: float
    log_level: str


def __get_config(
        env: environs.Env, commandline_arguments: argparse.Namespace) -> Config:
    return Config(
        capitals_filepath=env.str("CAPITALS_FILEPATH"),
        population_filepath=env.str("POPULATION_FILEPATH"),
        output_map_filepath=commandline_arguments.OUTPUT_PATH,
        starting_point_latitude=env.float("STARTING_POINT_LATITUDE"),
        starting_point_longitude=env.float("STARTING_POINT_LONGITUDE"),
        log_level=env.str("LOG_LEVEL")
    )


def __get_commandline_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""Creates an HTML map with color-coded population
        volume and marked locations of capitals."""
    )
    parser.add_argument("OUTPUT_PATH", help="Output filepath")
    commandline_arguments = parser.parse_args()
    return commandline_arguments


def main():
    """Set up environment, invoke app, save map"""
    env = environs.Env()
    env.read_env()  # Read .env file if exists
    config = __get_config(env, __get_commandline_arguments())

    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s [%(levelname)s/%(threadName)s] %(message)s",
    )
    logging.debug("Configuration OK")

    population_geojson = open(
        config.population_filepath, 'r', encoding='utf-8-sig').read()

    world_map = build_world_map(
        pandas.read_csv(config.capitals_filepath),
        population_geojson,
        config.starting_point_latitude,
        config.starting_point_longitude)

    logging.info("Saving map")
    world_map.save(config.output_map_filepath)
