from satsearch import Search
import sys
from rich import print as rprint
import logging
from felicette.utils.geo_utils import get_tiny_bbox
from felicette.utils.sys_utils import exit_cli
from felicette.constants import band_tag_map
from felicette.utils.file_manager import (
    save_to_file,
    data_file_exists,
    file_paths_wrt_id,
)
from felicette.utils.sys_utils import display_file

def handle_prompt_response(response):
    if response in ["n", "N"]:
        exit_cli(
            rprint,
            "Why not try a different location next time? I'd suggest [link=https://en.wikipedia.org/wiki/Svalbard]Svalbard[/link] :)"
        )
    elif response in ["y", "Y", ""]:
        return None
    else:
        exit_cli(rprint, "[red]Sorry, invalid response. Exiting :([/red]")

def handle_img_prompt_response(response_show_image,paths,key):
    if response_show_image in ["n", "N"]:
        return None
    elif response_show_image in ["y", "Y", ""]:
        display_file(paths[str(key)])
        return
    else:
        rprint("[red]Sorry, invalid response.([/red]")
        response_show_image = input(
        "Do you want to have a look at the downloaded preview image ? [Y/n]"
        )
        handle_img_prompt_response(response_show_image,paths,key)
        return

def search_landsat_data(coordinates, cloud_cover_lt):
    search = Search(
        bbox=get_tiny_bbox(coordinates),
        query={
            "eo:cloud_cover": {"lt": cloud_cover_lt},
            "collection": {"eq": "landsat-8-l1"},
        },
        sort=[{"field": "eo:cloud_cover", "direction": "asc"}],
    )

    # improvement: filter by date, cloud cover here

    search_items = search.items()
    print("Date at which picture was taken : " + str(search_items[0].date))
    if not len(search_items):
        exit_cli(print, "No data matched your search, please try different parameters.")
    landsat_item = search_items[0]
    return landsat_item


def preview_landsat_image(landsat_item):
    paths = file_paths_wrt_id(landsat_item._data["id"])
    # download image and save it in directory
    if not data_file_exists(paths["preview"]):
        save_to_file(
            landsat_item.assets["thumbnail"]["href"],
            paths["preview"],
            landsat_item._data["id"],
            "✗ preview data doesn't exist, downloading image",
        )
    else:
        rprint("[green] ✓ ", "required data exists for preview image")
    # print success info
    rprint("[blue]Preview image saved at:[/blue]")
    print(paths["preview"])
    logging.info("preview imagery !!!")
    response_show_image = input(
        "Do you want to have a look at the downloaded preview image ? [Y/n]"
    )
    handle_img_prompt_response(response_show_image,paths,"preview")
    # prompt a confirm option
    response = input(
        "Are you sure you want to see an enhanced version of the image at the path shown above? [Y/n]"
    )
    return handle_prompt_response(response)


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
