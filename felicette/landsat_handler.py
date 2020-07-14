from satsearch import Search
from felicette.utils.get_wrs import get_tiny_bbox

search = Search(bbox=get_tiny_bbox(85.8245, 20.2961), query = {
  "eo:cloud_cover": {
    "lt": 10
  },
  "collection": {
    "eq": "landsat-8-l1"
  }
})
landsat_item = search.items()[0]
print(landsat_item.assets)