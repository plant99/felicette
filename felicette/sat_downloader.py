from satsearch import Search
import sys
from rich import print as rprint
import requests
import json

from felicette.utils.geo_utils import get_tiny_bbox
from felicette.utils.sys_utils import exit_cli
from felicette.constants import band_tag_map
from felicette.utils.file_manager import (
    save_to_file,
    data_file_exists,
    file_paths_wrt_id,
    get_product_type_from_id,
)


def handle_prompt_response(response):
    if response in ["n", "N"]:
        exit_cli(
            rprint,
            "Why not try a different location next time? I'd suggest [link=https://en.wikipedia.org/wiki/Svalbard]Svalbard[/link] :)",
        )
    elif response in ["y", "Y", ""]:
        return None
    else:
        exit_cli(rprint, "[red]Sorry, invalid response. Exiting :([/red]")


def search_satellite_data(coordinates, cloud_cover_lt, product="landsat"):
    """
    coordinates: bounding box's coordinates
    cloud_cover_lt: maximum cloud cover
    product: landsat, sentinel
    """
    if product == "landsat":
        product = "landsat-8-l1-c1"
    elif product == "sentinel":
        product = "sentinel-s2-l1c"

    search = Search(
        url="https://earth-search.aws.element84.com/v0",
        bbox=get_tiny_bbox(coordinates),
        query={
            "eo:cloud_cover": {"lt": cloud_cover_lt},
        },
        sort=[{"field": "eo:cloud_cover", "direction": "asc"}],
        collections=[product]
    )

    # improvement: filter by date, cloud cover here

    search_items = search.items()
    if not len(search_items):
        exit_cli(print, "No data matched your search, please try different parameters.")

    # return the first result
    item = search_items[0]
    return item


def preview_satellite_image(item):
    paths = file_paths_wrt_id(item._data["id"])
    # download image and save it in directory
    if not data_file_exists(paths["preview"]):
        save_to_file(
            item.assets["thumbnail"]["href"],
            paths["preview"],
            item._data["id"],
            "✗ preview data doesn't exist, downloading image",
        )
    else:
        rprint("[green] ✓ ", "required data exists for preview image")
    # print success info
    rprint("[blue]Preview image saved at:[/blue]")
    print(paths["preview"])
    # prompt a confirm option
    response = input(
        "Are you sure you want to see an enhanced version of the image at the path shown above? [Y/n]"
    )
    return handle_prompt_response(response)


def download_data(item, bands):
    product_type = get_product_type_from_id(item._data["id"])
    if product_type == "sentinel":
        return download_sentinel_data(item, bands)
    else:
        return download_landsat_data(item, bands)


def download_sentinel_data(item, bands):
    # get paths w.r.t. id
    paths = file_paths_wrt_id(item._data["id"])
    # get meta info on path, to be used by boto3
    info_response = requests.get(item.assets["info"]["href"])
    info_response_json = json.loads(info_response.text)
    # save bands generically
    for band in bands:
        # pass band id in metadata
        info_response_json["band_id"] = band
        band_filename = paths["b%s" % band]
        if not data_file_exists(band_filename):
            save_to_file(
                item.assets["B0{}".format(band)]["href"],
                band_filename,
                item._data["id"],
                "✗ required data doesn't exist, downloading %s %s"
                % (band_tag_map["b" + str(band)], "band"),
                meta=info_response_json,
            )
        else:
            rprint(
                "[green] ✓ ",
                "required data exists for {} band".format(
                    band_tag_map["b" + str(band)]
                ),
            )
    return item._data["id"]


def download_landsat_data(landsat_item, bands):

    # get paths w.r.t. id
    paths = file_paths_wrt_id(landsat_item._data["id"])
    # save bands generically
    for band in bands:
        band_filename = paths["b%s" % band]
        if not data_file_exists(band_filename):
            save_to_file(
                landsat_item.assets["B{}".format(band)]["href"],
                band_filename,
                landsat_item._data["id"],
                "✗ required data doesn't exist, downloading %s %s"
                % (band_tag_map["b" + str(band)], "band"),
            )
        else:
            rprint(
                "[green] ✓ ",
                "required data exists for {} band".format(
                    band_tag_map["b" + str(band)]
                ),
            )

    return landsat_item._data["id"]
