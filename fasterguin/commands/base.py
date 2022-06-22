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

from ..asset import Asset
from ..options.base import Option, UnsupportedOption

from typing import TypeVar

T = TypeVar("T")


class Command:
    def __init__(self, value: str):
        self.options = {}
        self.value = value

    def accept_option(self, option: type):
        return False

    def get_value(self):
        return self.value

    def add_option(self, option: Option):
        opttype = type(option)
        if self.accept_option(opttype):
            self.options[opttype] = option
        else:
            raise UnsupportedOption(option)

    def get_option(self, option: type[T]) -> T | None:
        return self.options.get(option)

    def execute(self, context: Asset):
        pass
