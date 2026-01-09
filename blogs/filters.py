import django_filters
from .models import Blog

class BlogFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    tags = django_filters.CharFilter(field_name='tags__slug', lookup_expr='iexact')
    author = django_filters.NumberFilter(field_name='author__id')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    is_featured = django_filters.BooleanFilter(field_name='is_featured') 
    published_after = django_filters.DateFilter(field_name='published_at', lookup_expr='gte')
    published_before = django_filters.DateFilter(field_name='published_at', lookup_expr='lte')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Blog
        fields = ['category', 'tags', 'author','is_featured', 'status', 'published_after', 'published_before']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title_en__icontains=value) |
            Q(title_np__icontains=value) |
            Q(content_en__icontains=value) |
            Q(content_np__icontains=value)
        )
