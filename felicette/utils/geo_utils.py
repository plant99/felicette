import requests


def find_first_landsat(items):
    for index, item in enumerate(items):
        if "LC" in item._data["id"]:
            return item


def geocoder_util(location_name):
    # call nominatim api
    r = requests.get(
        "https://nominatim.openstreetmap.org/search?city={}&format=json".format(
            location_name
        )
    )
    r_json = r.json()
    # return lat, lon
    return (float(r_json[0]["lon"]), float(r_json[0]["lat"]))


def get_tiny_bbox(coordinates):
    lon, lat = coordinates
    return [lon, lat, lon + 0.00001, lat + 0.00001]
