# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "metabase"
app_title = "Metabase"
app_publisher = "Tablix"
app_description = "Visual Charting "
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "navdeepghai1@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
	"/assets/js/metabase-min.css"
]
app_include_js = [
	"/assets/js/metabase-min.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/metabase/css/metabase.css"
# web_include_js = "/assets/metabase/js/metabase.js"
after_install = "metabase.install.after_install"
before_install = "metabase.install.before_install"
# include js in page
# page_js = {"page" : "public/js/file.js"}
update_website_context = "metabase.website.website_context.update_website_context"
boot_session = "metabase.boot_session.update_boot_session"

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "metabase.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "metabase.install.before_install"
# after_install = "metabase.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "metabase.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
 	"all": [
 		"metabase.metabase.sync.start_sync"
 	],
}

jenv = {
	"add_extension":  "metabase.utils.jinja2.update_jinja_extension"
}
# Testing
# -------

# before_tests = "metabase.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "metabase.event.get_events"
# }

