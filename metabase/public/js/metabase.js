/*
	License Tablix
	Developer Navdeep Singh
	Email navdeepghai1@gmail.com
*/

frappe.provide("metabase.metabase");

metabase.metabase.MetabasePage = Class.extend({

	init: function(args){
		$.extend(this, args);
		this.make();
	},
	
	make: function(){
		this.remove_title();
		this.make_page();
		this.show_my_password();
		this.open_in_new_tab();

	},
	remove_title: function(){
		$(".page-title").empty();	
	},
	make_page: function(){
		var me = this;
		
		$(frappe.render_template("metabase_page", {"src":"http://188.226.136.185:5050"})).appendTo(".page-content");
		//ele.href = "http://188.226.136.185:5050";
		//$(ele).appendTo("#metabase");	
	},
	show_my_password: function(){
		var me = this;
		$(".show-my-password").on("click", function(event){
			
			event.preventDefault();
			if (frappe.boot.metabase.user_info){
				var info = frappe.boot.metabase.user_info;
				var html = frappe.render_template("metabase_login_form", {"email": info.email, password: info.info})
				frappe.msgprint(html);		
			}	
			else{
				frappe.msgprint(__("You're not authorized to view this page"));
			}
			
				
		});
	},
	open_in_new_tab: function(){
		
		var me = this;
		$(".open-in-new-window").on("click", function(event){

			event.preventDefault();
			var tab = window.open(frappe.boot.metabase.setting.url, "_target");
		
		});	
	}
		
})


