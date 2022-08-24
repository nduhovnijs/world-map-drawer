# world-map-drawer

Based on "https://www.udemy.com/course/the-python-mega-course/" excercise.
Create a world map with capitals pointed out and population volume color coded.

Set up environment & launch application
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python world_map_drawer.py map.html
```

Configuration is expected via environment variables or .env file. Example:
```
CAPITALS_FILEPATH = './resources/capitals.csv'
POPULATION_FILEPATH = './resources/population.json'
STARTING_POINT_LATITUDE = 56.9482
STARTING_POINT_LONGITUDE = 24.1546
LOG_LEVEL=DEBUG
```