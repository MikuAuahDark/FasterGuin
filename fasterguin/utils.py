# Copyright (C) 2023 Boba Birds Developers
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

import io
import os
import shutil
import struct
import sys

from typing import IO

# Also check paths
def concat_path(a: str, b: str):
    path = os.path.normpath(os.path.join(a, b))
    if path[: len(a)] != a:
        raise Exception("Path attempt to access outside root")
    return path


def get_program(opts: dict[str, str], key: str, name: str | None = None):
    result = opts[key]
    if result == None:
        result = shutil.which(name or key)
    return result


def print_to_stderr(text: bytes):
    t = str(text, " UTF-8").strip()
    if t:
        print(t, file=sys.stdout)


def size_probe(f: io.BytesIO | bytes):
    if isinstance(f, bytes):
        f = io.BytesIO(f)
        f.seek(0, io.SEEK_SET)
    header = f.read(4)
    if header == b"\x89PNG":
        if f.read(4) == b"\r\n\x1A\n":
            while True:
                (length,) = struct.unpack(">I", f.read(4))
                chunk = f.read(4)
                # Check chunks
                if chunk == b"IHDR":
                    # Header data we're looking for
                    data = struct.unpack(">II", f.read(8))
                    width = data[0]  # type: int
                    height = data[1]  # type: int
                    return (width, height)
                elif chunk == b"CgBI":
                    # This is actually non-compilant as per PNG spec said
                    # IHDR must come first.
                    f.seek(length + 4, io.SEEK_CUR)
                else:
                    break
    return None


def is_valid_image(path: str):
    valid = False
    with open(path, "rb") as f:
        header = f.read(8)
        valid = header == b"\x89PNG\r\n\x1A\n"
        f.close()
    return valid


def rmkdir(path: str):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


PACKERGUIN_STRUCTURE = [
    "annot.lua",
    "argparse.lua",
    "conf.lua",
    "JSON.lua",
    "main.lua",
    "mounter.lua",
    "RTA/baseAtlas.lua",
    "RTA/dynamicSize.lua",
    "RTA/fixedSize.lua",
    "RTA/init.lua",
    "RTA/packing.lua",
    "RTA/treeNode.lua",
    "RTA/util.lua",
]


def find_packerguin():
    path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../packerguin"))
    for files in PACKERGUIN_STRUCTURE:
        test = os.path.normpath(os.path.join(path, files))
        if not os.path.isfile(test):
            return None
    return path


def calculate_mipmaps(w: int, h: int):
    result = []  # type: list[tuple[int, int]]
    while w > 1 or h > 1:
        w = max(w // 2, 1)
        h = max(h // 2, 1)
        result.append((w, h))
    return result
