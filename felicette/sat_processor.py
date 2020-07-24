import rasterio as rio
import numpy as np
from rio_color import operations, utils
from PIL import Image
import PIL
from rich import print as rprint

from felicette.utils.color import color
from felicette.utils.gdal_pansharpen import gdal_pansharpen
from felicette.utils.file_manager import file_paths_wrt_id
from felicette.utils.image_processing_utils import process_sat_image
from felicette.utils.sys_utils import display_file

# increase PIL image processing pixels count limit
PIL.Image.MAX_IMAGE_PIXELS = 933120000


def process_landsat_vegetation(id, bands):

    # get paths of files related to this id
    paths = file_paths_wrt_id(id)

    # stack NIR, R, G bands

    # open files from the paths, and save it as stack
    b5 = rio.open(paths["b5"])
    b4 = rio.open(paths["b4"])
    b3 = rio.open(paths["b3"])

    # read as numpy ndarrays
    nir = b5.read(1)
    r = b4.read(1)
    g = b3.read(1)

    with rio.open(
        paths["stack"],
        "w",
        driver="Gtiff",
        width=b4.width,
        height=b4.height,
        count=3,
        crs=b4.crs,
        transform=b4.transform,
        dtype=b4.dtypes[0],
        photometric="RGB",
    ) as rgb:
        rgb.write(nir, 1)
        rgb.write(r, 2)
        rgb.write(g, 3)
        rgb.close()

    source_path_for_rio_color = paths["stack"]

    rprint("Let's make our 🌍 imagery a bit more colorful for a human eye!")
    # apply rio-color correction
    ops_string = "sigmoidal rgb 20 0.2"
    # refer to felicette.utils.color.py to see the parameters of this function
    # Bug: number of jobs if greater than 1, fails the job
    color(
        1,
        "uint16",
        source_path_for_rio_color,
        paths["vegetation_path"],
        ops_string.split(","),
        {"photometric": "RGB"},
    )

    # resize and save as jpeg image
    print("Generated 🌍 images!🎉")
    rprint("[yellow]Please wait while I resize and crop the image :) [/yellow]")
    process_sat_image(paths["vegetation_path"], paths["vegetation_path_jpeg"])
    rprint("[blue]GeoTIFF saved at:[/blue]")
    print(paths["vegetation_path"])
    rprint("[blue]JPEG image saved at:[/blue]")
    print(paths["vegetation_path_jpeg"])
    # display generated image
    display_file(paths["vegetation_path_jpeg"])


def process_landsat_rgb(id, bands):
    # get paths of files related to this id
    paths = file_paths_wrt_id(id)

    # stack R,G,B bands

    # open files from the paths, and save it as stack
    b4 = rio.open(paths["b4"])
    b3 = rio.open(paths["b3"])
    b2 = rio.open(paths["b2"])

    # read as numpy ndarrays
    r = b4.read(1)
    g = b3.read(1)
    b = b2.read(1)

    with rio.open(
        paths["stack"],
        "w",
        driver="Gtiff",
        width=b4.width,
        height=b4.height,
        count=3,
        crs=b4.crs,
        transform=b4.transform,
        dtype=b4.dtypes[0],
        photometric="RGB",
    ) as rgb:
        rgb.write(r, 1)
        rgb.write(g, 2)
        rgb.write(b, 3)
        rgb.close()

    source_path_for_rio_color = paths["stack"]

    # check if band 8, i.e panchromatic band has to be processed
    if 8 in bands:
        # pansharpen the image
        rprint(
            "Pansharpening image, get ready for some serious resolution enhancement! ✨"
        )
        gdal_pansharpen(["", paths["b8"], paths["stack"], paths["pan_sharpened"]])
        # set color operation's path to the pansharpened-image's path
        source_path_for_rio_color = paths["pan_sharpened"]

    rprint("Let's make our 🌍 imagery a bit more colorful for a human eye!")
    # apply rio-color correction
    ops_string = "sigmoidal rgb 20 0.2"
    # refer to felicette.utils.color.py to see the parameters of this function
    # Bug: number of jobs if greater than 1, fails the job
    color(
        1,
        "uint16",
        source_path_for_rio_color,
        paths["output_path"],
        ops_string.split(","),
        {"photometric": "RGB"},
    )

    # resize and save as jpeg image
    print("Generated 🌍 images!🎉")
    rprint("[yellow]Please wait while I resize and crop the image :) [/yellow]")
    process_sat_image(paths["output_path"], paths["output_path_jpeg"])
    rprint("[blue]GeoTIFF saved at:[/blue]")
    print(paths["output_path"])
    rprint("[blue]JPEG image saved at:[/blue]")
    print(paths["output_path_jpeg"])
    # display generated image
    display_file(paths["output_path_jpeg"])

def process_landsat_data(id, bands):

    if bands == [2, 3, 4] or bands == [2, 3, 4, 8]:
        process_landsat_rgb(id, bands)
    elif bands == [3, 4, 5]:
        process_landsat_vegetation(id, bands)
