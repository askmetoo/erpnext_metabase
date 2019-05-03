
import frappe
from frappe.utils.password import get_decrypted_password


def get_user_password(username=False, is_admin=False):
	password = None
	if is_admin:
		username = frappe.db.get_single_value("Metabase Setting", "admin")
		if not frappe.db.get_value("Metabase User", username):
			create_user(username)
		
	return get_decrypted_password("Metabase User", username, "password", raise_exception=False)


'''
	Create Metabase user for auto login
'''
def create_user(username):
	m_user = frappe.get_doc({

		"user": username, "password": frappe.generate_hash(),
		"email": username, "doctype": "Metabase User"
	})
	m_user.save(ignore_permissions=True)
	frappe.db.commit()	



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
		print(res.json().get("setup_token"))
	except Exception as e:
		print(e)
		frappe.msgprint("text = {0}".format(res.text))
	
