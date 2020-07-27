## Setup

To create a development setup of felicette, follow these steps

### Prerequisites

 - Make a fork of this repository
 - `cd` into your working directory, this will hereon be referenced as `$WORK_DIR`
 - Clone from `https://github.com/<your username>/felicette`
 - Add `$WORK_DIR/felicette` to `$PYTHONPATH` as documented [here](https://stackoverflow.com/a/3402176)
 - Setup felicette's dependencies in the following manner
#### Ubuntu/Debian 
```
$ sudo add-apt-repository ppa:ubuntugis/ppa
$ sudo apt-get update
$ sudo apt-get install python-numpy gdal-bin libgdal-dev
$ gdal-config --version
 <version-number>
 
* activate virtual environment *

$ pip install numpy GDAL==<version-number>
```

#### MacOS
```
$ brew install gdal
$ gdal-config --version
 <version-number>

* activate virtual environment *

$ pip install numpy GDAL==<version-number>
```

 - Test installation by doing `python felicette/cli.py --help`
 - Pick an issue
    - Issues with labels `low-hanging-fruit`, `good-first-issue` are easier to get started with
    - If you need help picking one, please send an email to shivashispadhi(at)gmail(dot)com
 - Make desired changes
 - Format the code using [`black`](https://github.com/psf/black)
 - Push the updated code to your fork
 - Make a PR to `develop` branch, and ask any active contributor for a review.

## Bookkeeping
* The product roadmap is documented [here](https://github.com/plant99/felicette/wiki/Product-Roadmap)
* If you want to work on a feature which isn't in `issues` section, feel free to raise one and assign to yourself before starting to work on it.
* Active issues being worked on are tracked [here](https://github.com/plant99/felicette/projects/1), once you plan to work on one, please update here as well to track the status.
* Until the next release, all the new changes go to `develop` branch.

Humongous thanks, for considering to contribute to `felicette`!
