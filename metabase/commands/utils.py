'''
	Developer Navdeep Singh
	Emial navdeepghai1@gmail.com
'''

import click, frappe
import os, subprocess, pwd, grp
from frappe import throw, _
from frappe.commands import pass_context, get_site


@click.command("install-java")
@pass_context
def install_java(context):

	out, ins = is_java_installed()
	if not ins:
		print(out)
		if os.getuid() != 0:
			pass
		print(os.getuid())

def is_java_installed():
	output = ""
	flag = False
	try:
		output = subprocess.call(["java", "--version"])
		flag = True	
	except OSError as e:
		output = _("Java not found")

	return output, flag


@click.command("generate-metabase-file")
@pass_context
def generate_metabase_file(context):
	
	site = get_site(context)
	frappe.init(site=site)
	frappe.connect()
	setting = frappe.get_doc("Metabase Setting", "Metabase Setting")
	host = "localhost" if setting.get("is_same_host") else setting.get("host_name")
	port_no = setting.get("port_no")	
		
	template = frappe.get_template("templates/config/metabase.conf")
	conf  = template.render({"port_no": port_no, "host": host})
	print(conf)	
	with open("metabase.conf", "rw+") as f:
		pass	
