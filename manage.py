#!/usr/bin/env python
# -*- coding: utf-8 -

import random as _random

from peewee import *

from myapp import app
from myapp.otp import db, User

from flask.ext.script import Manager, prompt

manager = Manager(app)

issuer = "OTPAuth"


def random_base32(length=16, random=_random.SystemRandom(), chars=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')):
    return ''.join(random.choice(chars) for _ in range(length))


def emergency(length=8, random=_random.SystemRandom(), chars=list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')):
    return ''.join(random.choice(chars) for _ in range(length))


@manager.command
def initdb():
    """ Init db"""

    try:
        db.create_tables([User])
    except Exception, e:
        print "Unexpected error: %s" % e


@manager.command
def useradd(login=None, count=5):
    """ Add a user"""

    secret = random_base32()

    if login is None:
        login = prompt("Login: ")

    emergency_list = ','.join(emergency() for _ in range(count))

    try:
        User.create(login=login, secret=secret, emergency=emergency_list)

        print "Scan QR: http://2qr.ru/otpauth://totp/%(issuer)s:%(login)s?secret=%(secret)s&issuer=%(issuer)s" % (
            {'issuer': issuer, 'login': login, 'secret': secret})

        print "Or add manually SECRET KEY: %s" % secret
        print "Emergency codes: %s" % emergency_list
    except Exception, e:
        print "Unexpected error: %s" % e


@manager.command
def userdel(login=None):
    """ Remove a user"""

    if login is None:
        login = prompt("Login: ")

    try:
        user = User.get(User.login == login)
        user.delete_instance()
        print "User has been deleted"
    except User.DoesNotExist:
        print "User not found"
    except Exception, e:
        print "Unexpected error: %s" % e


@manager.command
def userlist():
    """ List all users"""

    try:
        for user in User.select():
            print user.login
    except Exception, e:
        print "Unexpected error: %s" % e


@manager.command
def renew(login=None, count=5):
    """ Renew a emergency codes"""

    if login is None:
        login = prompt("Login: ")

    emergency_list = ','.join(emergency() for _ in range(int(count)))

    try:
        user = User.get(User.login == login)
        user.emergency = emergency_list
        user.save()
    except User.DoesNotExist:
        print "User not found"
    except Exception, e:
        print "Unexpected error: %s" % e
    else:
        print "Emergency codes: %s" % emergency_list

if __name__ == "__main__":
    manager.run()
