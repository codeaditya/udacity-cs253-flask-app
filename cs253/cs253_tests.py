#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import tempfile
import unittest

import cs253
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


class CS253TestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, cs253.app.config["DATABASE"] = tempfile.mkstemp()
        cs253.app.config["TESTING"] = True
        self.app = cs253.app.test_client()
        cs253.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(cs253.app.config["DATABASE"])


class BirthdayTestCase(CS253TestCase):
    def birthday_response(self, day, month, year):
        return self.app.post("/cs253/birthday-form", data=dict(
            day=day, month=month, year=year
        ), follow_redirects=True)

    def test_birthday_form_get_page_loading(self):
        rv = self.app.get("/cs253/birthday-form")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("What's your birthday?", rv.data)

    def test_birthday_form_post_valid_inputs(self):
        correct_birthday_msg = "Thanks! That&#39;s a totally valid day."
        rv = self.birthday_response("9", "July", "1991")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(correct_birthday_msg, rv.data)
        rv = self.birthday_response("24", "Jan", "1921")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(correct_birthday_msg, rv.data)
        rv = self.birthday_response("31", "Dec", "1991")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(correct_birthday_msg, rv.data)

    def test_birthday_form_post_invalid_inputs(self):
        incorrect_birthday_msg = "That doesn&#39;t look like a valid date to me."
        rv = self.birthday_response("0", "May", "2000")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(incorrect_birthday_msg, rv.data)
        rv = self.birthday_response("31", "Sept", "2010")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(incorrect_birthday_msg, rv.data)
        rv = self.birthday_response("5", "February", "2023")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(incorrect_birthday_msg, rv.data)
        rv = self.birthday_response("17", "December", "1840")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(incorrect_birthday_msg, rv.data)


class Rot13TestCase(CS253TestCase):
    def rot13_response(self, text):
        return self.app.post("/cs253/rot13", data=dict(
            text=text
        ), follow_redirects=True)

    def test_rot13_get_page_loading(self):
        rv = self.app.get("/cs253/rot13")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Enter some text to ROT13", rv.data)

    def test_rot13_post_escaped_character_inputs(self):
        rv = self.rot13_response("That's it, this has been rot13 converted.")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Gung&#39;f vg, guvf unf orra ebg13 pbairegrq.", rv.data)

    def test_rot13_post_converted_escaped_inputs(self):
        rv = self.rot13_response("Gung&#39;f vg, guvf unf orra ebg13 pbairegrq.")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("That&amp;#39;s it, this has been rot13 converted.",
                      rv.data)

    def test_rot13_post_escaped_html_inputs(self):
        rv = self.rot13_response("Testing </html> tags </textarea>. Hopeful.")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Grfgvat &lt;/ugzy&gt; gntf &lt;/grkgnern&gt;. Ubcrshy.",
                      rv.data)


if __name__ == "__main__":
    unittest.main()
