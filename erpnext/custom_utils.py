import frappe
    
def create_item(doc):
    # Create a new Item document
    item = frappe.get_doc({
        "doctype": "Item",
        "item_code": doc.brand +" "+ doc.model_name,
        "item_group": doc.category_group,
        "is_fixed_asset": 1,
        "is_stock_item": 0,
        "asset_category": doc.category_group,
        # Map other relevant fields from the source doctype to the Item doctype
    })
    item.insert()
