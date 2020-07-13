from satsearch import Search
from felicette.utils.get_wrs import get_tiny_bbox
search = Search(bbox=get_tiny_bbox(85.8245, 20.2961), collection="landsat-8-11")
print('bbox search: %s items' % search.found())
items = search.items()

for index, item in enumerate(items):
	print(item.assets)
	if index == 6:
		break
# print(items._items)

# print(items.summary())