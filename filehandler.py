import argparse
import os
import time


# TODO possible error handling

def get_filename():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-f', '-file', type=str, help='file to read')

    # TODO this?
    arg_parser.add_argument('-d', '-dir', type=str, help='directory to read')
    arg_parser.add_argument('-fp', '-file_regex', type=str, help='file name regex pattern')

    args = arg_parser.parse_args()
    return args.f


def open_read_file(filename, beginning=False):
    file = open(filename, 'r')

    if not beginning:
        file.seek(os.SEEK_SET, os.SEEK_END)

    return file


def read_till_eof(file, max_lines_to_read=20, max_secs_to_read=1):
    lines = []

    start_time = time.perf_counter()
    line = file.readline()
    while line and len(lines) < max_lines_to_read and (time.perf_counter() - start_time < max_secs_to_read):
        lines.append(line)
        line = file.readline()

    file.seek(file.tell())

    return lines
