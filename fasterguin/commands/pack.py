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

from ..asset import Asset
from ..options.algorithm import AlgorithmOption
from ..options.mipmap import MipmapOption

from .base import Command


class PackCommand(Command):
    def accept_option(self, option: type):
        return option in (AlgorithmOption, MipmapOption)

    def execute(self, context: Asset):
        algo = self.get_option(AlgorithmOption)
        mip = self.get_option(MipmapOption)
        profile = context.get_profile()
        print(f"Packing {self.value}")
        images, output, png = profile.run_packer(
            context.get_input_path(self.value),
            context.get_output_path(),
            True,
            "grid" if algo == None else algo.get_value(),
        )
        w, h = profile.run_compressor(png, output, mip is not None and mip.get_mipmap())
        for img in images:
            context.register_image(img)
        context.add_real_size(context.to_relative_output(output) + ".png", w, h, w, h)
