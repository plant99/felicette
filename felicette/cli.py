import click
import sys

from felicette.utils.geo_utils import geocoder_util
from felicette.sat_downloader import download_landsat_data
from felicette.sat_processor import process_landsat_data


@click.command()
@click.option('-c', '--coordinates', nargs=2, type=float, help="Coordinates in (lon, lat) format. This overrides -l command")
@click.option('-l', '--location-name', type=str, help="Location name in string format")
def main(coordinates, location_name):
	"""Satellite imagery for dummies."""
	if not coordinates and not location_name:
		click.echo("Please specify either --coordinates or --location-name")
		sys.exit(1)
	if location_name:
		coordinates = geocoder_util(location_name)

	# download data
	data_id = download_landsat_data(coordinates)
	# process data
	process_landsat_data(data_id)



if __name__ == "__main__":
	main()
