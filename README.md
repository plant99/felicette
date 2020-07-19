
# felicette

Satellite imagery for dummies.


# Installation

It's as simple as

    $ pip install felicette


# Usage

To use it:

    $ felicette --help

```
Usage: felicette [OPTIONS]

Satellite imagery for dummies.

Options:

-c, --coordinates FLOAT...  Coordinates in (lon, lat) format. This overrides

-l command

  

-l, --location-name TEXT  Location name in string format

-p, --pan-enhancement Enhance image with panchromatic band

--help  Show this message and exit.

```

Felicette can download and process Landsat images taking the location's input as `(lon, lat)` or the location name. They can be used in the following way.

With location name:

	$ felicette -l "Taal Volcano"

With coordinates:

	$ felicette -c 120.9977 14.0113

`-p` option uses the panchromatic band to enhance image's resolution to 15 meters, contrary to resolution of RGB bands(30 meters). 
To get a better image using felicette use:

	$ felicette -p -c 120.9977 14.0113

# What's in the name?


![Félicette](https://i.imgur.com/q4G5ThZ.jpg)


Félicette was the first cat launched into space, on 18 October 1963. Even though she landed back on earth safely, but she was humanely killed after 2 months to save her from a bad health, and scientific research. [Here's](https://www.youtube.com/watch?v=v-tpmvGRoyw) a footage of the mission from the archives.

When you get a satellite imagery using this tool, imagine Félicette took the picture for you :)) 
