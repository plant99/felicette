import click
import sys
from rasterio.errors import RasterioIOError

from felicette.utils.geo_utils import geocoder_util
from felicette.utils.file_manager import check_sat_path, file_paths_wrt_id
from felicette.sat_downloader import (
    download_landsat_data,
    search_landsat_data,
    preview_landsat_image,
)
from felicette.utils.sys_utils import exit_cli, remove_dir
from felicette.sat_processor import process_landsat_data

def trigger_download_and_processing(landsat_item, bands):
    # download data
    data_id = download_landsat_data(landsat_item, bands)
    # process data
    process_landsat_data(data_id, bands)

@click.command()
@click.option(
    "-c",
    "--coordinates",
    nargs=2,
    type=float,
    help="Coordinates in (lon, lat) format. This overrides -l command",
)
@click.option("-l", "--location-name", type=str, help="Location name in string format")
@click.option(
    "-p",
    "--pan-enhancement",
    default=False,
    is_flag=True,
    help="Enhance image with panchromatic band",
)
@click.option(
    "--no-preview",
    default=False,
    is_flag=True,
    help="Preview pre-processed low resolution RGB satellite image.",
)
@click.option(
    "-v",
    "--vegetation",
    default=False,
    is_flag=True,
    help="Show Color Infrared image to highlight vegetation",
)
def main(coordinates, location_name, pan_enhancement, no_preview, vegetation):
    """Satellite imagery for dummies."""
    if not coordinates and not location_name:
        exit_cli(print, "Please specify either --coordinates or --location-name")
    if location_name:
        coordinates = geocoder_util(location_name)

    # unless specified, cloud_cover_lt is 10
    landsat_item = search_landsat_data(coordinates, 10)

    # check if directory exists to save the data for this product id
    check_sat_path(landsat_item._data["id"])

    # if preview option is set, download and preview image
    if not no_preview:
        preview_landsat_image(landsat_item)

    # set bands to process
    bands = [2, 3, 4]
    if pan_enhancement:
        bands.append(8)

    if vegetation:
        bands = [3, 4, 5]

    # NB: can't enable pan-enhancement with vegetation

    try:
        trigger_download_and_processing(landsat_item, bands)
    except RasterioIOError:
        response = input("Local data for this location is corrupted, felicette will remove existing data to proceed, are you sure? [Y/n]")
        if response in ["y", "Y", ""]:
            # remove file dir
            file_paths = file_paths_wrt_id(landsat_item._data["id"])
            remove_dir(file_paths["base"])
            # retry downloading and processing image with a clean directory
            trigger_download_and_processing(landsat_item, bands)
        elif response in ["n", "N"]:
            exit_cli(print, "")



if __name__ == "__main__":
    main()
