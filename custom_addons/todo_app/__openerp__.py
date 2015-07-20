{
    "name" : "To-Do Application",
    "description" : "Manage your personal tasks with this module.",
    "author" : "Johan Vergeer",
    "depends" : ["mail"],
    "application" : True,
    "summary" : "You can manage your tasks with this module.",
    "version" : "1.0",
    "licence" : "AGPL-3",
    "website" : "https://github.com/johanvergeer/Odoo-dev",
    "category" : "I have to look for this"
                 "category is the functional category of the module, which defaults to"
                 "Uncategoryzed. This list of existing categories can be found in the security"
                 "Groups form (settings | user | groups menu), in the Application field"
                 "drop-down list.",
    "installable" : True,
    "auto_install" : True,
    "data" : ["views/todo_view.xml",
             "security/ir.model.access.csv",
              "security/todo_access_rules.xml"]

}