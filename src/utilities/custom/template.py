#!/usr/bin/env python

# template for writing new AWS batch scripts
import argparse
import datetime
import os
import re
import subprocess
import tarfile
import time

from collections import defaultdict

from utilities.log_util import get_logger, log_command

import boto3
from boto3.s3.transfer import TransferConfig

# an s3 bucket to upload your logs, if you want them
S3_LOG_DIR = "s3://salzman-lab/script_logs/"


def get_parser():
    """
    Required: Define the arguments your script takes in this function,
    so that evros can test them before launching a job
    """
    parser = argparse.ArgumentParser(
        prog="template.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Run SICILIAN"
    )

    requiredNamed = parser.add_argument_group("required arguments")

    """requiredNamed.add_argument(
        "--S3_input_data_path",
        required=True,
        help="Location of data in bucket",
    )"""

    requiredNamed.add_argument(
        "--out_path",
        required=True,
        help="Location to store results",
    )

    requiredNamed.add_argument(
        "--name",
        required=True,
        help="Name of run",
    )
"""
    requiredNamed.add_argument(
        "--r_ends",
        required=True,
        help="Format of fastq file extension",
    )

    requiredNamed.add_argument(
        "--bc_pattern",
        required=True,
        help="Barcode pattern",
    )
"""
    return parser

def whitelist(out_path, name):
    """
    Whitelist step of SICILIAN
    """

    t_config = TransferConfig(use_threads=False, num_download_attempts=25)

    dest_dir = os.path.join(out_path, name)
    if not os.path.exists(dest_dir):
        os.makediirs(dest_dir)

    return dest_dir


def get_default_requirements():
    """
    Optional: Define the default hardware requirements for this job
    """
    return argparse.Namespace(vcpus=4, memory=8000, storage=500)


def main(logger):
    # get the argument parser and parse args
    parser = get_parser()
    args = parser.parse_args()

    # use the logger
    logger.info("Attempting to echo the message...")

    # run a subprocess and log the attempt
    failed = log_command(logger, "echo {}".format(args.message), shell=True)


if __name__ == "__main__":
    mainlogger, log_file, file_handler = get_logger(__name__)

    dest_dir = whitelist(args.out_path, args.name)

    try:
        main(mainlogger)
    except:
        mainlogger.info("An exception occurred", exc_info=True)
        raise
