from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, PublicHabitListView

router = DefaultRouter()
router.register('habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/public-habits/', PublicHabitListView.as_view(), name='public-habits'),
]
