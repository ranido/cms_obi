#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2016 Stefano Maggiolo <s.maggiolo@gmail.com>
# Copyright © 2017-2018 Luca Wehrstedt <luca.wehrstedt@gmail.com>
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

"""This script creates a new user in the database.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.builtins.disabled import *  # noqa
from future.builtins import *  # noqa

# We enable monkey patching to make many libraries gevent-friendly
# (for instance, urllib3, used by requests)
import gevent.monkey


gevent.monkey.patch_all()  # noqa

import argparse
import logging
import sys

from cms import utf8_decoder
from cms.db import SessionGen, User
from cmscommon.crypto import generate_random_password, build_password, \
    hash_password

from sqlalchemy.exc import IntegrityError


logger = logging.getLogger(__name__)


def update_password(username, password, method, is_hashed):
    logger.info("Updating user password in the database.")

    if password is None:
        return False
    # shell will interfere with special characters, so a hashed string must be protected by
    # single quotes. We must remove them
    if password[0] == "'":
        password[0] = ' '
        if password[-1] == "'":
            password[-1] = ' '
        password = password.strip()
    
    if is_hashed:
        stored_password = build_password(password, method)
    else:
        stored_password = hash_password(password, method)

    with SessionGen() as session:
        user = session.query(User)\
            .filter(User.username == username).first()
        if user is None:
            logger.error("User %s does not exist.", username)
            return False

        session.query(User).filter(User.username == username).\
            update({"password": stored_password}, synchronize_session="fetch")
        session.commit()

    logger.info("User %s password updated, method=%s. " % (username, method))
    return True

def main():
    """Parse arguments and launch process.

    """
    parser = argparse.ArgumentParser(description="Update a user password.")
    parser.add_argument("username", action="store", type=utf8_decoder,
                        help="username used to log in")
    password_group = parser.add_mutually_exclusive_group()
    password_group.add_argument(
        "-p", "--plaintext-password", action="store", type=utf8_decoder,
        help="password of the user in plain text")
    password_group.add_argument(
        "-H", "--hashed-password", action="store", type=utf8_decoder,
        help="password of the user, already hashed using the given algorithm "
        "(currently only --bcrypt or --pbkdf2; note that the argument must be protected by single quotes "
        "if it contains shell special characters)")
    method_group = parser.add_mutually_exclusive_group()
    method_group.add_argument(
        "--bcrypt", dest="method", action="store_const", const="bcrypt",
        help="whether the password will be stored in bcrypt-hashed format "
             "(if omitted it will be stored in plain text)")
    method_group.add_argument(
        "--pbkdf2", dest="method", action="store_const", const="pbkdf2",
        help="whether the password will be stored in pbkdf2-hashed format "
             "(if omitted it will be stored in plain text)")

    args = parser.parse_args()

    if args.hashed_password is not None and args.method is None:
        parser.error("hashed password given but no method specified")

    success = update_password(args.username,
                              args.plaintext_password or args.hashed_password,
                              args.method or "plaintext",
                              args.hashed_password is not None)
    return 0 if success is True else 1


if __name__ == "__main__":
    sys.exit(main())
