#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import hmac
import random
import string

from cs253.config import SECRET_KEY

###############################################################################
## Password Hashing and Salting ###############################################
###############################################################################


def make_random_salt(length=5):
    return "".join(random.choice(string.letters) for _ in xrange(length))


def make_pw_hash(name, pw, salt=None):
    if salt is None:
        salt = make_random_salt()
    computed_hash = hashlib.sha256(name + pw + salt).hexdigest()
    return "{0}|{1}".format(computed_hash, salt)


def valid_pw(name, pw, computed_hash):
    salt = computed_hash.split("|")[1]
    return computed_hash == make_pw_hash(name, pw, salt)


###############################################################################
## Cookie Hashing #############################################################
###############################################################################


def hash_cookie(cookie_value):
    return hmac.new(SECRET_KEY, cookie_value).hexdigest()


def make_secure_cookie(cookie_value):
    return "{0}|{1}".format(cookie_value, hash_cookie(cookie_value))


def check_secure_cookie(hashed_string):
    if hashed_string is not None:
        cookie_value = hashed_string.split("|")[0]
        if hashed_string == make_secure_cookie(cookie_value):
            return cookie_value
