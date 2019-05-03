# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tablix and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import jwt
from frappe.utils import cint, flt, cstr

class Dashboard(Document):
	
	def validate(self):
		self.__setting =  frappe.get_doc("Metabase Setting", "Metabase Setting")
		
		self.update_url()
	
	def update_url(self):
	
		self.url = self.__setting.url
		key = self.__setting.embedded_token
		print(key)
		payload = {"resource": {"dashboard":cint(self.dashboard_id)}, "params": {}}
		token = jwt.encode(payload, key, algorithm="HS256").decode("utf8")
					
		self.iframe_url = "{url}/embed/dashboard/{token}{theme}".format(url=self.url, token=token, \
				theme=self.__setting.embedded_theme_setting)
	





def save_dashboard(data):
	
	if not data:
		return
	if isinstance(data, dict):
		data = [data]
	for dashboard in data:
		doc = None
		if frappe.db.get_value("Dashboard", {"dashboard_id":dashboard.get("id")}):
			val = frappe.db.get_value("Dashboard", {"dashboard_id": dashboard.get("id")}, \
				as_dict=True)
			doc = frappe.get_doc("Dashboard", val.get("name"))
		else:
			doc = frappe.get_doc({
				"doctype": "Dashboard", "dashboard_name": dashboard.get("name"),
				"dashboard_id": dashboard.get("id"), "creator_id": \
				dashboard.get("creator_id"), "created_at": dashboard.get("created_at"),
			})
		doc.dashboard_name = dashboard.get("name")
		doc.favorite = dashboard.get("favorite")
		doc.enable_embedding = dashboard.get("enable_embedding")
		doc.position = dashboard.get("position")
		doc.public_uuid = dashboard.get("public_uuid")
		doc.made_public_by_id = dashboard.get("made_public_by_id")
		doc.save(ignore_permissions=True)
		
	frappe.db.commit()
		
