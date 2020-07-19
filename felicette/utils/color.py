"""
Source: https://github.com/mapbox/rio-color/blob/master/rio_color/scripts/cli.py

Further modifications made to make it functional with felicette
"""
import rasterio
from rasterio.rio.options import creation_options
from rasterio.transform import guard_transform
from rio_color.workers import atmos_worker, color_worker
from rio_color.operations import parse_operations, simple_atmo_opstring
import riomucho
from rich import print


def check_jobs(jobs):
    """Validate number of jobs."""
    if jobs == 0:
        print("Jobs must be >= 1 or == -1")
    elif jobs < 0:
        import multiprocessing

        jobs = multiprocessing.cpu_count()
    return jobs


def color(jobs, out_dtype, src_path, dst_path, operations, creation_options):
    with rasterio.open(src_path) as src:
        opts = src.profile.copy()
        windows = [(window, ij) for ij, window in src.block_windows()]

    opts.update(**creation_options)
    opts["transform"] = guard_transform(opts["transform"])

    out_dtype = out_dtype if out_dtype else opts["dtype"]
    opts["dtype"] = out_dtype

    args = {"ops_string": " ".join(operations), "out_dtype": out_dtype}
    # Just run this for validation this time
    # parsing will be run again within the worker
    # where its returned value will be used
    try:
        parse_operations(args["ops_string"])
    except ValueError as e:
        import sys

        sys.exit(1)
        print(e)

    jobs = check_jobs(jobs)

    if jobs > 1:
        with riomucho.RioMucho(
            [src_path],
            dst_path,
            color_worker,
            windows=windows,
            options=opts,
            global_args=args,
            mode="manual_read",
        ) as mucho:
            mucho.run(jobs)
    else:
        with rasterio.open(dst_path, "w", **opts) as dest:
            with rasterio.open(src_path) as src:
                rasters = [src]
                for window, ij in windows:
                    arr = color_worker(rasters, window, ij, args)
                    dest.write(arr, window=window)

                dest.colorinterp = src.colorinterp
