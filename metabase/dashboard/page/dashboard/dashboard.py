
import frappe
from frappe import _, msgprint, throw
from frappe.utils import cint, flt, cstr
import datetime

@frappe.whitelist()
def get_embeddable_dashboard(name):
	# Later need to apply user permissions	
	return frappe.db.get_value("Dashboard", {"enable_embedding": 1, "name":name },\
		 fieldname=["iframe_url"], as_dict=True)
		
