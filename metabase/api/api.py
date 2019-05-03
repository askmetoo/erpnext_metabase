
import frappe
from frappe import _, msgprint, throw
from metabase.api import connection
from metabase.api.resources import *
import sys

class MetabaseAPI(connection.BaseAuthentication):
	
	def __init__(self, token=None, usr=None, pwd=None, is_setup=None):
		self.setting = frappe.get_doc("Metabase Setting", "Metabase Setting")
		super(MetabaseAPI, self).__init__(self.setting.url, token, usr, pwd, is_setup)

	def __getattr__(self, item):
		
		return ResourceWrapper(item, self)



class ResourceWrapper(object):
	
	def __init__(self, resource_class, api):
		if isinstance(resource_class, basestring):
			self.resource_class = self.str_to_class(resource_class)

		else:
			self.resource_class = resource_class
	
		self.api = api

	def str_to_class(self, resource_class):
		
		return getattr(sys.modules[__name__], resource_class)
	
	def __getattr__(self, item):
		
		return lambda *args, **kwargs: (getattr(self.resource_class, item))(*args, api=self.api, **kwargs)
			

'''
if __name__ == "__main__":
	MetabaseAPI()	
'''
