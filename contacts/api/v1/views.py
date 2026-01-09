from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from contacts.models import Contact
from .serializers import ContactSerializer
from janadesh.filters import LimitFilter  # your custom limit filter
from rest_framework.pagination import PageNumberPagination


# -----------------------------
# Custom Pagination (optional)
# -----------------------------
class ContactPagination(PageNumberPagination):
    page_size = 10  # default page size
    page_size_query_param = 'page_size'  # ?page_size=5
    max_page_size = 50

# -----------------------------
# Contact API ViewSet
# -----------------------------
class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing contact form submissions.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    # Only admin users can see full details
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]  # anyone can create (POST)

    # Filters & ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        LimitFilter
    ]
    filterset_fields = ['status']  # ?status=pending
    search_fields = ['name', 'email', 'subject', 'message']  # ?search=John
    ordering_fields = ['created_at', 'updated_at']  # ?ordering=-created_at
    ordering = ['-created_at']  # default

    # Pagination
    pagination_class = ContactPagination

    # Automatically capture IP & User-Agent
    def perform_create(self, serializer):
        request = self.request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        user_agent = request.META.get('HTTP_USER_AGENT')
        serializer.save(ip_address=ip_address, user_agent=user_agent)