#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

rot13 = Blueprint("rot13", __name__, template_folder="templates")


def rot13_converted(text):
    rot13_text = ""
    split_text = text.splitlines()
    for lines in split_text:
        for alphabet in lines:
            rot13_text += convert_to_rot13(alphabet)
        rot13_text += "\n"
    return rot13_text


def convert_to_rot13(alphabet):
    unicode_codepoint = ord(alphabet)
    # for small letters
    minimum, maximum = 97, 122
    if minimum <= unicode_codepoint <= maximum:
        return rot_character(unicode_codepoint, minimum, maximum)
    # for capital letters
    minimum, maximum = 65, 90
    if minimum <= unicode_codepoint <= maximum:
        return rot_character(unicode_codepoint, minimum, maximum)
    else:
        return alphabet


def rot_character(unicode_codepoint, minimum, maximum):
    unicode_codepoint += 13
    difference = unicode_codepoint - maximum
    if difference > 0:
        unicode_codepoint = (minimum - 1) + difference
    return chr(unicode_codepoint)


@rot13.route("/", methods=["GET", "POST"])
def rot13_form():
    rot13_text = ""
    if request.method == "POST":
        text = request.form.get("text")
        rot13_text = rot13_converted(text)
    return render_template("rot13_form.html", text=rot13_text)
