
frappe.pages['metabase'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Metabase Dashboard',
		single_column: true
	});

	console.log(frappe.provide);
	metabase = new metabase.metabase.MetabasePage({page:page});
}
