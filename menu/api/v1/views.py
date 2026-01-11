from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from menu.models import Menu, MenuItem
from .serializers import (
    MenuSerializer,
    MenuListSerializer,
    MenuCreateUpdateSerializer,
    MenuItemSerializer,
    MenuItemListSerializer,
    MenuItemCreateUpdateSerializer,
)


class MenuViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Menu CRUD operations
    
    list: Get all menus
    retrieve: Get a specific menu with all items
    create: Create a new menu (Admin only)
    update: Update a menu (Admin only)
    partial_update: Partially update a menu (Admin only)
    destroy: Delete a menu (Admin only)
    """
    queryset = Menu.objects.all().prefetch_related('items')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'is_active']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'location']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MenuListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MenuCreateUpdateSerializer
        return MenuSerializer
    
    def get_permissions(self):
        """Admin only for write operations"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
    
    @action(detail=False, methods=['get'])
    def by_location(self, request):
        """
        Get menus grouped by location
        GET /api/menus/by_location/
        """
        location = request.query_params.get('location')
        
        if not location:
            return Response(
                {'error': 'Location parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        menus = Menu.objects.filter(location=location, is_active=True)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Toggle menu active status
        POST /api/menus/{id}/toggle_active/
        """
        menu = self.get_object()
        menu.is_active = not menu.is_active
        menu.save()
        
        return Response({
            'message': f"Menu '{menu.name}' is now {'active' if menu.is_active else 'inactive'}",
            'is_active': menu.is_active
        })
    
    @action(detail=True, methods=['get'])
    def items_tree(self, request, pk=None):
        """
        Get menu items in tree structure
        GET /api/menus/{id}/items_tree/
        """
        menu = self.get_object()
        top_level_items = menu.items.filter(parent=None, is_active=True)
        serializer = MenuItemSerializer(top_level_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def locations(self, request):
        """
        Get all available menu locations
        GET /api/menus/locations/
        """
        locations = [
            {'value': choice[0], 'label': choice[1]}
            for choice in Menu.MENU_LOCATION_CHOICES
        ]
        return Response(locations)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get menu statistics
        GET /api/menus/statistics/
        """
        stats = {
            'total_menus': Menu.objects.count(),
            'active_menus': Menu.objects.filter(is_active=True).count(),
            'total_items': MenuItem.objects.count(),
            'active_items': MenuItem.objects.filter(is_active=True).count(),
            'by_location': {}
        }
        
        for location, label in Menu.MENU_LOCATION_CHOICES:
            stats['by_location'][location] = {
                'label': label,
                'count': Menu.objects.filter(location=location).count(),
                'active': Menu.objects.filter(location=location, is_active=True).count()
            }
        
        return Response(stats)


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MenuItem CRUD operations
    
    list: Get all menu items
    retrieve: Get a specific menu item
    create: Create a new menu item (Admin only)
    update: Update a menu item (Admin only)
    partial_update: Partially update a menu item (Admin only)
    destroy: Delete a menu item (Admin only)
    """
    queryset = MenuItem.objects.all().select_related('menu', 'parent')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['menu', 'parent', 'is_active', 'is_external', 'open_new_tab']
    search_fields = ['label_en', 'label_np', 'url']
    ordering_fields = ['order', 'created_at', 'label_en']
    ordering = ['order']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MenuItemListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MenuItemCreateUpdateSerializer
        return MenuItemSerializer
    
    def get_permissions(self):
        """Admin only for write operations"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
    
    @action(detail=False, methods=['get'])
    def by_menu(self, request):
        """
        Get menu items by menu ID
        GET /api/menu-items/by_menu/?menu_id=1
        """
        menu_id = request.query_params.get('menu_id')
        
        if not menu_id:
            return Response(
                {'error': 'menu_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        items = MenuItem.objects.filter(menu_id=menu_id, is_active=True)
        serializer = MenuItemListSerializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top_level(self, request):
        """
        Get only top-level menu items (parent=None)
        GET /api/menu-items/top_level/?menu_id=1
        """
        menu_id = request.query_params.get('menu_id')
        
        queryset = MenuItem.objects.filter(parent=None, is_active=True)
        
        if menu_id:
            queryset = queryset.filter(menu_id=menu_id)
        
        serializer = MenuItemSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        """
        Get children of a specific menu item
        GET /api/menu-items/{id}/children/
        """
        menu_item = self.get_object()
        children = menu_item.children.filter(is_active=True)
        serializer = MenuItemSerializer(children, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Toggle menu item active status
        POST /api/menu-items/{id}/toggle_active/
        """
        item = self.get_object()
        item.is_active = not item.is_active
        item.save()
        
        return Response({
            'message': f"Menu item '{item.label_en}' is now {'active' if item.is_active else 'inactive'}",
            'is_active': item.is_active
        })
    
    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """
        Reorder menu items
        POST /api/menu-items/reorder/
        Body: {"items": [{"id": 1, "order": 0}, {"id": 2, "order": 1}]}
        """
        items_data = request.data.get('items', [])
        
        if not items_data:
            return Response(
                {'error': 'items array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_count = 0
        for item_data in items_data:
            item_id = item_data.get('id')
            order = item_data.get('order')
            
            if item_id is not None and order is not None:
                MenuItem.objects.filter(id=item_id).update(order=order)
                updated_count += 1
        
        return Response({
            'message': f'{updated_count} menu items reordered successfully',
            'updated_count': updated_count
        })
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """
        Duplicate a menu item
        POST /api/menu-items/{id}/duplicate/
        """
        original = self.get_object()
        
        # Create duplicate
        duplicate = MenuItem.objects.create(
            menu=original.menu,
            parent=original.parent,
            label_en=f"{original.label_en} (Copy)",
            label_np=original.label_np,
            url=original.url,
            order=original.order + 1,
            icon=original.icon,
            is_external=original.is_external,
            open_new_tab=original.open_new_tab,
            is_active=False  # Set inactive by default
        )
        
        serializer = MenuItemSerializer(duplicate)
        return Response({
            'message': 'Menu item duplicated successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """
        Delete multiple menu items
        DELETE /api/menu-items/bulk_delete/
        Body: {"ids": [1, 2, 3]}
        """
        ids = request.data.get('ids', [])
        
        if not ids:
            return Response(
                {'error': 'ids array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count, _ = MenuItem.objects.filter(id__in=ids).delete()
        
        return Response({
            'message': f'{deleted_count} menu items deleted successfully',
            'deleted_count': deleted_count
        })
