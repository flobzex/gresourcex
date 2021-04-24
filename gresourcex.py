#! /usr/bin/env python3

from os import path
import sys
import subprocess


def make_gresource_list(input_file):
    proc = subprocess.run(["gresource", "list", input_file],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    if proc.returncode != 0:
        raise IOError(f"Invalid target '{input_file}': the file doesn't exist or is in an invalid format.")

    items_string = proc.stdout.decode("UTF-8")
    items = items_string.split("\n")

    return [x for x in items if len(x) != 0]


def read_resource_data(input_file, resource_path):
    proc = subprocess.run(["gresource", "extract", input_file, resource_path], \
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    if proc.returncode != 0:
        raise IOError(f"No such resource: {resource_path}")

    return proc.stdout


def write_resource_file(data, resource_path, out_file):
    res_dir = path.split(out_file)[0].strip()

    if len(res_dir) != 0 and not path.exists(res_dir):
        # print("> Making directory:", res_dir)
        path.os.makedirs(res_dir)

    try:
        print("> Writing", resource_path)
        f = open(out_file, "wb")
        f.write(data)
        f.close()
    except IOError as e:
        print(f"Unable to write resource '{resource_path}':", e)


def extract_gresource(input_file, output_dir):
    items = make_gresource_list(input_file)
    
    for res in items:
        data = read_resource_data(input_file, res)
        write_resource_file(data, res, output_dir + res)


def _print_help():
    print("usage: gresourcex <file> <out_dir>")
    exit(1)


def _check_args():
    argv_len = len(sys.argv)

    if argv_len == 2 and sys.argv[1] == "-h":
        _print_help()

    if argv_len < 3:
        print("error: missing arguments", file=sys.stderr)
        _print_help()
    elif argv_len > 3:
        print("error: too many arguments", file=sys.stderr)
        _print_help()

    input_file, output_dir = sys.argv[1:3]

    # check if input file exists
    if not path.exists(input_file):
        print("error: file doesn't exist:", input_file, file=sys.stderr)
        exit(1)

    # check if output dir 
    if path.exists(output_dir):
        print("error: there is already a file or directory with this name:", output_dir)

    return input_file, output_dir


def main():
    input_file, output_dir = _check_args()
    
    try:
        extract_gresource(input_file, output_dir)
    except IOError as e:
        raise e
        #print(e)
        exit(1)


if __name__ == "__main__":
    main()

