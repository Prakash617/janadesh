from rest_framework import viewsets,status
from organization.models import  Leadership, MembershipRegistration, Policy, Donation
from .serializers import (
    # OrganizationSerializer,
    LeadershipSerializer,
    MembershipRegistrationSerializer,
    PolicySerializer,
    DonationSerializer,
)

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone



# ------------------------
# Organization ViewSet
# ------------------------
# class OrganizationViewSet(viewsets.ModelViewSet):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer
#     lookup_field = 'slug'  # use slug in URLs instead of ID

# ------------------------
# Leadership ViewSet
# ------------------------
class LeadershipViewSet(viewsets.ModelViewSet):
    queryset = Leadership.objects.all()
    serializer_class = LeadershipSerializer
    lookup_field = 'slug'

# ------------------------
# MembershipRegistration ViewSet
# ------------------------
class MembershipRegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Membership Registration
    """
    queryset = MembershipRegistration.objects.all()
    serializer_class = MembershipRegistrationSerializer
    permission_classes = [AllowAny]

    filterset_fields = ['status', 'province']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """Create membership registration"""
        serializer.save(status='pending')

    # ✅ APPROVE ACTION
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        membership = self.get_object()

        if membership.status != 'pending':
            return Response(
                {'detail': 'Only pending applications can be approved.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        membership.status = 'approved'
        membership.approved_by = request.user
        membership.approved_at = timezone.now()
        membership.save()

        return Response(
            {'detail': 'Membership approved successfully.'},
            status=status.HTTP_200_OK
        )

    # ❌ REJECT ACTION
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        membership = self.get_object()
        reason = request.data.get('reason')

        if membership.status != 'pending':
            return Response(
                {'detail': 'Only pending applications can be rejected.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        membership.status = 'rejected'
        membership.rejection_reason = reason
        membership.save()
        return Response(
            {'detail': 'Membership rejected successfully.'},
            status=status.HTTP_200_OK
        )

# ------------------------
# Policy ViewSet
# ------------------------
class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    lookup_field = 'slug'

# ------------------------
# Donation ViewSet
# ------------------------
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
