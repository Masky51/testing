from __future__ import unicode_literals
import frappe
from frappe import auth
from frappe import _
from datetime import datetime
import geocoder
import requests
import base64
import os
import binascii

@frappe.whitelist( allow_guest=True )
def login(usr, pwd):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key":0,
            "message":"Authentication Error!"
        }

        return

    api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)

    frappe.response["message"] = {
        "success_key":1,
        "message":"Authentication success",
        "sid":frappe.session.sid,
        "api_key":user.api_key,
        "api_secret":api_generate,
        "username":user.username,
        "email":user.email
    }


def generate_keys(user):
    user_details = frappe.get_doc('User', user)
    api_secret = frappe.generate_hash(length=15)

    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key

    user_details.api_secret = api_secret
    user_details.save()

    return api_secret


# FINAL METHOD 

@frappe.whitelist()
def update_audit():
    # Retrieve data from the request
    data = frappe.request.json

    # Perform data validation and processing as required
    asset_id = data.get('asset_name')
    location = data.get('location_name')
    date_time_obj = datetime.now()
    image_link = data.get('image')

    # Fetch current location using geocoder
    g = geocoder.ip('me')
    # location = g.city
    coordinates = ','.join(map(str, g.latlng))

    image_data = fetch_image_data(image_link)

    converted_image = decrypt_image_data(image_data)
    # Check if the document already exists based on the asset ID
    existing_doc = frappe.get_doc('audit_details', {'asset_name': asset_id})

    if existing_doc:
        # Update the existing document
        existing_doc.location_name = location
        existing_doc.time = date_time_obj
        existing_doc.image = image_link
        existing_doc.coordinates = coordinates
        existing_doc.encryption = image_data
        existing_doc.preview = converted_image
        existing_doc.save()
        doc = existing_doc
    else:
        # Return an error response if the document does not exist
        return {
            'status': 'error',
            'message': 'Audit details not found',
            'data': None
        }
      
    # Return a response
    return {
        'status': 'success',
        'message': 'Audit details saved successfully',
        'data': doc.as_dict()       
    }

def fetch_image_data(image_link):
    if image_link.startswith(('http://', 'https://')):
        # Fetch image from web URL
        response = requests.get(image_link)
        image_content = response.content
    else:
        # Read image from local file path
        if not os.path.isabs(image_link):
            # If the path is relative, make it absolute
            image_link = os.path.join(frappe.get_site_path('public'), image_link)
        with open(image_link, 'rb') as f:
            image_content = f.read()

    # Add the prefix to the base64 encoded image data
    image_data = "data:image/png;base64," + base64.b64encode(image_content).decode('utf-8')
    return image_data


def decrypt_image_data(image_data):
    try:
        converted_image = base64.b64decode(image_data)
        return converted_image
    except binascii.Error:
        # If base64 decoding fails, assume the prefix is missing and try decoding without it
        try:
            converted_image = base64.b64decode(image_data[len("data:image/png;base64,"):])
            return converted_image
        except binascii.Error:
            # If decoding still fails, return None or handle the error as needed
            return None
