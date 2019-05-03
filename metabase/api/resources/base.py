'''
	Base for Every Request
'''

import frappe
from frappe import _, msgprint, throw
import requests
from frappe.utils import now_datetime, cint, cstr, flt
import json


class APIResource:
		
	resource_name = ""

	@classmethod
	def make_request(cls, method, api, data=None, params=None, headers=None):
		return api.send_request(method, cls.resource_name, data, params, headers)

	@classmethod
	def get(cls, api, data=None, params=None, headers=None):
		return cls.make_request("GET", api, data, params, headers)

	@classmethod
	def post(cls, api, data=None, params=None, headers=None):
		 return cls.make_request("POST", api, **kwargs)
	
	@classmethod
	def delete(cls, url, connection ,data=None, params=None, headers=None):
		return cls.make_request("DELETE", api, **kwargs)

	@classmethod
	def update(cls, url, connection, data=None, params=None, headers=None):
		return cls.make_request("PUT", api, **kwargs)


'''
def get_url():

	setting = frappe.get_doc("Metabase Setting", "Metabase Setting")
	
	if not setting.get("url") or not setting.get("port_no"):
		throw(_("Please enter URL and Port No. in Metabase Setting"))

	_url = ""
	url = setting.get("url")
	if url[0:4] == "http":
		_url = url
	else:
		_url = "http://{url}".format(url=url)	

	if url.rfind("/") == len(url)-1:
		_url = _url[0: len(_url)-1]
		_url = "{url}:{port_no}".format(url=_url,port_no=setting.get("port_no"))
	else:
		_url = "{url}:{port_no}".format(url=_url, port_no=setting.get("port_no"))
	return _url


def get_session():
	sess = requests.Session()
	# send always in json format only
	sess.headers.update({
		"Content-Type" : "application/json",	
	})	
	return sess

def send_request(method, path, data={}):

	# Path for instance should be "api/<resource_name>"
	sess = get_session()
	try:
		url = get_url()
		_path = ""
		if path[0:1] == "/":
			_path
		else:
			_path = "/{path}".format(path=path)
		_url = "{url}{path}".format(url=url, path=_path)
		data = json.dumps(data)
		res = sess.get(_url, data=data)
		frappe.msgprint("{res}".format(res=res.json()))
	except Exception as e:
		print e
		frappe.msgprint("text = {0}".format(res.text))
'''
				
