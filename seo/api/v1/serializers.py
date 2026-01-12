# serializers.py
from rest_framework import serializers
from menu.models import Menu, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    """Serializer for MenuItem with children support"""
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'menu',
            'parent',
            'label_en',
            'label_np',
            'title',
            'sub_title',
            'url',
            'order',
            'icon',
            'is_external',
            'open_new_tab',
            'is_active',
            'created_at',
            'children',
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_children(self, obj):
        """Get child menu items recursively"""
        if obj.children.exists():
            return MenuItemSerializer(
                obj.children.filter(is_active=True),
                many=True,
                context=self.context
            ).data
        return []


class MenuItemCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating menu items"""
    
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'menu',
            'parent',
            'label_en',
            'label_np',
            'title',
            'sub_title',
            'url',
            'order',
            'icon',
            'is_external',
            'open_new_tab',
            'is_active',
        ]
        read_only_fields = ['id']
    
    def validate_parent(self, value):
        """Ensure parent belongs to the same menu"""
        if value and self.instance:
            if value.menu != self.instance.menu:
                raise serializers.ValidationError(
                    "Parent menu item must belong to the same menu."
                )
        return value
    
    def validate(self, attrs):
        """Additional validation"""
        # Prevent circular references
        if attrs.get('parent') and self.instance:
            parent = attrs['parent']
            current = parent
            while current:
                if current == self.instance:
                    raise serializers.ValidationError({
                        "parent": "Cannot create circular reference in menu hierarchy."
                    })
                current = current.parent
        
        return attrs


class MenuItemListSerializer(serializers.ModelSerializer):
    """Simple serializer for listing menu items without children"""
    parent_label = serializers.CharField(source='parent.label_en', read_only=True)
    menu_name = serializers.CharField(source='menu.name', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'menu',
            'menu_name',
            'parent',
            'parent_label',
            'label_en',
            'label_np',
            'title',
            'sub_title',
            'url',
            'order',
            'icon',
            'is_external',
            'open_new_tab',
            'is_active',
            'created_at',
        ]


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for Menu with nested items"""
    items = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = [
            'id',
            'name',
            'location',
            'is_active',
            'created_at',
            'updated_at',
            'items',
            'items_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_items(self, obj):
        """Get only top-level menu items (parent=None) with their children"""
        top_level_items = obj.items.filter(parent=None, is_active=True)
        return MenuItemSerializer(top_level_items, many=True, context=self.context).data
    
    def get_items_count(self, obj):
        """Get total count of menu items"""
        return obj.items.count()


class MenuListSerializer(serializers.ModelSerializer):
    """Simple serializer for listing menus"""
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = [
            'id',
            'name',
            'location',
            'is_active',
            'items_count',
            'created_at',
            'updated_at',
        ]
    
    def get_items_count(self, obj):
        return obj.items.count()


class MenuCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating menus"""
    
    class Meta:
        model = Menu
        fields = [
            'id',
            'name',
            'location',
            'is_active',
        ]
        read_only_fields = ['id']
    
    def validate_name(self, value):
        """Ensure unique menu name per location"""
        location = self.initial_data.get('location') or (
            self.instance.location if self.instance else None
        )
        
        queryset = Menu.objects.filter(name=value, location=location)
        
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError(
                f"A menu with this name already exists in the '{location}' location."
            )
        
        return value
