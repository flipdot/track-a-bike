# Track a Bike

Collects data from Rent a Bike.

## Usage

    docker run --name track-a-bike --rm -v $HOME/track-a-bike/:/data flipdot/track-a-bike collect

The data will be saved to `$HOME/track-a-bike/xml/`

## TODO

* Analyze data / create fancy graphs inside the docker image
* Synchronize data with another server / S3 Bucket
* Add command line options to track other cities, not just Kassel