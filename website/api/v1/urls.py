from janadesh.api.router import router
from .views import AboutMovementViewSet,FutureVisionViewSet,SocialMediaLinkViewSet



router.register(r"about-movement", AboutMovementViewSet, basename="about-movement")
router.register(r"future-vision", FutureVisionViewSet, basename="future-vision")
router.register(r"social-links", SocialMediaLinkViewSet, basename="social-links")


