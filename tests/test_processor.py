"""
Test processor
"""

import unittest
import pandas

from world_map_drawer.processor import parse_capitals, get_population_size_color, Capital


class TestProcessor(unittest.TestCase):
    """Test business logic/data tranformations"""

    def test_parse_capitals(self) -> None:
        """Test parse_capitals"""
        expected_capitals = [
            Capital(name='Riga', latitude=56.949649, longitude=24.105186),
            Capital(name='Vilnius', latitude=54.687156, longitude=25.279651),
            Capital(name='Luxembourg', latitude=49.611621, longitude=6.131935)
        ]

        dataframe = pandas.read_csv("./tests/test_resources/capitals.csv")
        capitals = parse_capitals(dataframe)
        self.assertEqual(expected_capitals, capitals)

    def test_get_population_size_color(self) -> None:
        """Test get_population_size_color"""
        arguments_and_expectations = {
            1000000: 'cyan',
            6000000: 'blue',
            20000000: 'green',
            90000000: 'yellow',
            500000000: 'orange',
            2000000000: 'red',
        }

        for argument, expectation in arguments_and_expectations.items():
            self.assertEqual(get_population_size_color(
                country_data={'properties': {'POP2005': argument}}), {'fillColor': expectation})


if __name__ == "__main__":
    unittest.main()
