#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2012 Bernard Blackham <bernard@largestprime.net>
# Copyright © 2014-2018 Stefano Maggiolo <s.maggiolo@gmail.com>
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.builtins.disabled import *  # noqa
from future.builtins import *  # noqa

task_info = {
    "name": "batchfileiomanaged",
    "title": "Test Batch Task using manager with I/O via files",
    "official_language": "",
    "submission_format_choice": "other",
    "submission_format": "batchfileiomanaged.%l",
    "time_limit_{{dataset_id}}": "0.5",
    "memory_limit_{{dataset_id}}": "128",
    "task_type_{{dataset_id}}": "Batch",
    "TaskTypeOptions_{{dataset_id}}_Batch_compilation": "grader",
    "TaskTypeOptions_{{dataset_id}}_Batch_io_0_inputfile": "input.txt",
    "TaskTypeOptions_{{dataset_id}}_Batch_io_1_outputfile": "output.txt",
    "TaskTypeOptions_{{dataset_id}}_Batch_output_eval": "comparator",
    "score_type_{{dataset_id}}": "Sum",
    "score_type_parameters_{{dataset_id}}": "50",
}

managers = [
    "grader.c",
    "grader.cpp",
    "grader.pas",
    "grader.py",
    "grader.java",
    "grader.cs",
    "checker",
]

test_cases = [
    ("1.in", "1.out", True),
    ("2.in", "2.out", False),
]
