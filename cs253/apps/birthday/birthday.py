#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, render_template, request, url_for

birthday = Blueprint("birthday", __name__, template_folder="templates")

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
          "Nov", "Dec", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if 1 <= day <= 31:
            return day


def valid_month(month):
    if month.capitalize() in MONTHS:
        return month.capitalize()


def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if 1850 <= year <= 2020:
            return year


@birthday.route("/birthday-form", methods=["GET", "POST"])
def birthday_form():
    day, month, year, error_msg = "", "", "", ""
    if request.method == "POST":
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")
        if valid_day(day) and valid_month(month) and valid_year(year):
            return redirect(url_for("birthday.birthday_thanks"))
        else:
            error_msg = "That doesn't look like a valid date to me."
    return render_template("birthday_form.html", error=error_msg, day=day,
                           month=month, year=year)


@birthday.route("/birthday-thanks")
def birthday_thanks():
    title_text = "Birthday Thanks"
    body_text = "Thanks! That's a totally valid day."
    return render_template("base.html", title_text=title_text,
                           body_text=body_text)
