from satsearch import Search
import sys
from rich import print

from felicette.utils.geo_utils import get_tiny_bbox
from felicette.constants import band_tag_map
from felicette.utils.file_manager import save_to_file, data_file_exists, check_sat_path

def search_landsat_data(coordinates, cloud_cover_lt):
    search = Search(
        bbox=get_tiny_bbox(coordinates),
        query={
            "eo:cloud_cover": {"lt": cloud_cover_lt},
            "collection": {"eq": "landsat-8-l1"},
        },
    )
    # improvement: filter by date, cloud cover here

    search_items = search.items()
    if not len(search_items):
        print("No data matched your search, please try different parameters.")
        sys.exit(0)
    landsat_item = search_items[0]
    return landsat_item

def download_landsat_data(
    coordinates=(85.8245, 20.2961), cloud_cover_lt=10, bands=[2, 3, 4, 8]
):
    landsat_item = search_landsat_data(coordinates, cloud_cover_lt)
    # check if directory exists to save the data for this product id
    check_sat_path(landsat_item._data["id"])

    # save bands generically
    for band in bands:
        band_filename = landsat_item._data["id"] + "-b{}.tiff".format(band)
        if not data_file_exists(band_filename, landsat_item._data["id"]):
            save_to_file(landsat_item.assets["B{}".format(band)]["href"], band_filename, landsat_item._data["id"])
        else:
            print("[green] ✓ ", "required data exists for {} band".format(band_tag_map["b"+str(band)]))

    return landsat_item._data["id"]


if __name__ == "__main__":
    download_landsat_data()
