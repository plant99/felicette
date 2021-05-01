# felicette

Satellite imagery for dummies.

### What can you do with this tool?

**TL;DR**: Generate JPEG earth imagery from coordinates/location name with publicly available satellite data.

This tool is for a sentient being who wants to view high-res satellite imagery of earth, without digging through all the nitty gritty geospatial details of it. So if this is your first time trying to explore how parts of the Earth look from space, you're at the right place.

NB: `felicette` at the present state searches for cloud-cover < 10%, and doesn't constrain results on the basis of dates. 

One can see [Product Roadmap](https://github.com/plant99/felicette/wiki/Product-Roadmap) for upcoming features.

### Installation

`felicette` depends on [GDAL](https://gdal.org/). But the following steps cover GDAL's installation as well.

`rio-color` uses numpy headers to setup, thus installing numpy and GDAL=={ogrinfo --version} would be sufficient before installing felicette.

#### Debian 
```
$ sudo add-apt-repository ppa:ubuntugis/ppa
$ sudo apt-get update
$ sudo apt-get install python-numpy gdal-bin libgdal-dev
$ gdal-config --version
 <version-number>
 
* activate virtual environment *

$ pip install numpy GDAL==<version-number>
$ pip install felicette

```

#### MacOS
```
$ brew install gdal
$ gdal-config --version
 <version-number>

* activate virtual environment *

$ pip install numpy GDAL==<version-number>
$ pip install felicette
```

#### Docker

As pointed out [here](https://news.ycombinator.com/item?id=23951167), the following docker image works and is volume-mapped to the present working directory. 

    $ docker run -it -v "$PWD"/felicette-data:/root/felicette-data milhouse1337/felicette felicette -l "Montreal"

Thanks [@milhouse1337](https://hub.docker.com/u/milhouse1337) for the docker-image.

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
  -pan, --pan-enhancement     Enhance image with panchromatic band
  --no-preview                Skip previewing of pre-processed low resolution RGB
                              satellite image.

  -v, --vegetation            Show Color Infrared image to highlight
                              vegetation

  -V, --version               Show the version number and quit
  -p, --product TEXT          Product name 'landsat'/'sentinel'
  --help                      Show this message and exit.
```

Felicette can download and process Landsat images taking the location's input as `(lon, lat)` or the location name. They can be used in the following way.

With location name:

    $ felicette -l "Kanyakumari"

With coordinates:

    $ felicette -c 77.5385 8.0883

`--product` / `-p` option is used to specify which data-product is used to generate images i.e Sentinel or Landsat. By default, Landsat-8 data will be used to generate images.

    $ felicette -l "Kanyakumari" -p "sentinel"

**NB**: *To use sentinel data source, one has to set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (To generate a pair, go to AWS console -> My Security Credentials -> Access keys). This is because [Sentinel-2 data](https://registry.opendata.aws/sentinel-2/) is in a [Requester Pays](https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html) bucket.


`-pan` option uses the panchromatic band to enhance image's resolution to 15 meters, contrary to resolution of RGB bands(30 meters) if Landsat product is being used. Felicette doesn't support any panchromatic enhancements for Sentinel-2 data which already have a resolution of 10m.
To get a better Landsat image using felicette use:

    $ felicette -pan -c 77.5385 8.0883

`--no-preview` option doesn't download image to preview, and directly downloads and processes original data. Please use this if you're sure of the location/quality of the images to be generated by felicette with the arguments provided to it.

    $ felicette --no-preview -p -c 77.5385 8.0883
  
`-v` option generates a [CIR](https://eos.com/color-infrared/) image to highlight vegetation in 'red' color. Note that, '-p' option isn't taken into consideration while generating CIR imagery in felicette.

    $ felicette  -v -l "Kanyakumari"

-------------------------
### Latest release

[0.1.13](https://github.com/plant99/felicette/releases/tag/0.1.13)
  

-------------------------
### Feli.. what?

![Félicette](https://i.imgur.com/q4G5ThZ.jpg)


Félicette was the first cat launched into space, on 18 October 1963. Even though she landed back on earth safely, Félicette was euthanized two months after the launch so that scientists could perform a necropsy to examine her brain. She was the only cat to have survived spaceflight. [Here's](https://www.youtube.com/watch?v=v-tpmvGRoyw) a footage of the mission from the archives.

When you get a satellite imagery using this tool, imagine Félicette took the picture for you :)) 

-------------------------
### Preview and examples

![Coastal Odisha](https://i.imgur.com/BaquOGJ.jpg)

[Here](https://github.com/plant99/felicette/wiki/Sample-images-generated-by-felicette) are some more sample images generated by felicette.

[Here](
https://drive.google.com/drive/folders/1QxJUaCt_MDE7LAdh9znTP7796JXAHKhU?usp=sharing) is a link to the original images generated with RGB, CIR options.

Following is a recording of the terminal session recording usage of `felicette`.
[![asciicast](https://asciinema.org/a/349495.png)](https://asciinema.org/a/349495)

-------------------------
### Contributing

`felicette` is open-source and welcomes all kinds of contributions, be it documentation/wiki pages/bug-fixes/development of new features.
A small contributors' guide is available [here](https://github.com/plant99/felicette/wiki/Contributors-Guide). 
