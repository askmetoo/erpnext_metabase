
import frappe
from frappe import _, throw
from frappe.utils import cint, cstr, now_datetime
from metabase.api.api import MetabaseAPI

@frappe.whitelist()
def start_sync():
	
	setting = frappe.get_doc("Metabase Setting", "Metabase Setting")
	api =  MetabaseAPI(setting.session_token)
	sync_embeddable_links(api)	


def sync_embeddable_links(api):
	from metabase.dashboard.doctype.dashboard.dashboard import save_dashboard
	save_dashboard(api.Dashboard.get())
