#!/usr/bin/python
# -*- coding: utf-8 -*-

import contextlib
import sqlite3

from flask import Flask, g, request
from werkzeug.contrib.cache import SimpleCache

# use basic caching provided by Werkzeug Library
CACHE = SimpleCache(default_timeout=864000)

# create our application
app = Flask(__name__)
app.config.from_object("cs253.config")


def create_table_for(sql_schema):
    with contextlib.closing(connect_db()) as db:
        with app.open_resource(sql_schema, mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def init_db():
    create_table_for("schema/ascii_art_schema.sql")
    create_table_for("schema/blog_schema.sql")
    create_table_for("schema/users_schema.sql")


def connect_db():
    return sqlite3.connect(app.config["DATABASE"],
                           detect_types=sqlite3.PARSE_DECLTYPES |
                                        sqlite3.PARSE_COLNAMES)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()


def get_ip_address():
    if app.config.get("PYTHONANYWHERE"):
        ip_address = request.headers.get("X-Forwarded-For")
    else:
        ip_address = request.remote_addr
    return str(ip_address)


from apps.index import index
from apps.birthday.birthday import birthday
from apps.rot13.rot13 import rot13
from apps.ascii_chan.ascii_chan import ascii_chan
from apps.user_auth.user_auth import user_auth
from apps.blog import blog

app.register_blueprint(index, url_prefix="/")
app.register_blueprint(birthday, url_prefix="/cs253")
app.register_blueprint(rot13, url_prefix="/cs253")
app.register_blueprint(ascii_chan, url_prefix="/cs253/ascii-chan")
app.register_blueprint(user_auth, url_prefix="/cs253/blog")
app.register_blueprint(blog, url_prefix="/cs253/blog")
