#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import re

from flask import (Blueprint, g, make_response, redirect, render_template,
                   request, url_for)

import cs253.lib.utils as utils

user_auth = Blueprint("user_auth", __name__)

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_REGEX = re.compile(r"^.{3,20}$")
EMAIL_REGEX = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def valid_signup_username(username):
    return username and USERNAME_REGEX.match(username)


def valid_signup_password(password):
    return password and PASSWORD_REGEX.match(password)


def valid_signup_email(email):
    # Since email is optional, either don't provide an email at all,
    # or else, provide a valid email.
    return not email or EMAIL_REGEX.match(email)


def validate_signup_form(username, password, verify, email):
    error_in_form = False
    signup_params = dict(username=username,
                         email=email)
    if not valid_signup_username(username):
        signup_params["username_errormsg"] = "That's not a valid username."
        error_in_form = True
    if not valid_signup_password(password):
        signup_params["password_errormsg"] = "That's not a valid password."
        error_in_form = True
    elif password != verify:
        signup_params["verify_errormsg"] = "Your passwords didn't match."
        error_in_form = True
    if not valid_signup_email(email):
        signup_params["email_errormsg"] = "That's not a valid email."
        error_in_form = True
    return error_in_form, signup_params


def query_user_by_name(username):
    cur = g.db.execute("SELECT * FROM users WHERE username = ?", [username])
    return cur.fetchone()


def query_user_by_id(user_id):
    cur = g.db.execute("SELECT * FROM users WHERE id = ?", [user_id])
    return cur.fetchone()


def add_user_to_db(username, secure_password, email=None):
    current_time = datetime.datetime.utcnow()
    db_query = ("INSERT INTO users (username, password, creation_date, email) "
                "VALUES (?, ?, ?, ?)")
    db_query_parameters = [username, secure_password, current_time, email]
    g.db.execute(db_query, db_query_parameters)
    g.db.commit()


def successful_login_response(user):
    user_id = str(user[0])
    user_cookie = utils.make_secure_cookie(user_id)
    my_response = make_response(redirect(url_for("user_auth.user_welcome")))
    my_response.set_cookie("user_id", user_cookie)
    return my_response


@user_auth.route("/signup", methods=["GET", "POST"])
def user_signup():
    signup_params = dict()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        verify = request.form.get("verify")
        email = request.form.get("email")
        validation = validate_signup_form(username, password, verify, email)
        error_in_form, signup_params = validation
        if not error_in_form:
            user_exists = query_user_by_name(username)
            if not user_exists:
                secure_password = utils.make_pw_hash(username, password)
                add_user_to_db(username, secure_password, email)
                user = query_user_by_name(username)
                return successful_login_response(user)
            else:
                signup_params["username_errormsg"] = "User already exists."
    return render_template("user_signup.html", **signup_params)


@user_auth.route("/welcome")
def user_welcome():
    user_cookie = request.cookies.get("user_id")
    user_id = utils.check_secure_cookie(user_cookie)
    if not user_id:
        return redirect(url_for("user_auth.user_signup"))
    username = query_user_by_id(user_id)[1]
    return render_template("user_welcome.html", username=username)


@user_auth.route("/login", methods=["GET", "POST"])
def user_login():
    login_errormsg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = query_user_by_name(username)
        if user:
            stored_password = user[2]
            if utils.valid_pw(username, password, stored_password):
                return successful_login_response(user)
        login_errormsg = "Invalid login"
    return render_template("user_login.html", login_errormsg=login_errormsg)


@user_auth.route("/logout")
def user_logout():
    my_response = make_response(redirect(url_for("user_auth.user_signup")))
    my_response.set_cookie("user_id", "")
    return my_response
