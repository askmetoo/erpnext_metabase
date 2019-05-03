# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tablix and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from frappe.utils import cint, cstr, flt, now_datetime
from frappe import _, msgprint, throw
from metabase.api.utils import get_user_password
from metabase.api.api import MetabaseAPI
from datetime import timedelta

class MetabaseSetting(Document):

	def validate(self):
		
		if not self.get("admin"):
			throw(_("Please select Admin"))
		self.validate_port_no_and_host()
		self.create_admin_user()

	def validate_port_no_and_host(self):
		if not self.get("port_no") or not self.get("host_name"):
			frappe.throw(_("Port name and host names are mandatory"))	
		self.set_url()

	def set_url(self):
		self.url = "{0}{1}:{2}".format(self.get_scheme(), self.get_host_name(),
				 self.get_port_no())	
			
	
	def get_host_name(self):
		origin = frappe.local.request.headers.get("Origin")
		host_name = frappe.local.request.headers.get("Host")
		if not self.is_same_host:
			host_name = self.host_name
		
		host_name = host_name.strip("https://|http://")	
		if host_name.find(":") >= 0:
			host_name = host_name[0: host_name.rfind(":")+1]
		return host_name
				
		
	def get_port_no(self):
	
		return self.port_no

	def get_scheme(self):
		origin = frappe.local.request.headers.get("Origin")
		scheme = "http://"
		if self.is_same_host and "https" in origin:
			scheme = "https://"
		elif not self.is_same_host and "https" in self.host_name:
			scheme = "https://"
		
		return scheme	
	
	def create_admin_user(self):
		if not frappe.db.get_value("Metabase User", self.get("admin")):
			admin = frappe.get_doc({
				"email": self.admin, "user": self.admin,
				"password": frappe.generate_hash(),
				"doctype": "Metabase User",	
			})
			admin.save(ignore_permissions=True)
	
			

@frappe.whitelist()
def setup_metabase(frm):
	setting = frappe.get_doc("Metabase Setting", "Metabase Setting")
	password = get_user_password(username=None, is_admin=True)
	config = get_database_config(setting)
	if setting.get("setup_complete"):
		return frappe.msgprint(_("Setup has already been completed"))

	metabase = MetabaseAPI(is_setup=True)
	config.update({"token": metabase.token})
	user_info = metabase.send_request("POST", "api/setup", data=config)
	user = frappe.get_doc("Metabase User", setting.get("admin"))
	user.session_token = user_info.get("id")
	setting.session_token = user_info.get("id")
	setting.token_expiry_date = now_datetime()+timedelta(days=13)
	user.session_expire_on = now_datetime()+timedelta(days=13)
	user.save()
	setting.save()
	frappe.db.commit()
				


def get_database_config(setting):

	conf = frappe.get_conf()
	
	m_user = frappe.get_doc("Metabase User", setting.get("admin"))
	return {
		"user":{
			"email": setting.get("email"),
			"first_name": setting.get("first_name"),
			"last_name": setting.get("last_name"),
			"password": m_user.get_password(raise_exception=False)
			
		},
		"database":{
			"engine": "mysql",
			"name": "ERP-Metabase Database",
			"details": {
				"dbname": conf.get("db_name"),
				"host": "localhost","port": 3306,
				"password": conf.get("db_password"),
				"user": conf.get("db_name")
			}
		},
		"prefs": {
			"site_name": "Tablix"
		},
	}



