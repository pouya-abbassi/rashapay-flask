#! /usr/bin/python3.5
# -*- coding: UTF-8 -*-

##############################
# http://rashapay.com
# https://github.com/pouya-abbassi/rashapay-py
# By Pouya Abbassi
# This source code is built for easy-pay service.
# No database and no callback url. Best to use for donation (that you don't want to restore user data and how much they pay) and learning cases.
##############################

__author__ = "Pouya Abbassi"
__copyright__ = "Copyright 2016, http://RashaPay.com"
__credits__ = ["Nima Barzegar"]
__license__ = "GPL-v3 https://www.gnu.org/licenses/gpl-3.0.en.html"
__version__ = "0.1.0"
__maintainer__ = "Pouya Abbassi"
__status__ = "Production"


from flask import Flask
import urllib               # Used for sending request to rashapay webservice
import json                 # Used for parsing json object
import random               # Used for generating random orderID
app = Flask(__name__)

consumer_key = "1234:5678"			# Copy the Ckey of your website from (http://rashapay.com//userpanel.php?action=listofsites)
amount = "1000"					# Integer, Min 1000 (rials)
email = "info@mail.com"				# Buyer Email (Bank may send an email to confirm payment)
name = "Buyer"					# Buyer name
orderid = random.randint(1,99999999999)		# Just a random integer as orderID
callback = "http://localhost/callback"		# User will redirected here after payment
mobile = "09120000000"				# Buyer phone number
description = "Description"			# Max 200 characters

@app.route("/")
def index():
    return '<meta charset="utf-8"><style>*{direction:rtl;text-align:right;}</style><h1>ماژول پایتون درگاه پرداخت راشاپی</h1><form method="post"action="request"accept-charset="UTF-8"enctype="application/x-www-form-urlencoded"autocomplete="off"><table><tr><td>مبلغ پرداختی:</td><td><input type="text"name="amount"value="1000"></td></tr><tr><td>نام:</td><td><input type="text"name="name"></td></tr><tr><td>ایمیل:</td><td><input type="text"name="email"></td></tr><tr><td>موبایل:</td><td><input type="text"name="mobile"></td></tr><tr><td>توضیحات:</td><td><textarea name="description" rows="10" cols="30"></textarea></td></tr><tr><td></td><td><input type="submit"value="پرداخت"></td></tr></form>'

@app.route("/request", methods=['POST'])
def request():
    return "Hello World!!!!!"

if __name__ == "__main__":
    app.run()
