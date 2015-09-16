# -*- coding: utf-8 -

from flask import Flask
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
app.secret_key = '\xe7\x16\x06\xc7\xe8\xc7\xae\xb9\x94y\x0f\xbc\x06t{\xd0\xa2\xce/\xf8H~7\x0e'
CsrfProtect(app)
# app.config.from_object('config')

import myapp.otp
