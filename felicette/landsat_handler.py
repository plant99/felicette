from satsearch import Search
from felicette.utils.get_wrs import get_tiny_bbox
from felicette.utils.file_manager import save_to_file, data_file_exists

search = Search(
    bbox=get_tiny_bbox(85.8245, 20.2961),
    query={"eo:cloud_cover": {"lt": 10}, "collection": {"eq": "landsat-8-l1"}},
)
landsat_item = search.items()[0]


# save bands generically
bands = [2,3,4]
for band in bands:
    band_filename = landsat_item._data["id"] + "-b{}.tiff".format(band)
    if not data_file_exists(band_filename):
        save_to_file(landsat_item.assets["B{}".format(band)]["href"], band_filename)
    else:
        print("required data exists for {}".format(band_filename))
