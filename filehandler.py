import argparse
import select
import subprocess


# TODO possible error handling

def get_filename():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-f', '-file', type=str, help='file to read')

    # TODO this?
    arg_parser.add_argument('-d', '-dir', type=str, help='directory to read')
    arg_parser.add_argument('-fp', '-file_regex', type=str, help='file name regex pattern')

    args = arg_parser.parse_args()
    return args.f


def tail_file(filename):
    # _stream = subprocess.run(["tail", "-f", filename], capture_output=True, text=True)
    stream = subprocess.Popen(["tail", "-f", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    poller = select.poll()
    poller.register(stream.stdout)
    return poller, stream


def write_to_file(filename, lines):
    file = open(filename, 'a+')
    # for line in lines:
    file.writelines(lines)
