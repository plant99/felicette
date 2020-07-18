import rasterio as rio
import numpy as np
from rio_color import operations, utils
from utils.file_manager import file_paths_wrt_id
from PIL import Image
import os

def process_landsat_image(id):
	# get paths of files related to this id
	paths = file_paths_wrt_id(id)

	# open files from the paths
	b4 = rio.open(paths["b4"])
	b3 = rio.open(paths["b3"])
	b2 = rio.open(paths["b2"])

	# read as numpy ndarrays
	r = b4.read(1)
	g = b3.read(1)
	b = b2.read(1)

	# downscale the arrays to range (0, 1)
	r = utils.to_math_type(r)
	g = utils.to_math_type(g)
	b = utils.to_math_type(b)

	# make rgb image for processing 
	img = np.array([r,g,b])

	# apply rio-color correction
	ops = "sigmoidal rgb 20 0.2"

	assert img.shape[0] == 3
	assert img.min() >= 0
	assert img.max() <= 1

	for func in operations.parse_operations(ops):
	    img = func(img)

	# after correction
	norm_r = utils.scale_dtype(img[0], np.uint16)
	norm_g = utils.scale_dtype(img[1], np.uint16)
	norm_b = utils.scale_dtype(img[2], np.uint16)

	with rio.open(paths["output_path"],'w',driver='Gtiff', width=b4.width, height=b4.height, 
	              count=3,crs=b4.crs,transform=b4.transform, dtype=np.uint16, photometric="RGB") as rgb:
	    rgb.write(norm_r.astype(np.uint16),1) 
	    rgb.write(norm_g.astype(np.uint16),2) 
	    rgb.write(norm_b.astype(np.uint16),3) 
	    rgb.close()


	im = Image.open(paths["output_path"])
	im.save(paths["output_path_jpeg"], "JPEG", quality=100)
	print("saved as tiff and jpeg")




process_landsat_image("LC81390462020136")
