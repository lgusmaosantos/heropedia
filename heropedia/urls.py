"""heropedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HeroListView.as_view(), name='hero_listing'),
    path('criar-heroi/', views.HeroCreateView.as_view(), name='hero_creation'),
    path('atualizar-heroi/<int:pk>/', views.HeroUpdateView.as_view(), name='hero_update'),
    path('apagar-heroi/<int:pk>/', views.HeroDeleteView.as_view(), name='hero_delete'),
    path('buscar-heroi/', views.SearchListView.as_view(), name='hero_search'),
    path('herois-favoritos/', views.FavoriteHeroesListView.as_view(), name='favorite_heroes'),
    path('remover-favorito/', views.FavoriteHeroRemovalDeleteView.as_view(), name='remove_favorite'),
    path('adicionar-favorito/', views.FavoriteHeroAddView.as_view(), name='add_favorite')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
