# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/02_cli.ipynb (unless otherwise specified).

__all__ = ['get_cli_args', 'main']

# Cell
import argparse
import os
import numpy as np
from .core import unwrap
from .loading import load_interferogram

# Cell


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Name of interferogram file to load")
    parser.add_argument(
        "--outname", "-o", help="Name of output file to save (default = `filename`.unw)"
    )
    parser.add_argument(
        "--max-iters",
        default=500,
        type=int,
        help="maximum number of ADMM iterations to run (default = %(default)s)",
    )
    parser.add_argument(
        "--tol",
        default=np.pi / 10,
        type=float,
        help="maximum allowed change for any pixel between ADMM iterations (default = %(default)s)",
    )
    parser.add_argument(
        "--lmbda",
        default=1,
        type=float,
        help="splitting parameter of ADMM. Smaller = more stable, Larger = faster "
        "convergence. (default = %(default)s)",
    )
    parser.add_argument(
        "--p",
        default=0,
        type=float,
        help="value used in shrinkage operator (default = %(default)s)",
    )
    parser.add_argument(
        "--c",
        default=1.3,
        type=float,
        help="acceleration constant using in updating lagrange multipliers in ADMM "
        "(default = %(default)s)",
    )
    parser.add_argument(
        "--dtype",
        default="float32",
        help="numpy datatype of filename (default = %(default)s)",
    )
    parser.add_argument(
        "--debug", action="store_true", help="print diagnostic ADMM information"
    )
    return parser.parse_args()


def main():
    arg_dict = vars(get_cli_args())
    inname = arg_dict.pop("filename")
    igram = load_interferogram(inname)
    mag = np.abs(igram)
    phase = np.angle(igram)
    outname = arg_dict.pop("outname")
    if outname is None:
        base, ext = os.path.splitext(inname)
        outname = base + ".unw"

    if not outname.endswith(".unw"):
        raise NotImplementedError(
            "Only saving as binary .unw is implemented currently."
        )
    # TODO: save as other types?
    unw_phase = unwrap(phase, **arg_dict)
    unw_with_mag = np.hstack((mag, unw_phase))
    unw_with_mag.tofile(outname)