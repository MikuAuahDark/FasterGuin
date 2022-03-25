# Copyright (C) 2022 Boba Birds Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import argparse
import os
import shlex
import sys

if __name__ == "__main__" and __package__ is None:
    # Copied from yt-dlp
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))
    __package__ = "fasterguin"

from . import utils
from .asset import Asset
from .options.base import UnsupportedOption

from . import COMMAND_LIST, OPTION_LIST, PROFILE_LIST

def process_command(cmddata: list[str], context: Asset):
    # Parse command
    cmd_name = cmddata[0].lower()
    cmd_class = COMMAND_LIST.get(cmd_name)
    if cmd_class == None:
        raise Exception(f"Unknown command '{cmd_name}'")
    cmd = cmd_class(cmddata[1])
    # Parse options
    for i in range(2, len(cmddata), 2):
        opt_name = cmddata[i].lower()
        opt_class = OPTION_LIST.get(opt_name)
        if opt_class == None:
            raise Exception(f"Unknown option '{opt_name}'")
        opt = opt_class(opt_name, cmddata[i + 1])
        try:
            cmd.add_option(opt)
        except UnsupportedOption as e:
            raise Exception(f"Command '{cmd_name}': {e}")
    cmd.execute(context)

def main(arg):
    parser = argparse.ArgumentParser("program")
    parser.add_argument("input", help="Asset definition file.")
    parser.add_argument("output", help="Processed asset output directory.")
    parser.add_argument("-d", "--directory", help="Unprocessed asset input directory.")
    parser.add_argument("-p", "--profile", help="Asset processing profile.", choices=PROFILE_LIST.keys(), default='pc')
    parser.add_argument("--astcenc", help="astcenc executable.")
    parser.add_argument("--etctool", help="EtcTool executable.")
    parser.add_argument("--love", help="LOVE executable.")
    parser.add_argument("--magick", help="ImageMagick executable.")
    parser.add_argument("--packer", help="packerguin path/.love file.")
    # Parse args
    args = parser.parse_args(arg[1:])
    opts = {
        'astcenc': args.astcenc,
        'etctool': args.etctool,
        'magick': args.magick,
        'love': args.love,
        'packer': args.packer
    }
    profile = PROFILE_LIST[args.profile](opts)
    asset = Asset(profile)
    input_abs = os.path.abspath(args.input)
    input_dir = os.path.dirname(input_abs) if args.directory == None else os.path.abspath(args.directory)
    output_abs = os.path.abspath(args.output)
    asset.set_input_directory(input_dir)
    asset.set_output_directory(output_abs)
    utils.rmkdir(output_abs)
    # Start parsing
    line_count = 0
    with open(args.input, 'r', encoding='UTF-8') as f:
        for line in f:
            line_count = line_count + 1
            line = line.strip()
            if len(line) > 0:
                params = shlex.split(line, True)
                if len(params) > 0:
                    try:
                        process_command(params, asset)
                    except Exception as e:
                        print(f"Error while parsing at line {line_count}")
                        raise e
    # Write metadata
    realsize = asset.get_output_path(asset.get_realsize_output())
    with open(realsize, 'w', encoding='UTF-8') as f:
        print(f"Writing {realsize}")
        asset.dump_real_size(f)

if __name__ == "__main__":
    main(sys.argv)
