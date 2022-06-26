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

import os
import subprocess
import sys
import tempfile

from .. import utils
from .base import Profile


POSSIBLE_ASTCENC = ["astcenc", "astcenc-avx2", "astcenc-sse4.1", "astcenc-sse2", "astcenc-neon", "astcenc-native"]


class AndroidProfile(Profile):
    def __init__(self, opts: dict[str, str]):
        Profile.__init__(self, opts)
        # Search astcenc
        for astcenc in POSSIBLE_ASTCENC:
            self.astcenc = utils.get_program(opts, "astcenc", astcenc)
            if self.astcenc is not None:
                break
        if self.astcenc == None:
            raise Exception("astcenc not found")

    def run_compressor(self, image: bytes, destwoext: str):
        image_po2, po2size = self.make_po2(image)
        filename = os.path.basename(tempfile.mktemp(".png"))
        with open(filename, "wb") as f:
            f.write(image_po2)
            f.close()
        process = subprocess.Popen(
            [self.astcenc, "-cl", filename, f"{destwoext}.astc.ktx", "4x4", "100", "-silent"],
            0,
            self.astcenc,
            subprocess.PIPE,
            sys.stdout,
            sys.stderr,
        )
        process.communicate(None)
        process.wait()
        os.remove(filename)
        if process.returncode != 0:
            raise Exception("astcenc failed")
        return (po2size, po2size)
