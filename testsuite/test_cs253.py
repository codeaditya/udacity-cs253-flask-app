#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import tempfile
import unittest

import cs253


class CS253TestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, cs253.app.config["DATABASE"] = tempfile.mkstemp()
        cs253.app.config["TESTING"] = True
        self.app = cs253.app.test_client()
        self.ctx = cs253.app.test_request_context()
        self.ctx.push()
        cs253.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(cs253.app.config["DATABASE"])
        self.ctx.pop()
