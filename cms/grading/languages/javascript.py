#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2016-2017 Stefano Maggiolo <s.maggiolo@gmail.com>
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

"""Javascript programming language definition."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.builtins.disabled import *  # noqa
from future.builtins import *  # noqa

from cms.grading import Language
from shlex import quote as shell_quote

__all__ = ["Javascript"]


class Javascript(Language):
    """This defines the Javascript programming language, interpreted with the
    standard Javascript interpret available in the system.

    """

    @property
    def name(self):
        """See Language.name."""
        return "Javascript"

    @property
    def requires_multithreading(self):
        """See Language.requires_multithreading."""
        return True

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".js"]

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        command = ["/bin/sh", "-c", 
                   "" + " ".join(["cat",
                             "/usr/local/etc/saci/prenode.js",
                             shell_quote(source_filenames[0]),
                             " > ",
                                  shell_quote(executable_filename) + ""])]
        return [command]

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""
        args = args if args is not None else []
        return [["/usr/bin/nodejs", executable_filename] + args]
