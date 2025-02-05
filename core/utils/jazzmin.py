# jazzmin.py

JAZZMIN_SETTINGS = {
    # Branding
    "site_title": "MoreLiving Admin",
    "site_header": "MoreLiving Management System",
    "site_brand": "MoreLiving Admin",
    "welcome_sign": "Welcome to the MoreLiving Admin Panel",
    "copyright": "© 2025 MoreLiving",
    "search_model": "property.Property",

    # Top menu links
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "property"},
        {"name": "Support", "url": "https://support.moreliving.com", "new_window": True},
    ],

    # Applications to display in the sidebar
    "apps_icons": {
        "auth": "fas fa-users-cog",
        "country": "fas fa-globe",
        "currency": "fas fa-money-bill",
        "faq": "fas fa-question-circle",
        "offers": "fas fa-tags",
        "property": "fas fa-building",
        "reviews": "fas fa-star",
        "rooms": "fas fa-bed",
        "users": "fas fa-user",
    },

    # Customize sidebar menu
    "icons": {
        "auth.Group": "fas fa-users",
        "auth.User": "fas fa-user",
        "country.Country": "fas fa-flag",
        "country.City": "fas fa-city",
        "currency.Currency": "fas fa-coins",
        "faq.MoreLivingFAQ": "fas fa-info-circle",
        "faq.PropertyFAQ": "fas fa-info-circle",
        "offers.WeeklyOffers": "fas fa-tag",
        "property.Property": "fas fa-hotel",
        "property.PropertyCategory": "fas fa-list",
        "property.Amenity": "fas fa-concierge-bell",
        "reviews.GuestReview": "fas fa-comments",
        "reviews.PropertyReview": "fas fa-comment-alt",
        "rooms.BedType": "fas fa-bed",
        "rooms.Prices": "fas fa-dollar-sign",
        "rooms.RoomAmenities": "fas fa-swimmer",
        "rooms.RoomBeds": "fas fa-bed",
        "rooms.RoomImages": "fas fa-image",
        "rooms.RoomTypes": "fas fa-door-open",
        "users.User": "fas fa-user-circle",
    },

    # UI Customizations
    "show_sidebar": True,
    "navigation_expanded": True,
    "custom_css": None,
    "custom_js": None,
    "related_modal_active": True,
    "use_google_fonts_cdn": True,

    # Footer
    "footer_text": "© 2025 MoreLiving. All rights reserved.",

    # Custom icons for apps and models
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}
