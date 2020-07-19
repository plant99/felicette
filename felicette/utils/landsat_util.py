import requests


def find_first_landsat(items):
    for index, item in enumerate(items):
        if "LC" in item._data["id"]:
            print(index)
            return item
        else:
            print(item)


def geocoder_util(city_name):
    # call nominatim api
    r = requests.get(
        "https://nominatim.openstreetmap.org/search?city={}&format=json".format(name)
    )
    r_json = r.json()
    # return lat, lon
    return (r_json[0]["lat"], r_json[0]["lon"])
