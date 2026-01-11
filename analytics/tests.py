from django.test import TestCase, Client
from analytics.models import AnalyticsEvent

class AnalyticsAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_blog_api_logging(self):
        response = self.client.get('/api/v1/blogs/')
        self.assertEqual(response.status_code, 200)
        event = AnalyticsEvent.objects.last()
        self.assertEqual(event.event_type, 'page_view')
        self.assertEqual(event.url, '/api/v1/blogs/')

    def test_contact_api_logging(self):
        data = {"name": "John", "email": "john@example.com", "message": "Hello"}
        response = self.client.post('/api/v1/contacts/', data, content_type='application/json')
        self.assertEqual(response.status_code, 201)  # or 200 depending on your view
        event = AnalyticsEvent.objects.last()
        self.assertEqual(event.event_type, 'form_submit')
        self.assertEqual(event.url, '/api/v1/contacts/')
