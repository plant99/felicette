import tempfile
import os
import requests
from tqdm import tqdm
from rich import print as rprint
import boto3

from felicette.constants import band_tag_map
from felicette.utils.sys_utils import exit_cli

workdir = os.path.join(os.path.expanduser("~"), "felicette-data")


def check_sat_path(id):
    data_path = os.path.join(workdir, id)

    if not os.path.exists(data_path):
        os.makedirs(data_path, exist_ok=True)


def hook(t):
    def inner(bytes_amount):
        t.update(bytes_amount)

    return inner


def save_to_file(url, filename, id, info_message, meta=None):
    product_type = get_product_type_from_id(id)
    data_path = os.path.join(workdir, id)
    data_id = filename.split("/")[-1].split("-")[1].split(".")[0]
    rprint(info_message)
    file_path = os.path.join(data_path, filename)

    if product_type == "sentinel" and meta:
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", None)
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", None)
        # if access key or secret isn't defined, print error message and exit
        if (not aws_access_key_id) or (not aws_secret_access_key):
            exit_cli(rprint, "Error: [red]AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY[/red] must be set in environment variables to access Sentinel data.")
        # prepare boto3 client
        s3_client = boto3.Session().client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        band = os.path.join(meta["path"], "B0%s.jp2" % (meta["band_id"]))
        filesize = s3_client.head_object(
            Bucket="sentinel-s2-l1c", Key=band, RequestPayer="requester"
        ).get("ContentLength")
        with tqdm(total=filesize, unit="B", unit_scale=True, desc=data_id) as t:
            response = s3_client.download_file(
                Bucket="sentinel-s2-l1c",
                Key=band,
                Filename=file_path,
                ExtraArgs={"RequestPayer": "requester"},
                Callback=hook(t),
            )
    else:
        # for landsat, and preview images - resources which can be downloaded via http
        response = requests.get(url, stream=True)
        with tqdm.wrapattr(
            open(file_path, "wb"),
            "write",
            miniters=1,
            desc=data_id,
            total=int(response.headers.get("content-length", 0)),
        ) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)
        fout.close()


def data_file_exists(filename):
    return os.path.exists(filename)


def get_product_type_from_id(id):
    if "LC" in id:
        return "landsat"
    else:
        return "sentinel"


def file_paths_wrt_id(id):
    home_path_id = os.path.join(workdir, id)
    extension = None
    if get_product_type_from_id(id) == "landsat":
        extension = "tiff"
    else:
        extension = "jp2"
    return {
        "base": home_path_id,
        "preview": os.path.join(home_path_id, "%s-preview.jpg" % (id)),
        "b5": os.path.join(home_path_id, "%s-b5.%s" % (id, extension)),
        "b4": os.path.join(home_path_id, "%s-b4.%s" % (id, extension)),
        "b3": os.path.join(home_path_id, "%s-b3.%s" % (id, extension)),
        "b2": os.path.join(home_path_id, "%s-b2.%s" % (id, extension)),
        "b8": os.path.join(home_path_id, "%s-b8.%s" % (id, extension)),
        "stack": os.path.join(home_path_id, "%s-stack.tiff" % (id)),
        "pan_sharpened": os.path.join(home_path_id, "%s-pan.tiff" % (id)),
        "output_path": os.path.join(
            home_path_id, "%s-color-processed.tiff" % (id)
        ),
        "output_path_jpeg": os.path.join(
            home_path_id, "%s-color-processed.jpeg" % (id)
        ),
        "vegetation_path": os.path.join(
            home_path_id, "%s-vegetation.tiff" % (id)
        ),
        "vegetation_path_jpeg": os.path.join(home_path_id, "%s-vegetation.jpeg" % (id)),
    }
