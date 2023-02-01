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
import os

from . import utils
from .profiles.base import Profile


class Asset:
    def __init__(self, profile: Profile):
        self.input = None
        self.output = None
        self.prefix = ""
        self.profile = profile
        self.real_sizes = {}
        self.real_size_out = "metadata.json"
        self.registered_images = set()
        self.mipmapping = False

    def set_input_directory(self, path: str):
        self.input = os.path.abspath(path)

    def set_output_directory(self, path: str):
        self.output = os.path.abspath(path)

    def get_profile(self):
        return self.profile

    def set_prefix(self, prefix: str):
        if len(prefix) == 0:
            self.prefix = ""
        else:
            prefix = prefix.replace("\\", "/")
            if prefix[-1] != "/":
                self.prefix = prefix + "/"
            else:
                self.prefix = prefix

    def get_prefix(self):
        return self.prefix

    def get_input_path(self, path: str = None):
        if path == None:
            return self.input
        else:
            return utils.concat_path(self.input, path)

    def get_output_path(self, path: str = None):
        if self.output == None:
            raise Exception("Output path is not defined")
        if path == None:
            return self.output
        else:
            return utils.concat_path(self.output, path)

    def to_relative_output(self, abspath: str):
        if self.output == None:
            raise Exception("Output path is not defined")
        abspath = os.path.normpath(abspath)
        if abspath[: len(self.output)] != self.output:
            raise Exception("Absolute path is outside output directory")
        return abspath[len(self.output) + 1 :]

    def register_image(self, fullimage: str):
        if fullimage in self.registered_images:
            print(f"Image {fullimage} already registered.")
            return False
        else:
            self.registered_images.add(fullimage)

    def add_real_size(self, image: str, ow: int, oh: int, w: int, h: int):
        path = self.prefix + image
        self.real_sizes[path] = [ow, oh, w, h]
        self.register_image(path)

    def dump_real_size(self, f):
        if f != None:
            json.dump(self.real_sizes, f, indent="\t", ensure_ascii=False)
        else:
            return json.dumps(self.real_sizes, indent="\t", ensure_ascii=False)

    def get_realsize_output(self):
        return self.real_size_out

    def set_realsize_output(self, out: str):
        self.real_size_out = out

    def get_mipmap(self):
        return self.mipmapping

    def enable_mipmap(self):
        self.mipmapping = True
