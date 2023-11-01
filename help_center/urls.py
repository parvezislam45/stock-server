from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, HelpCenterViewSet, live_chat

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'contact-messages', ContactMessageViewSet)
router.register(r'help-center', HelpCenterViewSet, basename='help-center')

urlpatterns = [
    # path('send/', HelpCenterViewSet.as_view),
    path('api/', include(router.urls)),  # Include the API URLs
    path('live-chat/', live_chat, name='live_chat'),
]