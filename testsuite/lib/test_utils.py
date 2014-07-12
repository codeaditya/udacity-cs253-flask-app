#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import cs253.lib.utils as utils


class UtilsPasswordTestCase(unittest.TestCase):
    def test_make_random_salt_length(self):
        self.assertEqual(len(utils.make_random_salt()), 5)
        self.assertEqual(len(utils.make_random_salt(2)), 2)
        self.assertEqual(len(utils.make_random_salt(11)), 11)

    def test_make_random_salt_returns_string(self):
        self.assertIsInstance(utils.make_random_salt(), str)
        self.assertIsInstance(utils.make_random_salt(6), str)

    def test_make_pw_hash_returns_string(self):
        self.assertIsInstance(utils.make_pw_hash("name", "password"), str)
        self.assertIsInstance(utils.make_pw_hash("name", "password", "salt"),
                              str)

    def test_make_pw_hash_does_not_contain_password(self):
        self.assertNotIn("password", utils.make_pw_hash("name", "password"))
        self.assertNotIn("password",
                         utils.make_pw_hash("name", "password", "salt"))

    def test_make_pw_hash_length(self):
        hashed_pw = utils.make_pw_hash("name", "password")
        hashed_pw_list = hashed_pw.split("|")
        self.assertEqual(len(hashed_pw_list), 2)
        hashed_pw = utils.make_pw_hash("name", "password", "salt")
        hashed_pw_list = hashed_pw.split("|")
        self.assertEqual(len(hashed_pw_list), 2)

    def test_make_pw_hash_with_known_salt_returns_same_salt(self):
        hashed_pw = utils.make_pw_hash("name", "password", "salt")
        hashed_pw_list = hashed_pw.split("|")
        self.assertEqual(hashed_pw_list[1], "salt")

    def test_valid_pw(self):
        computed_hash = utils.make_pw_hash("name", "password", "salt")
        random_hash = utils.make_pw_hash("random_name", "random_password")
        self.assertTrue(utils.valid_pw("name", "password", computed_hash))
        self.assertTrue(computed_hash != random_hash)
        self.assertFalse(utils.valid_pw("name", "password", random_hash))


class UtilsCookieTestCase(unittest.TestCase):
    def test_hash_cookie_returns_string(self):
        self.assertIsInstance(utils.hash_cookie("cookie"), str)
        self.assertIsInstance(utils.hash_cookie("11"), str)

    def test_make_secure_cookie_returns_string(self):
        self.assertIsInstance(utils.make_secure_cookie("cookie"), str)
        self.assertIsInstance(utils.make_secure_cookie("11"), str)

    def test_make_secure_cookie(self):
        secure_cookie = utils.make_secure_cookie("cookie")
        secure_cookie_list = secure_cookie.split("|")
        self.assertEqual(secure_cookie_list[0], "cookie")
        self.assertEqual(secure_cookie_list[1], utils.hash_cookie("cookie"))

    def test_check_secure_cookie_returns_none_for_none_hashed_string(self):
        self.assertIsNone(utils.check_secure_cookie(None))

    def test_check_secure_cookie_returns_none_for_modified_cookie_value(self):
        hashed_string = utils.make_secure_cookie("cookie")
        hashed_string_list = hashed_string.split("|")
        hashed_string_list[0] = "modified_cookie_value"
        modified_hashed_string = "|".join(hashed_string_list)
        self.assertIsNone(utils.check_secure_cookie(modified_hashed_string))

    def test_check_secure_cookie_returns_none_for_modified_cookie_hash(self):
        hashed_string = utils.make_secure_cookie("cookie")
        hashed_string_list = hashed_string.split("|")
        hashed_string_list[1] = "modified_cookie_hash"
        modified_hashed_string = "|".join(hashed_string_list)
        self.assertIsNone(utils.check_secure_cookie(modified_hashed_string))

    def test_check_secure_cookie_returns_cookie_value_for_unmodified_hash(self):
        hashed_string = utils.make_secure_cookie("cookie")
        self.assertEqual("cookie", utils.check_secure_cookie(hashed_string))
