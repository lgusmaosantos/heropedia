from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Hero

# Create your views here.


class HeroListView(ListView):
    """A view contendo a relação de heróis já cadastrados.
    Em seu template HTML há links para as funcionalidades
    de edição, remoção e cadastro de novos registros.
    """
    model = Hero
    paginate_by = 10
    template_name = 'hero-listing.html'
