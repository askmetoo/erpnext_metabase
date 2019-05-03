
import frappe
from .api.utils import get_user_password

def update_boot_session(context):

	context.update({
		"metabase": {
			"user_info": get_user_info(),
			"setting": frappe.get_doc("Metabase Setting", "Metabase Setting")
		}
	})



def get_user_info():
	
	user_info =  frappe.db.get_value("Metabase User", frappe.session.user, ["email"], as_dict=True)
	if not user_info and frappe.session.user=="Administrator":
		metabase_setting = frappe.get_doc("Metabase Setting", "Metabase Setting")
		user_info = frappe.db.get_value("Metabase User", metabase_setting.get("admin"), ["email"], as_dict=True)	
		

	if user_info:
		user_info.update({"info": get_user_password(user_info.get("email"))})	
	return user_info
