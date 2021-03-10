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

    requiredNamed.add_argument(
        "--name",
        required=True,
        help="Name of run",
    )

    return parser

def whitelist(name):
    """
    Whitelist step of SICILIAN
    """

    t_config = TransferConfig(use_threads=False, num_download_attempts=25)

    if not os.path.exists(name):
        os.makedirs(name)

    return name


def get_default_requirements():
    """
    Optional: Define the default hardware requirements for this job
    """
    return argparse.Namespace(vcpus=4, memory=8000, storage=500)


def main(logger):
    # get the argument parser and parse args
    parser = get_parser()
    args = parser.parse_args()

    dest_dir = whitelist(args.name)
    print(dest_dir)

    # use the logger
    logger.info("Attempting to echo the message...")

    # run a subprocess and log the attempt
    failed = log_command(logger, "echo {}".format(args.message), shell=True)


if __name__ == "__main__":
    mainlogger, log_file, file_handler = ut_log.get_logger(__name__)
    s3c = boto3.client("s3")
    main(mainlogger)
