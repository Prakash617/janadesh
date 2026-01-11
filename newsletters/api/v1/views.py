from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from janadesh.filters import LimitFilter
from django.utils import timezone

from newsletters.models import NewsletterSubscription
from .serializers import NewsletterSubscriptionSerializer
from newsletters.models import NewsletterSubscription
class NewsletterSubscriptionViewSet(viewsets.ModelViewSet):
    """
    API for newsletter subscriptions.
    """
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer
    lookup_field = 'id' # Explicitly set lookup field

    # Anyone can subscribe, only admin can view/manage
    def get_permissions(self):
        if self.action in ['create', 'unsubscribe']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    # Filters
    filter_backends = [DjangoFilterBackend, LimitFilter]
    filterset_fields = ['is_active']

    # -----------------------------
    # Subscribe (POST)
    # -----------------------------
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')

        # Reactivate if already exists
        subscription, created = NewsletterSubscription.objects.get_or_create(
            email=email,
            defaults={'name': request.data.get('name', '')}
        )

        if not created and not subscription.is_active:
            subscription.is_active = True
            subscription.unsubscribed_at = None
            subscription.save()

        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # -----------------------------
    # Unsubscribe
    # -----------------------------
    @action(detail=False, methods=['post'], url_path='unsubscribe')
    def unsubscribe(self, request):
        email = request.data.get('email')

        try:
            subscription = NewsletterSubscription.objects.get(email=email)
            subscription.is_active = False
            subscription.unsubscribed_at = timezone.now()
            subscription.save()
            return Response({'detail': 'Unsubscribed successfully'})
        except NewsletterSubscription.DoesNotExist:
            return Response(
                {'detail': 'Email not found'},
                status=status.HTTP_404_NOT_FOUND
            )
