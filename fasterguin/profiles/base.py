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

import json
import math
import os
import re
import subprocess

from .. import utils

from typing import Dict, List, Tuple

PACKER_OUTPUT_MATCH = re.compile(r"Writing (.+)")


class Profile:
    def __init__(self, opts: Dict[str, str]):
        # Need ImageMagick
        self.magick = utils.get_program(opts, "magick")
        if self.magick == None:
            raise Exception("ImageMagick not found")
        # Need LOVE
        if os.name == "nt":
            # In Windows, use lovec.exe
            self.love = utils.get_program(opts, "love", "lovec")
        else:
            self.love = utils.get_program(opts, "love")
        if self.love == None:
            raise Exception("LOVE not found")
        self.bb_rw_packer = opts["packer"]
        if self.bb_rw_packer == None:
            self.bb_rw_packer = os.getenv("BB_RW_PACKER")
            if self.bb_rw_packer == None:
                self.bb_rw_packer = utils.find_packerguin()
                if self.bb_rw_packer == None:
                    raise Exception("packerguin is not specified")

    def run_resize(self, image: bytes, width: int, height: int):
        process = subprocess.Popen(
            [self.magick, "convert", "png:-", "-resize", "{}x{}!".format(width, height), "-depth", "8", "png:-"],
            0,
            self.magick,
            subprocess.PIPE,
            subprocess.PIPE,
            subprocess.PIPE,
        )
        result, _ = process.communicate(image)
        process.wait()
        if process.returncode != 0:
            utils.print_to_stderr(result)
            raise Exception("Resize failed")
        return result

    def make_po2(self, image: bytes) -> Tuple[bytes, int]:
        width, height = utils.size_probe(image)
        po2 = 2 ** math.ceil(math.log2(max(width, height)))  # type: int
        process = subprocess.Popen(
            [
                self.magick,
                "convert",
                f"png:-",
                "-background",
                "transparent",
                "-gravity",
                "northwest",
                "-extent",
                "{}x{}".format(po2, po2),
                "-depth",
                "8",
                "png:-",
            ],
            0,
            self.magick,
            subprocess.PIPE,
            subprocess.PIPE,
            subprocess.PIPE,
        )
        result, stderr = process.communicate(image)
        process.wait()
        if process.returncode != 0:
            utils.print_to_stderr(stderr)
            raise Exception("PO2 failed")
        return result, po2

    def run_packer(self, input: str, output: str, po2: bool, algorithm: str = "grid"):
        cmd = [self.love, self.bb_rw_packer, input, output, "-a", algorithm]
        if po2:
            cmd.append("-2")
        process = subprocess.Popen(cmd, 0, self.love, None, subprocess.PIPE, subprocess.PIPE)
        # Run process
        result, _ = process.communicate()
        process.wait()
        if process.returncode != 0:
            utils.print_to_stderr(result)
            raise Exception(f"Packer failed with exit code {process.returncode}")
        result_str = str(result, "UTF-8")
        out = re.findall(PACKER_OUTPUT_MATCH, result_str)
        # output[1] is the PNG, output[2] is the JSON
        out_png = out[0].strip()
        out_json = out[1].strip()
        with open(out_png, "rb") as f:
            output_png = f.read()
            f.close()
            os.remove(out_png)
        with open(out_json, "r", encoding="UTF-8") as f:
            images = list(json.load(f).keys())  # type: List[str]
        filename, _ = os.path.splitext(out_png)
        return (images, filename, output_png)

    def run_compressor(self, image: bytes, destwoext: str) -> Tuple[int, int]:
        # Implementation must override this
        raise NotImplementedError("compression is not implemented")
