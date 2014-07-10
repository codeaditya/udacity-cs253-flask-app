#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import time
import urllib2

from flask import Blueprint, g, redirect, render_template, request, url_for

from cs253 import get_ip_address
from cs253.cache import CACHE
from cs253.config import IPINFODB_API_KEY1

ascii_chan = Blueprint("ascii_chan", __name__, template_folder="templates")

IPINFODB_URL = "http://api.ipinfodb.com/v3/ip-city/?key={0}&format=json&ip=" \
               "".format(IPINFODB_API_KEY1)
GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=450x400&sensor=false"


def get_coords(ip):
    url = IPINFODB_URL + str(ip)
    try:
        content = json.load(urllib2.urlopen(url))
    except urllib2.URLError:
        return
    else:
        latitude = str(content.get("latitude"))
        longitude = str(content.get("longitude"))
        if float(latitude) and float(longitude):
            return latitude + "," + longitude


def gmaps_img_for(points):
    url = GMAPS_URL
    for point in points:
        url += "&markers={0}".format(point)
    return url


def query_latest_arts(update=False):
    key = "ascii_arts_latest"
    arts = CACHE.get(key)
    if (arts is None) or update:
        db_query = "SELECT * FROM ascii_art ORDER BY created DESC LIMIT 10"
        cur = g.db.execute(db_query)
        art_list = [dict(title=row[1], art=row[2],
                         created=row[3], coords=row[4])
                    for row in cur.fetchall()]
        update_time = time.time()
        arts = (art_list, update_time)
        CACHE.set(key, arts)
    return arts


def add_art_to_db(title, art, coords=None):
    current_time = datetime.datetime.utcnow()
    db_query = ("INSERT INTO ascii_art (title, art, created, coords) "
                "VALUES (?, ?, ?, ?)")
    db_query_parameters = [title, art, current_time, coords]
    g.db.execute(db_query, db_query_parameters)
    g.db.commit()


def write_ascii_art_page(title="", art="", errormsg=""):
    arts = query_latest_arts()
    art_list = arts[0]
    update_time = arts[1]
    query_age = str(int(time.time() - update_time))
    points = []
    for item in art_list:
        coords = str(item.get("coords"))
        if coords != "" and coords.find("None") == -1:
            points.append(coords)
    img_url = None
    if points:
        img_url = gmaps_img_for(points)
    return render_template("ascii_chan.html", title=title, art=art,
                           errormsg=errormsg, img_url=img_url,
                           art_list=art_list, query_age=query_age)


@ascii_chan.route("/", methods=["GET", "POST"])
def ascii_chan_page():
    title, art, errormsg = "", "", ""
    if request.method == "POST":
        title = request.form.get("title")
        art = request.form.get("art")
        if title and art:
            coords = get_coords(get_ip_address())
            add_art_to_db(title, art, coords)
            query_latest_arts(update=True)
            return redirect(url_for("ascii_chan.ascii_chan_page"))
        else:
            errormsg = "We need both a title and some artwork!"
    return write_ascii_art_page(title=title, art=art, errormsg=errormsg)
