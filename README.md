
# felicette

Satellite imagery for dummies.

### Who should use this tool?

TL;DR: Generate JPEG earth imagery from coordinates/location name

This tool is for a sentient being who wants to view high-res satellite imagery of earth, without digging through all the nitty gritty geospatial details of it. So if this is your first time trying to explore how parts of the Earth looks from space, you're at the right place.

NB: `felicette` at the present state searches for cloud-cover < 10%, and doesn't constrain results on the basis of dates. 

### Installation

`felicette` depends on GDAL. But the following steps cover GDAL's installation as well.

#### Debian 
```
$ sudo add-apt-repository ppa:ubuntugis/ppa
$ sudo apt-get update
$ sudo apt-get install python-numpy gdal-bin libgdal-dev
$ gdal-config --version
 <version-number>
 
* activate virtual environment *

$ pip install GDAL==<version-number>
$ pip install felicette

```

#### MacOS
```
$ brew install gdal
$ gdal-config --version
 <version-number>

* activate virtual environment *

$ pip install GDAL==<version-number>
$ pip install felicette
```

#### "Why you no make a section for Windows?" :|

`rio-color`, one of the felicette's dependencies isn't available on conda ecosystem yet. [Here's](https://github.com/mapbox/rio-color/issues/58#issuecomment-406466990) the link to a small discussion on an installation-issue. This section would be updated when there is a stable version of `felicette` for Windows.

Felicette has plans to build in-house RGB image enhancement algorithms or use [imagemagick](https://imagemagick.org/script/command-line-processing.php) /\[similar tools on conda-forge] for a Windows release, at least until `rio-color` is available on conda-forge/conda.

-------------------------

### Usage

To use it:

    $ felicette --help

```
Usage: felicette [OPTIONS]

  Satellite imagery for dummies.

Options:
  -c, --coordinates FLOAT...  Coordinates in (lon, lat) format. This overrides
                              -l command

  -l, --location-name TEXT    Location name in string format
  -p, --pan-enhancement       Enhance image with panchromatic band
  -pre, --preview-image       Preview pre-processed low resolution RGB
                              satellite image.

  -v, --vegetation            Show Color Infrared image to highlight
                              vegetation

  --help                      Show this message and exit.

```

Felicette can download and process Landsat images taking the location's input as `(lon, lat)` or the location name. They can be used in the following way.

With location name:

    $ felicette -l "Svalbard"

With coordinates:

    $ felicette -c 20.9752 77.8750

`-p` option uses the panchromatic band to enhance image's resolution to 15 meters, contrary to resolution of RGB bands(30 meters). 
To get a better image using felicette use:

    $ felicette -p -c 20.9752 77.8750

`-pre` option downloads a low-res image for preview, to check if the image is worth your computation, Network I/O. :)

    $ felicette -pre -p -c 20.9752 77.8750
  
`-v` option generates a [CIR](https://eos.com/color-infrared/) image to highlight vegetation in 'red' color. Note that, '-p' option isn't taken into consideration while generating CIR imagery in felicette.

    $ felicette -pre -v -l "Svalbard"
  

-------------------------
### Feli.. what?

![Félicette](https://i.imgur.com/q4G5ThZ.jpg)


Félicette was the first cat launched into space, on 18 October 1963. Even though she landed back on earth safely, Félicette was euthanized two months after the launch so that scientists could perform a necropsy to examine her brain. She was the only cat to have survived spaceflight. [Here's](https://www.youtube.com/watch?v=v-tpmvGRoyw) a footage of the mission from the archives.

When you get a satellite imagery using this tool, imagine Félicette took the picture for you :)) 

-------------------------
### Preview and examples
[Here](
https://drive.google.com/drive/folders/1QxJUaCt_MDE7LAdh9znTP7796JXAHKhU?usp=sharing) is a link to the images generated with RGB, CIR options.

Following is a recording of the terminal session recording usage of `felicette`.
[![asciicast](https://asciinema.org/a/IoiUnkJ1IcXtsj81hjrmSpZi5.png)](https://asciinema.org/a/IoiUnkJ1IcXtsj81hjrmSpZi5)