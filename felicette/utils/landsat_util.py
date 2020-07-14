def find_first_landsat(items):
	for index, item in enumerate(items):
		if "LC" in item._data["id"]:
			print(index)
			return item
		else:
			print(item)