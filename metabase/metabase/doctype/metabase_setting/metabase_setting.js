// Copyright (c) 2018, Tablix and contributors
// For license information, please see license.txt
cur_frm.add_fetch("admin", "email", "email")
cur_frm.add_fetch("admin", "first_name", "first_name")
cur_frm.add_fetch("admin", "last_name", "last_name")

frappe.provide("metabase_setting");
metabase_setting.Metabase = Class.extend({

	init: function(args){
	
		$.extend(this, args);
	},
	refresh: function(){

		var me = this;
		this.frm.add_custom_button(__("Setup Metabase"), function(){

			me.setup_metabase();
		}).addClass("btn-success");	
		this.frm.add_custom_button(__("Sync Metabase"), function(){

			me.install_metabase();
		}).addClass("btn-primary");
	},
	
	install_metabase: function(){

		var me = this;
		frappe.model.with_doctype(this.frm.doctype, function(){

			frappe.call({
				method: "metabase.metabase.sync.start_sync",
				frm: me.frm.doc,
				freeze: true,
				freeze_message: __("Wait while we're installing Metabase for you"),
				callback: function(res){
					console.log(res);
				}	 
			})
		});
	},
	setup_metabase: function(){
	
		var me = this;
		frappe.model.with_doctype(me.frm.doctype, function(){

			frappe.call({

				method: "metabase.metabase.doctype.metabase_setting.metabase_setting.setup_metabase",
				args: {frm: me.frm.doc},
				freeze: true,
				freeze_message: __("Wait while we're initializing setup for you"),
				callback: function(res){
					frappe.msgprint(__("Metabase setup successfully"));
					me.frm.refresh();		
				}
			});	
		});		
	},
	is_same_host: function(){
		var me = this;
		if(me.frm.doc.is_same_host){
			me.frm.doc.host_name = "localhost";
		}
		this.frm.refresh_field("host_name");	
	}
});

cur_frm.script_manager.make(metabase_setting.Metabase);
