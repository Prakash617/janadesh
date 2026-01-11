# views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from analytics.models import AnalyticsEvent
from .serializers import (
    AnalyticsEventSerializer,
    AnalyticsEventCreateSerializer,
    AnalyticsEventListSerializer,
)


class AnalyticsEventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AnalyticsEvent
    
    list: Get all analytics events (Admin only)
    retrieve: Get a specific event (Admin only)
    create: Track a new analytics event (Public)
    """
    queryset = AnalyticsEvent.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event_type', 'object_type', 'language', 'country', 'city']
    search_fields = ['url', 'ip_address', 'country', 'city']
    ordering_fields = ['created_at', 'event_type']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AnalyticsEventListSerializer
        elif self.action == 'create':
            return AnalyticsEventCreateSerializer
        return AnalyticsEventSerializer
    
    def get_permissions(self):
        """Public can create (track), admin can view"""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def create(self, request, *args, **kwargs):
        """Track analytics event"""
        # Auto-capture IP and user agent if not provided
        data = request.data.copy()
        
        if not data.get('ip_address'):
            data['ip_address'] = self.get_client_ip(request)
        
        if not data.get('user_agent'):
            data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'message': 'Event tracked successfully',
            'event_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """
        Get analytics statistics
        GET /api/analytics/statistics/
        Query params: days (default: 30)
        """
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        events = AnalyticsEvent.objects.filter(created_at__gte=start_date)
        
        stats = {
            'total_events': events.count(),
            'total_page_views': events.filter(event_type='page_view').count(),
            'total_blog_views': events.filter(event_type='blog_view').count(),
            'total_campaign_views': events.filter(event_type='campaign_view').count(),
            'total_downloads': events.filter(event_type='download').count(),
            'total_form_submits': events.filter(event_type='form_submit').count(),
            'unique_sessions': events.values('session_id').distinct().count(),
            'unique_ips': events.values('ip_address').distinct().count(),
            'date_range': {
                'start': start_date.date().isoformat(),
                'end': timezone.now().date().isoformat(),
                'days': days
            }
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def top_pages(self, request):
        """
        Get top pages by views
        GET /api/analytics/top_pages/
        Query params: limit (default: 10), days (default: 30)
        """
        limit = int(request.query_params.get('limit', 10))
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        top_pages = (
            AnalyticsEvent.objects
            .filter(event_type='page_view', created_at__gte=start_date)
            .values('url')
            .annotate(views=Count('id'))
            .order_by('-views')[:limit]
        )
        
        return Response(list(top_pages))
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def top_countries(self, request):
        """
        Get top countries by events
        GET /api/analytics/top_countries/
        Query params: limit (default: 10), days (default: 30)
        """
        limit = int(request.query_params.get('limit', 10))
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        top_countries = (
            AnalyticsEvent.objects
            .filter(created_at__gte=start_date)
            .exclude(country__isnull=True)
            .exclude(country='')
            .values('country')
            .annotate(count=Count('id'))
            .order_by('-count')[:limit]
        )
        
        return Response(list(top_countries))
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def events_by_type(self, request):
        """
        Get events grouped by type
        GET /api/analytics/events_by_type/
        Query params: days (default: 30)
        """
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        events_by_type = (
            AnalyticsEvent.objects
            .filter(created_at__gte=start_date)
            .values('event_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        return Response(list(events_by_type))
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def events_timeline(self, request):
        """
        Get events timeline (by date)
        GET /api/analytics/events_timeline/
        Query params: days (default: 30), group_by (day/hour, default: day)
        """
        days = int(request.query_params.get('days', 30))
        group_by = request.query_params.get('group_by', 'day')
        start_date = timezone.now() - timedelta(days=days)
        
        events = AnalyticsEvent.objects.filter(created_at__gte=start_date)
        
        if group_by == 'hour':
            timeline = (
                events
                .extra(select={'date': "date_trunc('hour', created_at)"})
                .values('date')
                .annotate(count=Count('id'))
                .order_by('date')
            )
        else:  # day
            timeline = (
                events
                .extra(select={'date': "date_trunc('day', created_at)"})
                .values('date')
                .annotate(count=Count('id'))
                .order_by('date')
            )
        
        return Response(list(timeline))
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def events_by_language(self, request):
        """
        Get events grouped by language
        GET /api/analytics/events_by_language/
        Query params: days (default: 30)
        """
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        events_by_language = (
            AnalyticsEvent.objects
            .filter(created_at__gte=start_date)
            .values('language')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        return Response(list(events_by_language))
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def object_stats(self, request):
        """
        Get statistics for specific object type
        GET /api/analytics/object_stats/?object_type=blog
        Query params: object_type (required), days (default: 30)
        """
        object_type = request.query_params.get('object_type')
        
        if not object_type:
            return Response(
                {'error': 'object_type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        object_stats = (
            AnalyticsEvent.objects
            .filter(object_type=object_type, created_at__gte=start_date)
            .values('object_id')
            .annotate(
                total_views=Count('id'),
                unique_sessions=Count('session_id', distinct=True),
                unique_ips=Count('ip_address', distinct=True)
            )
            .order_by('-total_views')
        )
        
        return Response(list(object_stats))
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def referrer_stats(self, request):
        """
        Get top referrers
        GET /api/analytics/referrer_stats/
        Query params: limit (default: 10), days (default: 30)
        """
        limit = int(request.query_params.get('limit', 10))
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        referrer_stats = (
            AnalyticsEvent.objects
            .filter(created_at__gte=start_date)
            .exclude(referrer__isnull=True)
            .exclude(referrer='')
            .values('referrer')
            .annotate(count=Count('id'))
            .order_by('-count')[:limit]
        )
        
        return Response(list(referrer_stats))
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def track_page_view(self, request):
        """
        Convenient endpoint for tracking page views
        POST /api/analytics/track_page_view/
        Body: {url, referrer?, session_id?, language?}
        """
        data = {
            'event_type': 'page_view',
            'url': request.data.get('url'),
            'referrer': request.data.get('referrer'),
            'session_id': request.data.get('session_id'),
            'language': request.data.get('language', 'en'),
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
        
        serializer = AnalyticsEventCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Page view tracked successfully'
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def track_blog_view(self, request):
        """
        Track blog post view
        POST /api/analytics/track_blog_view/
        Body: {blog_id, url, session_id?, language?}
        """
        data = {
            'event_type': 'blog_view',
            'object_type': 'blog',
            'object_id': request.data.get('blog_id'),
            'url': request.data.get('url'),
            'referrer': request.data.get('referrer'),
            'session_id': request.data.get('session_id'),
            'language': request.data.get('language', 'en'),
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
        
        serializer = AnalyticsEventCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Blog view tracked successfully'
        }, status=status.HTTP_201_CREATED)

