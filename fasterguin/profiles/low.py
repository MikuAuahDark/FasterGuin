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

import math
import os
import subprocess
import sys
import tempfile

from .. import utils
from .base import Profile


class LowProfile(Profile):
    def __init__(self, opts: dict[str, str]):
        Profile.__init__(self, opts)
        # Search etcpack
        self.etctool = utils.get_program(opts, "etctool", "EtcTool")
        if self.etctool == None:
            raise Exception("EtcTool not found")

    def run_compressor(self, image: bytes, destwoext: str):
        # Create temp output directory
        filename, _ = os.path.splitext(os.path.basename(tempfile.mktemp()))
        image_po2, po2size = self.make_po2(image)
        mipmaps = str(int(math.log2(po2size)) + 1)
        filenamepng = f"{filename}.png"
        with open(filenamepng, "wb") as f:
            f.write(image_po2)
            f.close()
        cmd = [
            self.etctool,
            filenamepng,
            "-format",
            "RGBA8",
            "-effort",
            "0",
            "-j",
            str(os.cpu_count()),
            "-m",
            mipmaps,
            "-output",
            f"{destwoext}.etc2.ktx",
        ]
        success = False
        # etc2comp crashes sometimes, so try it 10 times
        for i in range(1, 11):
            process = subprocess.Popen(cmd, 0, self.etctool, subprocess.PIPE, sys.stdout, sys.stderr)
            process.communicate(None)
            process.wait()
            if process.returncode == 0:
                success = True
                break
            else:
                print(f"etctool failed with code {process.returncode}, attempt {i} of 10")
        if not success:
            raise Exception("etctool failed")
        os.remove(filenamepng)
        return (po2size, po2size)
