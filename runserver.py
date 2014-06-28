#!/usr/bin/python
# -*- coding: utf-8 -*-

from cs253 import app

if not app.config.get('PYTHONANYWHERE'):
    app.run()
