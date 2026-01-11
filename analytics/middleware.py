from django.utils.deprecation import MiddlewareMixin
from .models import AnalyticsEvent


class AnalyticsMiddleware(MiddlewareMixin):
    """
    Middleware to track API requests for analytics (version-agnostic).
    """

    def process_request(self, request):
        try:
            # Skip admin, static, media
            if request.path.startswith(('/admin/', '/static/', '/media/')):
                return

            # Only track API endpoints
            if not request.path.startswith('/api/'):
                return

            # Determine event type
            event_type = self.get_event_type(request.path, request.method)
            object_type, object_id = self.get_object_info(request.path)

            # Create AnalyticsEvent
            AnalyticsEvent.objects.create(
                event_type=event_type,
                object_type=object_type,
                object_id=object_id,
                url=request.path,
                referrer=request.META.get('HTTP_REFERER', ''),
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                session_id=self.get_or_create_session(request),
                language=getattr(request, 'LANGUAGE_CODE', 'en'),
            )

        except Exception as e:
            # Fail silently
            print("AnalyticsMiddleware error:", e)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def get_or_create_session(self, request):
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key

    def get_event_type(self, path, method):
        """
        Determines event type based on API path and method.
        Version-agnostic.
        """
        # Extract resource name from path: /api/v1/blogs/slug/ -> blogs
        parts = path.strip('/').split('/')
        resource = parts[2] if len(parts) >= 3 else (parts[1] if len(parts) >= 2 else '')

        if resource == 'blogs':
            return 'blog_view'
        elif resource == 'campaigns':
            return 'campaign_view'
        elif resource == 'download':
            return 'download'
        elif method == 'POST':
            return 'form_submit'
        else:
            return 'api_request'

    def get_object_info(self, path):
        """
        Extract object_type and object_id/slug from path.
        Version-agnostic.
        Example: /api/v1/blogs/my-blog-slug/ -> object_type='blog', object_id='my-blog-slug'
        """
        parts = path.strip('/').split('/')
        if len(parts) >= 3:
            resource = parts[2]
            obj_id = parts[3] if len(parts) >= 4 else None
            return resource[:-1] if resource.endswith('s') else resource, obj_id
        return None, None
