DASHUB_SETTINGS = {
    "site_logo": "/static/img/logo_janadesh.webp",
    "site_icon": "/static/favicon.ico",
    "theme_color": "#1E72B7",
    "border_radius": "5px",
    "hide_models": [
        # --------------------------------------------------
        # Django Core
        # --------------------------------------------------
        "auth",
        "auth.user",
        "auth.group",
        # --------------------------------------------------
        # Accounts
        # --------------------------------------------------
        "accounts",
        # "accounts.user",
        # --------------------------------------------------
        # Blogs
        # --------------------------------------------------
        "blogs",
        "blogs.blog",
        "blogs.blogcategory",
        "blogs.blogtag",
        "blogs.comment",
        # --------------------------------------------------
        # Campaign
        # --------------------------------------------------
        "campaign",
        "campaign.campaign",
        "campaign.campaignactivity",
        "campaign.volunteer",
        # --------------------------------------------------
        # Contacts & Communication
        # --------------------------------------------------
        "contacts",
        "contacts.contact",
        "newsletters",
        "newsletters.newslettersubscription",
        # --------------------------------------------------
        # Galleries & Media
        # --------------------------------------------------
        "galleries",
        "galleries.gallery",
        "galleries.galleryimage",
        # --------------------------------------------------
        # Menu Management
        # --------------------------------------------------
        "menu",
        "menu.menu",
        "menu.menuitem",
        # --------------------------------------------------
        # Organization (Public-facing)
        # --------------------------------------------------
        "organization",
        "organization.organization",
        "organization.leadership",
        "organization.membershipregistration",
        "organization.policy",
        "organization.policycategory",
        "organization.donation",
        # --------------------------------------------------
        # Organization (RBAC / Internal)
        # --------------------------------------------------
        "organization_app",
        "organization_app.organization",
        "organization_app.branch",
        "organization_app.role",
        "organization_app.staffrole",
        # --------------------------------------------------
        # Pages & Website
        # --------------------------------------------------
        "page",
        "page.page",
        "website",
        "website.about",
        "website.futurevision",
        "website.socialmedialink",
        "website.socialplatform",
        "website.herosection",
        
        # --------------------------------------------------
        # SEO
        # --------------------------------------------------
        "seo",
        "seo.seometadata",
        # --------------------------------------------------
        # Services
        # --------------------------------------------------
        "services",
        "services.service",
        # --------------------------------------------------
        # Timelines & Manifesto
        # --------------------------------------------------
        "timelines",
        "timelines.timeline",
        "manifesto",
        "manifesto.manifesto",
        # --------------------------------------------------
        # Analytics
        # --------------------------------------------------
        "analytics",
        "analytics.analyticsevent",
    ],
    "custom_links": {

    # =========================
    # AUTH / USER MANAGEMENT
    # =========================
    "auth": [
        {"model": "auth.post", "order": 1},

        {
            "name": "User Management",
            "icon": "fa-solid fa-users",
            "order": 2,
            "submenu": [
                {"model": "auth.user", "order": 1},
                {"model": "auth.group", "order": 2},
            ],
        },
    ],

    # =========================
    # ORGANIZATION SETTINGS
    # =========================
    "Organization Settings": [
        {
            "name": "Organization",
            "icon": "hgi hgi-stroke hgi-command",
            "url": "/admin/organization/organization/",
            "order": 1,
            "submenu": [
                {"model": "organization_app.organization", "order": 1},
                {"model": "organization_app.branch", "order": 2},
                {"model": "organization.membershipregistration", "order": 3},
                {"model": "organization.leadership", "order": 4},
                {"model": "organization.policycategory", "order": 5},
                {"model": "organization.policy", "order": 6},
                # {"model": "organization.donation", "order": 7},
            ],
        },
    ],

    # =========================
    # WEBSITE SETTINGS
    # =========================
    "Website Settings": [

        {
            "name": "Content",
            "icon": "hgi hgi-stroke hgi-carousel-horizontal",
            "url": "/admin/website/content/",
            "order": 1,
            "submenu": [
                {"model": "website.herosection", "order": 1},
                {"model": "website.about", "order": 1},
                {"model": "seo.seometadata", "order": 2},
                {"model": "manifesto.manifesto", "order": 3},
                {"model": "website.futurevision", "order": 4},
                {"model": "website.curateditem", "order": 5},
                {"model": "website.socialplatform", "order": 6},
                {"model": "website.socialmedialink", "order": 6},
                {"model": "timelines.timeline", "order": 7},
                {"model": "services.service", "order": 8},
                {"model": "galleries.gallery", "order": 9},
            ],
        },

        {
            "name": "Blog",
            "icon": "hgi hgi-stroke hgi-license",
            "url": "/admin/website/blog/",
            "order": 2,
            "submenu": [
                {"model": "blogs.blog", "order": 1},
                {"model": "blogs.blogcategory", "order": 2},
                {"model": "blogs.blogtag", "order": 3},
            ],
        },

        {
            "name": "Communication",
            "icon": "hgi hgi-stroke hgi-service",
            "url": "/admin/website/communication/",
            "order": 3,
            "submenu": [
                {"model": "newsletters.newslettersubscription", "order": 1},
                {"model": "contacts.contact", "order": 2},
            ],
        },
    ],

    # =========================
    # ADVANCED TOOLS
    # =========================
    "advance": [
        {
            "name": "File Manager",
            "url": "/filemanager/",
            "icon": "hgi hgi-stroke hgi-folder-cloud",
            "order": 1,
        },
    ],
},
    "submenus_models": ["auth.group"],
    "default_orders": {
        "auth": 10,
        "auth.group": 4,
    },
    "icons": {
        "accounts.user": "hgi hgi-stroke hgi-user-sharing",
        "auth.group": "hgi hgi-stroke hgi-user-group-03",
        "analytics.analyticsevent": "hgi hgi-stroke hgi-chart-bar",
        "blogs.blogcategory": "hgi hgi-stroke hgi-calendar-02",
        "blogs.blogtag": "hgi hgi-stroke hgi-tag-01",
        "blogs.blog": "hgi hgi-stroke hgi-license",
        "blogs.comment": "hgi hgi-stroke hgi-comment-01",
        "campaign.campaign": "hgi hgi-stroke hgi-megaphone-01",
        "campaign.campaignactivity": "hgi hgi-stroke hgi-activity-01",
        "campaign.volunteer": "hgi hgi-stroke hgi-add-male",
        "contacts.contact": "hgi hgi-stroke hgi-contact-01",
        "galleries.gallery": "hgi hgi-stroke hgi-image-01",
        "galleries.galleryimage": "hgi hgi-stroke hgi-image-plus",
        "menu.menu": "hgi hgi-stroke hgi-menu-01",
        "menu.menuitem": "hgi hgi-stroke hgi-list",
        "organization.organization": "hgi hgi-stroke hgi-drawing-compass",
        "organization.leadership": "hgi hgi-stroke hgi-user-group",
        "organization.membershipregistration": "hgi hgi-stroke hgi-user-add-01",
        "organization.policy": "hgi hgi-stroke hgi-policy",
        "organization.policycategory": "hgi hgi-stroke hgi-ai-sheets",
        "organization.donation": "hgi hgi-stroke hgi-wallet-01",
        "seo.seometadata": "hgi hgi-stroke hgi-globe",
        "services.service": "hgi hgi-stroke hgi-service",
        "timelines.timeline": "hgi hgi-stroke hgi-timeline",
        "newsletters.newslettersubscription": "hgi hgi-stroke hgi-news-01",
        "manifesto.manifesto": "hgi hgi-stroke hgi-medical-file",
        "page.page": "hgi hgi-stroke hgi-file-01",
        "website.about": "hgi hgi-stroke hgi-atom-01",
        "website.futurevision": "hgi hgi-stroke hgi-vision",
        "website.socialmedialink": "hgi hgi-stroke hgi-soil-moisture-field",
        "organization_app.branch": "hgi hgi-stroke hgi-git-merge",
        "organization_app.organization": "hgi hgi-stroke hgi-command",
        "organization_app.role": "hgi hgi-stroke hgi-film-roll-01",
        "organization_app.staffrole": "hgi hgi-stroke hgi-account-setting-03",
        "analytics.analyticsevent": "hgi hgi-stroke hgi-math",
    },
    "custom_js": [
        "/static/js/admin.js",
    ],
    "custom_css": [
        "/static/css/admin.css",
    ],
}
