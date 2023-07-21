# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from erpnext.custom_utils import create_item

class WorkSpaceFurniture(Document):
	def after_insert(self):
		create_item(self)
       
        
