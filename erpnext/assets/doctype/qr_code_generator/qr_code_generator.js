// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('QR Code Generator', {
	 refresh(frm) {
		var template = '';
    	if (frm.doc.__islocal) {
      		template = '<img src="" />';
	  	frm.set_df_property('qr_preview', 'options', frappe.render_template(template));
      		frm.refresh_field('qr_preview');
    	} else {
      		if (frm.doc.logo) {
	    	frm.set_df_property('logo', 'read_only', 1);    
	    	frm.refresh_field('logo');
      		} else {
        		frm.set_df_property('logo', 'hidden', 1);    
	    	frm.refresh_field('logo');  
      		}
      		template = '<img src="' + frm.doc.qr_code + '" width="240px"/>';
	  	frm.set_df_property('qr_preview', 'options', frappe.render_template(template));
      		frm.refresh_field('qr_preview');
    }
	// frm.add_custom_button(__('QR Code Page'), function(){
    //     window.location.href = 'http://erpnext_new.com:8003/qr-codes#';
    // }, __("Manage"));
	frm.add_custom_button(__('Go to QR Code Page'), function(){
		// Get the current hostname and port number
		var hostname = window.location.hostname;
		var port = window.location.port;
	
		// Create the URL for the desired webpage
		var url = 'http://' + hostname;
		
		// Check if a port number exists and add it to the URL
		if (port) {
			url += ':' + port;
		}
	
		// Concatenate with the desired page
		url += '/qr-codes#';
	
		// Redirect to the generated URL
		window.location.href = url;
	});
	 },
	 onload(frm) {
		var template = '';
		if (frm.doc.__islocal) {
		  template = '<img src="" />';
		  frm.set_df_property('qr_preview', 'options', frappe.render_template(template));
		  frm.refresh_field('qr_preview');
		} else {
		  if (frm.doc.logo) {
			frm.set_df_property('logo', 'read_only', 1);    
			frm.refresh_field('logo');
		  } else {
			frm.set_df_property('logo', 'hidden', 1);    
			frm.refresh_field('logo');  
		  }
		  template = '<img src="' + frm.doc.qr_code + '" width="240px"/>';
		  frm.set_df_property('qr_preview', 'options', frappe.render_template(template));
		  frm.refresh_field('qr_preview');
		}
	  }
});
