from janadesh.api.router import router
from .views import (
    # OrganizationViewSet,
    LeadershipViewSet,
    MembershipRegistrationViewSet,
    PolicyViewSet,
    DonationViewSet,
)


# Register all routes with the shared router
# router.register("organizations", OrganizationViewSet, basename="organization")
router.register("leadership", LeadershipViewSet, basename="leadership")
router.register("membership-registrations", MembershipRegistrationViewSet, basename="membership-registration")
router.register("policies", PolicyViewSet, basename="policy")
router.register("donations", DonationViewSet, basename="donation")


