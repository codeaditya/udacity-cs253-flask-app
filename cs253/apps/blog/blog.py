#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

from flask import (Blueprint, Markup, abort, g, jsonify, redirect, request,
                   render_template, url_for)

from cs253.cache import CACHE

blog = Blueprint("blog", __name__, template_folder="templates")


def last_post_id():
    cur = g.db.execute("SELECT * FROM blog ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    return str(row[0])


def query_blog_frontpage(update=False):
    cache_key = "blog_frontpage"
    db_query = "SELECT * FROM blog ORDER BY id DESC LIMIT 10"
    db_query_parameters = []
    return cached_blog_query(cache_key, db_query, db_query_parameters, update)


def query_blog_page(page_no, update=False):
    cache_key = "page_" + str(page_no)
    last_id = int(last_post_id())
    entry_per_page = 10
    last_post = last_id - (page_no - 1) * entry_per_page
    first_post = last_post - entry_per_page + 1
    db_query = "SELECT * FROM blog WHERE id <= ? AND id >= ? ORDER BY id DESC"
    db_query_parameters = [last_post, first_post]
    return cached_blog_query(cache_key, db_query, db_query_parameters, update)


def query_post_permalink(post_id, update=False):
    cache_key = "post_" + str(post_id)
    db_query = "SELECT * FROM blog WHERE id = ?"
    db_query_parameters = [int(post_id)]
    return cached_blog_query(cache_key, db_query, db_query_parameters, update)


def cached_blog_query(cache_key, db_query, db_query_parameters, update):
    posts = CACHE.get(cache_key)
    if (posts is None) or update:
        cur = g.db.execute(db_query, db_query_parameters)
        post_list = [dict(id=row[0], subject=row[1], content=row[2],
                          created=row[3].strftime("%a, %d %b %Y %H:%M:%S GMT"))
                     for row in cur.fetchall()]
        update_time = time.time()
        posts = (post_list, update_time)
        CACHE.set(cache_key, posts)
    return posts_with_age(posts)


def posts_with_age(posts):
    post_list, update_time = posts
    query_age = str(int(time.time() - update_time))
    return post_list, query_age


def write_blog_page(post_list, query_age, prev_page_no=None, next_page_no=None,
                    front_page=False):
    for item in post_list:
        escaped_content = ""
        for line in item.get("content").splitlines():
            escaped_content += Markup.escape(line) + Markup("<br>")
        item["content"] = escaped_content
        if item.get("id") == 1:
            next_page_no = None
    if not post_list and not front_page:
        return abort(404)
    else:
        blog_page_params = dict(
            post_list=post_list,
            query_age=query_age,
            prev_page_no=prev_page_no,
            next_page_no=next_page_no,
        )
        return render_template("blog_page.html", **blog_page_params)


@blog.route("/flush")
def flush_cache():
    CACHE.clear()
    return redirect(url_for("blog.blog_frontpage"))


@blog.route("/")
def blog_frontpage():
    post_list, query_age = query_blog_frontpage()
    return write_blog_page(post_list, query_age, next_page_no="2",
                           front_page=True)


@blog.route("/post/<int:post_id>")
def post_permalink(post_id):
    post_list, query_age = query_post_permalink(post_id)
    return write_blog_page(post_list, query_age)


@blog.route("/page/<int:page_no>")
def blog_page(page_no):
    if page_no == 1:
        return redirect(url_for("blog.blog_frontpage"))
    next_page_no = str(page_no + 1)
    prev_page_no = str(page_no - 1)
    if int(prev_page_no) < 1:
        prev_page_no = None
    post_list, query_age = query_blog_page(page_no)
    return write_blog_page(post_list, query_age, prev_page_no, next_page_no)


@blog.route("/.json")
def jsonify_blog_frontpage():
    post_list, query_age = query_blog_frontpage()
    return jsonify(posts=post_list, query_age=query_age)


@blog.route("/post/<int:post_id>.json")
def jsonify_post_permalink(post_id):
    post_list, query_age = query_post_permalink(post_id)
    return jsonify(posts=post_list, query_age=query_age)


@blog.route("/newpost", methods=["GET", "POST"])
def blog_newpost():
    subject, content, errormsg = "", "", ""
    if request.method == "POST":
        subject = request.form.get("subject")
        content = request.form.get("content")
        if subject and content:
            current_time = datetime.datetime.utcnow()
            db_query = ("INSERT INTO blog (subject, content, posted) "
                        "VALUES (?, ?, ?)")
            db_query_parameters = [subject, content, current_time]
            g.db.execute(db_query, db_query_parameters)
            g.db.commit()
            post_id = last_post_id()
            query_blog_frontpage(update=True)
            query_post_permalink(post_id, update=True)
            # TODO update/invalidate CACHE for all /page/<int:page_no>
            return redirect(url_for("blog.post_permalink", post_id=post_id))
        else:
            errormsg = "We need both Subject and Content"
    return render_template("blog_newpost.html", subject=subject,
                           content=content, errormsg=errormsg)
