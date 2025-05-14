ROLE_PERMISSIONS = {
    'superadmin': [
        'add_property', 'change_property', 'delete_property', 'view_property',
        'can_approve_property', 'can_feature_property', 'can_sell_property',
    ],
    'agent': [
        'add_property', 'change_property', 'view_property', 'can_approve_property'
    ],
    'seller': [
        'add_property', 'change_property', 'view_property'
    ],
    'buyer': [
        'view_property'
    ],
    'tenant': [
        'view_property'
    ],
    'landlord': [
        'add_property', 'change_property', 'view_property'
    ],
    'manager': [
        'change_property', 'view_property', 'can_feature_property'
    ]
}
