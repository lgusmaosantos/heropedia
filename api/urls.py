from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HeroModelViewSet, HeroPictureUpdateAPIView

# Rotas API REST

hero_router = DefaultRouter()
hero_router.register('hero', HeroModelViewSet)

urlpatterns = [
    path('', include(hero_router.urls)),
    path('hero-picture/<int:pk>/', HeroPictureUpdateAPIView.as_view(), name='hero_picture_update')
]