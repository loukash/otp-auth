# -*- coding: utf-8 -

from flask import Flask
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
app.config.from_object('config')
CsrfProtect(app)

import myapp.otp
