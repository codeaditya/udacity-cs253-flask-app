#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, make_response, render_template, request

import cs253.lib.utils as utils

index = Blueprint("index", __name__)


@index.route("/")
def index_page():
    visits = 0
    visit_cookie_hashed = request.cookies.get("visits")
    if visit_cookie_hashed:
        visit_cookie_val = utils.check_secure_cookie(visit_cookie_hashed)
        if visit_cookie_val:
            visits = int(visit_cookie_val)
    visits += 1
    new_visit_cookie_hashed = utils.make_secure_cookie(str(visits))
    my_response = make_response(render_template("index.html",
                                                visits=str(visits)))
    my_response.set_cookie("visits", new_visit_cookie_hashed)
    return my_response
