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
from ..options.destination import DestinationOption
from ..options.dimension import DimensionOption
from ..options.resize import ResizeOption

from .base import Command
from .file import FileCommand

OPTS_LIST = (DimensionOption, ResizeOption)

class FolderCommand(Command):
    def __init__(self, value: str):
        Command.__init__(self, value)
        # Ensure slashes
        v = value.replace('\\', '/')
        if v[-1] != '/':
            self.value = v + '/'
        else:
            self.value = v
    def accept_option(self, option: type):
        return option == DimensionOption or option == ResizeOption or option == DestinationOption
    def execute(self, context: Asset):
        files = []
        dest = self.get_option(DestinationOption)
        input_path = context.get_input_path(self.value)
        for _, _, f in os.walk(input_path):
            files.extend(f)
            break
        for f in files:
            if utils.is_valid_image(os.path.join(input_path, f)):
                cmd = FileCommand(self.value + f)
                for opt in OPTS_LIST:
                    opt_data = self.get_option(opt)
                    if opt_data != None:
                        cmd.add_option(opt_data)
                if dest != None:
                    cmd.set_output_override(dest.get_value())
                cmd.execute(context)
