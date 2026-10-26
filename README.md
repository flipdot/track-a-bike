# Track a Bike

Collects data from Rent a Bike.

## Usage

    docker run --name track-a-bike --rm --restart=unless-stopped -v $HOME/track-a-bike/:/data flipdot/track-a-bike collect

The data will be saved to `$HOME/track-a-bike/xml/` and compressed every day.

The visualization scripts (`neo4j2plot.py`, `src/visualize/neo4j2dot.py`, `mark_transporters.py`) expect a Neo4j server at `bolt://localhost:7687`.

## Development

Dependencies are managed with [uv](https://docs.astral.sh/uv/):

    uv sync          # create .venv and install dependencies
    uv run python -m unittest discover -s tests -v   # smoke tests

## TODO

* Analyze data / create fancy graphs inside the docker image
* Synchronize data with another server / S3 Bucket
* Add command line options to track other cities, not just Kassel