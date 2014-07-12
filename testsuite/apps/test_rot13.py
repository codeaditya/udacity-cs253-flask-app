#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import url_for

from testsuite.test_cs253 import CS253TestCase


class Rot13TestCase(CS253TestCase):
    def rot13_response(self, text):
        return self.app.post(url_for("rot13.rot13_form"), data=dict(
            text=text
        ), follow_redirects=True)

    def test_rot13_get_page_loading(self):
        rv = self.app.get(url_for("rot13.rot13_form"))
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
