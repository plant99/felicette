import rasterio as rio
import numpy as np
from rio_color import operations, utils
from matplotlib import pyplot as plt
from PIL import Image
import PIL
import os

from felicette.utils.color import color
from felicette.utils.gdal_pansharpen import gdal_pansharpen
from felicette.utils.file_manager import file_paths_wrt_id

# increase PIL image processing pixels count limit 
PIL.Image.MAX_IMAGE_PIXELS = 933120000

count = 0

def process_landsat_image(id):
	global count
	count += 1
	if count > 1:
		return

	# get paths of files related to this id
	paths = file_paths_wrt_id(id)
	
	print("being called as parent function")

	# stack R,G,B bands

	# open files from the paths, and save it as stack
	b4 = rio.open(paths["b4"])
	b3 = rio.open(paths["b3"])
	b2 = rio.open(paths["b2"])

	# read as numpy ndarrays
	r = b4.read(1)
	g = b3.read(1)
	b = b2.read(1)

	with rio.open(paths["stack"],'w',driver='Gtiff', width=b4.width, height=b4.height, 
				  count=3,crs=b4.crs,transform=b4.transform, dtype=b4.dtypes[0], photometric="RGB") as rgb:
		rgb.write(r,1) 
		rgb.write(g,2) 
		rgb.write(b,3) 
		rgb.close()

	# pansharpen the image
	gdal_pansharpen(["", paths["b8"], paths["stack"], paths["pan_sharpened"]])

	# apply rio-color correction
	ops_string = "sigmoidal rgb 20 0.2"
	# refer to felicette.utils.color.py to see the parameters of this function
	# Bug: number of jobs if greater than 1, fails the job
	color(1, "uint16", paths["pan_sharpened"], paths["output_path"], ops_string.split(","), {"photometric":"RGB"})

	# save as jpeg image
	im = Image.open(paths["output_path"])
	im.save(paths["output_path_jpeg"], "JPEG", quality=100)
	print("saved as tiff and jpeg")




process_landsat_image("LC81390462020136")
