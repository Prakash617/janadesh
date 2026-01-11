from janadesh.api.router import router
from campaign.api.v1.views import *



router.register("campaigns", CampaignViewSet, basename="campaign")
router.register("campaign-activities", CampaignActivityViewSet, basename="campaign-activity")
router.register("volunteers", VolunteerViewSet, basename="volunteer")


