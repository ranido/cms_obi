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

"""Java programming language definition, using the default JDK installed
in the system.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.builtins.disabled import *  # noqa
from future.builtins import *  # noqa
from six import PY3

if PY3:
    from shlex import quote as shell_quote
else:
    from pipes import quote as shell_quote

from cms.grading import Language


# ranido-begin
import os
import logging
logger = logging.getLogger(__name__)
# ranido-end

__all__ = ["JavaJDK"]


class JavaJDK(Language):
    """This defines the Java programming language, compiled and executed using
    the Java Development Kit available in the system.

    """

    USE_JAR = True

    @property
    def name(self):
        """See Language.name."""
        return "Java / JDK"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".java"]

    @property
    def requires_multithreading(self):
        """See Language.requires_multithreading."""
        return True

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""

        # ranido-begin
        changed_name = False
        logger.info("+++++++++ java source_file=%s", source_filenames[0])
        tmp,ext = os.path.splitext(source_filenames[0])
        if tmp.find('_'):
            logger.info("+++++++++ java tmp=%s, ext=%s", tmp,ext)
            tmp = tmp.split('_')
            new_name = tmp[-1] + '.java'
            logger.info("************ newname=%s", new_name)
            if new_name != source_filenames[0]:
                copy_command = ["/bin/cp", source_filenames[0], new_name]
                source_filenames = [new_name]
                logger.info("************ java source_file=%s", source_filenames[0])
                logger.info("************ java using source_file=%s", new_name)
                changed_name = True
        # ranido-end
        
        compile_command = ["/usr/bin/javac"] + source_filenames
        # We need to let the shell expand *.class as javac create
        # a class file for each inner class.

        if JavaJDK.USE_JAR:
            jar_command = ["/bin/sh", "-c",
                           " ".join(["jar", "cf",
                                     shell_quote(executable_filename),
                                     "*.class"])]
            # ranido-begin
            if changed_name:
                logger.info("************ return copy_command=%s", str(copy_command))
                return [copy_command, compile_command, jar_command]
            else:
                logger.info("************ return compile_command without copy")
                return [compile_command, jar_command]
            # ranido-end
        else:
            zip_command = ["/bin/sh", "-c",
                           " ".join(["zip", "-r", "-", "*.class", ">",
                                     shell_quote(executable_filename)])]
            # ranido-begin
            if changed_name:
                logger.info("************ return copy_command=%s", str(copy_command))
                return [copy_command, compile_command, zip_command]
            else:
                logger.info("************ return compile_command without copy")
                return [compile_command, zip_command]
            # ranido-end

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""

        # ranido-begin
        #main = 'solucao'
        tmp = executable_filename
        if tmp.find('_') > 0:
            logger.info("************ java main=%s", main)
            tmp = tmp.split('_')
            main = tmp[-1]
            logger.info("************ java using main=%s", main)
        # ranido-end

        args = args if args is not None else []

        if JavaJDK.USE_JAR:
            # executable_filename is a jar file, main is the name of
            # the main java class
            return [["/usr/bin/java", "-Deval=true", "-Xmx512M", "-Xss64M",
                     "-cp", executable_filename, main] + args] 
        else:
            unzip_command = ["/usr/bin/unzip", executable_filename]
            command = ["/usr/bin/java", "-Deval=true", "-Xmx512M", "-Xss64M",
                       main] + args
            return [unzip_command, command]
