app_name = "ai_business_analytics"
app_title = "AI Business Analytics"
app_publisher = "AI Analytics Manufacturing Pvt Ltd"
app_description = "AI-powered business analytics and natural language data querying for Frappe"
app_email = "aianalytics2021@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "ai_business_analytics",
# 		"logo": "/assets/ai_business_analytics/logo.png",
# 		"title": "AI Business Analytics",
# 		"route": "/ai_business_analytics",
# 		"has_permission": "ai_business_analytics.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ai_business_analytics/css/ai_business_analytics.css"
# app_include_js = "/assets/ai_business_analytics/js/ai_business_analytics.js"

# include js, css files in header of web template
# web_include_css = "/assets/ai_business_analytics/css/ai_business_analytics.css"
# web_include_js = "/assets/ai_business_analytics/js/ai_business_analytics.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ai_business_analytics/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ai_business_analytics/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ai_business_analytics.utils.jinja_methods",
# 	"filters": "ai_business_analytics.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ai_business_analytics.install.before_install"
# after_install = "ai_business_analytics.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ai_business_analytics.uninstall.before_uninstall"
# after_uninstall = "ai_business_analytics.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ai_business_analytics.utils.before_app_install"
# after_app_install = "ai_business_analytics.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ai_business_analytics.utils.before_app_uninstall"
# after_app_uninstall = "ai_business_analytics.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "ai_business_analytics.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ai_business_analytics.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["ai_business_analytics.search.awesomebar_results"]

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
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ai_business_analytics.tasks.all"
# 	],
# 	"daily": [
# 		"ai_business_analytics.tasks.daily"
# 	],
# 	"hourly": [
# 		"ai_business_analytics.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ai_business_analytics.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ai_business_analytics.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ai_business_analytics.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "ai_business_analytics.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ai_business_analytics.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ai_business_analytics.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ai_business_analytics.utils.before_request"]
# after_request = ["ai_business_analytics.utils.after_request"]

# Job Events
# ----------
# before_job = ["ai_business_analytics.utils.before_job"]
# after_job = ["ai_business_analytics.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ai_business_analytics.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

