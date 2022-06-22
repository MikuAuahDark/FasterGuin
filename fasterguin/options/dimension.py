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

import re

from .base import Option

DIMENSION_MATCH = re.compile(r"^(\d+)x(\d+)$")


class DimensionOption(Option):
    def __init__(self, name: str, value: str):
        Option.__init__(self, name, value)
        if value == "original":
            self.dimensions = None
        else:
            match = re.match(DIMENSION_MATCH, value)
            if match != None:
                width = int(match.group(1))
                height = int(match.group(2))
                if width > 0 and height > 0:
                    self.dimensions = (width, height)
                    return
            raise Exception("Invalid dimensions")

    def get_dimensions(self):
        return self.dimensions
