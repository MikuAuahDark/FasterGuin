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

from .. import utils
from .base import Profile


class PCProfile(Profile):
    def run_compressor(self, image: bytes, destwoext: str, mipmap: bool = False):
        sizes = utils.size_probe(image)
        assert sizes is not None
        (w, h) = sizes
        if mipmap:
            mips = self.create_resized_mip(image)
            for i in range(len(mips)):
                with open(f"{destwoext}-mipmap{i + 1}.png", "wb+") as f:
                    f.write(mips[i])
        else:
            # Just write PNG
            with open(f"{destwoext}.png", "wb+") as f:
                f.write(image)
        return w, h
