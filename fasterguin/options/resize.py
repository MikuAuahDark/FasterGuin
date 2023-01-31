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

from .base import Option


class ResizeOption(Option):
    def __init__(self, name: str, value: str):
        Option.__init__(self, name, value)
        self.scaling = None
        self.width = None
        self.height = None
        if value[-1] == "%":
            try:
                self.scaling = float(value[:-1]) / 100.0
            except ValueError:
                raise Exception("Invalid resize value")
        else:
            dimension = value.split("x")
            if len(dimension) == 2:
                try:
                    if dimension[0] != "":
                        self.width = int(dimension[0])
                    if dimension[1] != "":
                        self.height = int(dimension[1])
                    if self.width == None and self.height == None:
                        raise Exception("invalid")
                except Exception:
                    raise Exception("Invalid resize value")

    def compute_size(self, width: int, height: int):
        # I still have no idea what rounding should be used, so I picked
        # ceil for now.
        if self.scaling != None:
            return math.ceil(width * self.scaling), math.ceil(height * self.scaling)
        elif self.width != None and self.height != None:
            return self.width, self.height
        elif self.width != None:
            return self.width, math.ceil(self.width * height / float(width))
        elif self.height != None:
            return math.ceil(self.height * width / float(height)), self.height
        else:
            raise Exception("Invalid resize state (width, height, scaling is None)")
