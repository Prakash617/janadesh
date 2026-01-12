# urls.py
from janadesh.api.router import router

from .views import (
    MenuViewSet,
    MenuItemViewSet,
)


# Menu Management
router.register("menus", MenuViewSet, basename="menu")

# Menu Items
router.register("menu-items", MenuItemViewSet, basename="menu-item")