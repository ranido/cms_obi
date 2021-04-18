#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2018 Stefano Maggiolo <s.maggiolo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for the binary module"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.builtins.disabled import *  # noqa
from future.builtins import *  # noqa

import unittest

from cmscommon.commands import pretty_print_cmdline


class TestPrettyPrintCmdline(unittest.TestCase):

    def test_success(self):
        self.assertEqual(
            pretty_print_cmdline(["ls", "-al", "file"]),
            "ls -al file")

    def test_spaces(self):
        self.assertEqual(
            pretty_print_cmdline(["ls", "-al", "file with spaces"]),
            "ls -al 'file with spaces'")

    def test_quotes(self):
        self.assertEqual(
            pretty_print_cmdline(["ls", "-al", "file'with'quotes"]),
            """ls -al 'file'"'"'with'"'"'quotes'""")

    def test_double_quotes(self):
        self.assertEqual(
            pretty_print_cmdline(["ls", "-al", "file\"with\"dblquotes"]),
            """ls -al 'file"with"dblquotes'""")


if __name__ == "__main__":
    unittest.main()
