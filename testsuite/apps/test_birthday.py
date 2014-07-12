#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import url_for

from testsuite.test_cs253 import CS253TestCase


class BirthdayTestCase(CS253TestCase):
    def birthday_response(self, day, month, year):
        return self.app.post(url_for("birthday.birthday_form"), data=dict(
            day=day, month=month, year=year
        ), follow_redirects=True)

    def test_birthday_form_get_page_loading(self):
        rv = self.app.get(url_for("birthday.birthday_form"))
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
