{
    'name': 'GearGuard Maintenance',
    'version': '18.0.1.0.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',

        # ACTIONS FIRST
        'views/actions.xml',

        # SEARCH
        'views/maintenance_request_search.xml',

        # VIEWS
        'views/maintenance_equipment_views.xml',
        'views/maintenance_team_views.xml',
        'views/maintenance_request_views.xml',

        # MENUS LAST
        'views/menu.xml',
    ],
    'application': True,
}
