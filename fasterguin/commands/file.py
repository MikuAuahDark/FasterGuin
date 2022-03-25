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

from .. import utils
from ..asset import Asset
from ..options.dimension import DimensionOption
from ..options.resize import ResizeOption

from .base import Command

class FileCommand(Command):
    def __init__(self, value: str):
        Command.__init__(self, value)
        self.outdir_override = None
    def set_output_override(self, outdir_override: str):
        self.outdir_override = outdir_override
    def get_output_filename(self):
        if self.outdir_override != None:
            return self.outdir_override + os.path.basename(self.value)
        else:
            return self.value
    def accept_option(self, option: type):
        return option == DimensionOption or option == ResizeOption
    def execute(self, context: Asset):
        dimension = self.get_option(DimensionOption)
        resize = self.get_option(ResizeOption)
        with open(context.get_input_path(self.value), 'rb') as f:
            png = f.read()
        profile = context.get_profile()
        print(f"Processing {self.value}")
        cw, ch = utils.size_probe(png)
        ow, oh = cw, ch
        rw, rh = cw, ch
        if resize != None:
            rw, rh = resize.compute_size(cw, ch)
            png = profile.run_resize(png, rw, rh)
        if dimension == None:
            ow, oh = rw, rh
        else:
            dimensions = dimension.get_dimensions()
            if dimensions != None:
                ow, oh = dimensions[0], dimensions[1]
        out = self.get_output_filename()
        outpath = context.get_output_path(out)
        utils.rmkdir(os.path.dirname(outpath))
        outwoext, _ = os.path.splitext(outpath)
        profile.run_compressor(png, outwoext)
        context.add_real_size(out, ow, oh, rw, rh)
