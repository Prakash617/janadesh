from rest_framework import serializers
from galleries.models import Gallery, GalleryImage

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'caption_en', 'caption_np', 'order', 'created_at']

class GallerySerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, read_only=True)  # nested images

    class Meta:
        model = Gallery
        fields = [
            'id', 'title_en', 'title_np', 'slug', 'description_en', 'description_np',
            'cover_image', 'is_featured', 'order', 'created_at', 'updated_at', 'images'
        ]
