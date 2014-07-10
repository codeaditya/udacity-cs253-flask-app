#!/usr/bin/python
# -*- coding: utf-8 -*-

from werkzeug.contrib.cache import SimpleCache

# use basic caching provided by Werkzeug Library
CACHE = SimpleCache(default_timeout=864000)
