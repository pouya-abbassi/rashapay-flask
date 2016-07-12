#! /usr/bin/python2.7
# -*- coding: UTF-8 -*-

##############################
# http://rashapay.com
# https://github.com/pouya-abbassi/rashapay-flask
# By Pouya Abbassi
# This source code is built for Flask python microframework (http://flask.pocoo.org).
# The / just has a normal form that collects user data such as name and email. /request will check if everything is fine and will send user to the payment service. /callback will recieve payment status.
##############################

__author__ = "Pouya Abbassi"
__copyright__ = "Copyright 2016, http://RashaPay.com"
__credits__ = "Nima Barzegar"
__license__ = "GPL-v3 https://www.gnu.org/licenses/gpl-3.0.en.html"
__version__ = "0.1.0"
__maintainer__ = "Pouya Abbassi"
__status__ = "Production"


from flask import Flask, request, redirect	# The framework!
import urllib					# Used for sending request to rashapay webservice
import json					# Used for parsing json object
import random					# Used for generating random orderID
app = Flask(__name__)				# If you are a flask developer, you know what it means!

consumer_key = "1234:5678"			# Copy the Ckey of your website from (http://rashapay.com//userpanel.php?action=listofsites)
callback = "http://localhost/callback"		# User will redirected here after payment

@app.route("/")					# Generating the / page that just contains html form for sending user data to the "request" page
def index():
	return '<meta charset="utf-8"><style>*{direction:rtl;text-align:right;}</style><h1>ماژول پایتون درگاه پرداخت راشاپی</h1><form method="post"action="request"accept-charset="UTF-8"enctype="application/x-www-form-urlencoded"autocomplete="off"><table><tr><td>مبلغ پرداختی:</td><td><input type="text"name="amount"value="1000"></td></tr><tr><td>نام:</td><td><input type="text"name="name"></td></tr><tr><td>ایمیل:</td><td><input type="text"name="email"></td></tr><tr><td>موبایل:</td><td><input type="text"name="mobile"></td></tr><tr><td>توضیحات:</td><td><textarea name="description" rows="10" cols="30" maxlenght="200"></textarea></td></tr><tr><td></td><td><input type="submit"value="پرداخت"></td></tr></form>'

@app.route("/request", methods=['POST'])	# This page will get user data and sends request to the webservice
def req():
	orderid = str(random.randint(1,99999999999))	# Just a random integer as orderID
	amount = request.form['amount']			# Integer, Min 1000 (rials)
	email = request.form['email']			# Buyer Email (Bank may send an email to confirm payment)
	name = request.form['name']			# Buyer name
	mobile = request.form['mobile']			# Buyer phone number
	description = request.form['description']	# Max 200 character

	data = urllib.urlencode({"consumer_key":consumer_key,"amount":amount,"email":email,"name":name,"orderid":orderid,"callback":callback,"mobile":mobile,"description":description})	# Generating data for creating the request.
	u = urllib.urlopen("http://rashapay.com/srv/rest/rpaypaymentrequest", data)	# Sending data to the webservice url.

	obj = u.read()	# Reading received data
	parsed_json = json.loads(obj)	# Parsing json object

	if parsed_json['status'] == '11' :
		output = 'مشخصات ارسالی نادرست است.'								# Incorrect variables
	elif parsed_json['status'] == '12' :
		output = 'اتصال به وب‌سرویس ناموفق است.'							# Failed to connect to the WebService
	elif parsed_json['status'] == '13' :
		output = 'IP سایت درخواست دهنده با IP ثبت شده در سیستم مطابقت ندارد.'				# Your IP is not the same as what is stored in our DataBase
	elif parsed_json['status'] == '14' : 
		output = 'شماره‌ی سفارش ارسالی (order_id) تکراری است. لطفا دوباره امتحان کنید.'		# OrderID is not unique and was used before
	elif parsed_json['status'] == '15' :
		output = 'فرمت مبلغ نامعتبر است.'								# Price format is invalid
	elif parsed_json['status'] == '16' :
		output = 'فرمت ایمیل صحیح نیست.'								# Email format is invalid
	elif parsed_json['status'] == '17' :
		output = 'آدرس callback تعریف نشده است.'							# No CallBack url was declared
	elif parsed_json['status'] == 'response' :
		output = 0										    	# Everything is fine, Getting the "token" part of json data and appending it to the payment url
	else :
		output = str(parsed_json['status'])								# Contact us at http://rashapay.com//about.php?#contactus

	if output == 0 :
		return redirect("http://rashapay.com/srv/gatewaychannel/requestpayment/" + parsed_json['token'])	# Appending token to the webservice url to redirecting user to the payment page
	else :
		return output	# In case something went wrong

@app.route("/callback", methods=['post'])	# This page will check if transaction went well. Payment page of the bank will redirect user to this page.
def callback():
	if request.form['refid'] == '10' :	# If transaction was incompelete. (try again)
		return ('تراکنش ناتمام')
	else :
		orderid = request.form['orderid']	# Payment page used POST to give us details about transaction
		refid = request.form['refid']		# Same as above line

		data = urllib.urlencode({"consumer_key":consumer_key,"orderid":orderid,"refid":refid})	# Generating data for creating the request.
		u = urllib.urlopen("http://rashapay.com/srv/rest/rpaypaymentverify", data)	# Sending data to the webservice url.

		obj = u.read()	# Reading received data
		parsed_json = json.loads(obj)	# Parsing json object

		if parsed_json['status'] == 'response' :	# If webservice respond to our request
			if str(parsed_json['code']) == '0' :	# If payment went well
				return 'Order ID: ' + str(orderid) + '<br>The transaction was successful: ' + str(refid)
			else :					# if something went wrong and payment payment failed
				return 'Error code: ' + str(parsed_json['code']) + '<br>Order ID: ' + str(orderid) + ' failed.'
		else :						# If there was something wrong with our request
			return 'Error code: ' + str(parsed_json['status']) + '<br>Order ID: ' + str(orderid) + ' failed.'


@app.route("/test")	# /test is just for testing. Sends some data to /callback to see what will happen.
def test():
	return '<form action="callback" method="post"><input type="text" name="consumer_key" value="2435:1861"><input type="text" name="orderid" value="21826051646"><input type="text" name="refid" value="117389035664"><button></button></form>'


if __name__ == "__main__":	# Modularity is the key!
	app.run()
