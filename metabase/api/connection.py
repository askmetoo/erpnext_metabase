'''
	Middleware between two endpoints
'''

import json
import requests
import urllib
import datetime
import httplib2
import frappe
from frappe import _, msgprint, throw

class Connection(object):
	
	def __init__(self, url, token=None, usr=None, pwd=None):
		
		if not(token or usr and pwd):
			throw(_("Please provide [Token]/[Username, Password]"))
		self.url = url
		if token:
			self.token = token
		elif usr and pwd:
			self.token = self.get_user_token(usr, pwd)
		self.update_token()

	def init_sess(self):
		self.sess = requests.Session()
		self.sess.headers.update({
			"content-type":"application/json",
		})
	
	def update_token(self):
		# Update headers to default
		self.sess.headers.update({
			"X-Metabase-Session": self.token 		
		})
			
	def send_request(self, method, api, data={}, params={}, headers={}):
		self.is_metabase_website_active()
		try:
			res = None
			method = method.upper()
			req_url = self.get_request_url(api, params)
			data = json.dumps(data) if data else {}
			
			if method == "GET":
				res = self.get_request(req_url, data=data, headers=headers)
			elif method == "POST":
				res = self.post_request(req_url, data=data, headers=headers)
			elif method == "PUT":
				res = self.put_request(req_url, data=data, headers=headers)
			elif method == "DELETE":
				res = self.delete_request(req_url, data=data, headers=headers)
			else:
				raise ValueError(_("Invalid Method"))
		
			return self.handle_response(res)
	
		except ValueError as e:
			print(e)
			print(frappe.get_traceback())
		except Exception as e:
			print (e)
			print (frappe.get_traceback())

	def get_request(self, url, data={}, headers={}):
		return self.sess.get(url, data=data, headers=headers)	

	def post_request(self, url, data={}, headers={}):
			
		return self.sess.post(url, data=data, headers=headers)

	def put_request(self, url, data={}, headers={}):

		return self.sess.put(url, data=data, headers=headers)

	def delete_request(self, url, data={}, headers={}):

		return self.sess.delete(url, data=data, headers=headers)

	def get_request_url(self, api, params={}):
		url = self.url
		if not self.url[0:4] == "http":
			url = "http://{url}".format(url=self.base_url)
	
		url = url.strip("/")
		api = api.strip("/")
		req_url = "{url}/api/{api}".format(url=url, api=api)
		if params:
			req_url = req_url + "?"+urllib.quote(params)
		return req_url				
	
	def handle_response(self, res):
		if res.status_code >= 400 and res.status_code <= 451:
			frappe.throw(_("Client Error {0} \n {1}:".format(res.status_code, res.json())))
		elif res.status_code >= 500 and res.status_code <= 511:
			frappe.throw(_("Server Error {0} \n {1}:".format(res.status_code, res.json()))) 	
		return res.json()

	def update_sess_headers(self, key, val):
		self.sess.headers.update({key:val})


	def is_metabase_website_active(self):
	
		try:	
			http = httplib2.Http()
			res, content = http.request(self.setting.url, "HEAD")
			if res.status > 400:
				ValueError("Website {0} isn't accessible.".format(self.setting.url))		
		except Exception as e:
			raise Exception("Website {0} isn't accessible".format(self.setting.url))

	def get_user_token(self, usr, pwd):
		api = "api/session"
		res = self.send_request("GET", api)
		if not res:
			return None
		return res.get("id")

	def get_setup_token(self):
		api = "api/session/properties"
		res = self.send_request("GET", api)
		if not res:
			return None	
		return res.get("setup_token")

	
class BaseAuthentication(Connection):
	

	def __init__(self, url, token=None, usr=None, pwd=None, is_setup=False):
		self.init_sess()
		if is_setup:
			self.url = url
			token = self.get_setup_token()
		self.is_metabase_website_active()
		super(BaseAuthentication, self).__init__(url, token, usr, pwd)
			

