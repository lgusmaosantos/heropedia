from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
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
    ordering = ['name']


class HeroCreateView(SuccessMessageMixin, CreateView):
    """A view onde se dá o registro de um novo herói."""
    model = Hero
    fields = ['name', 'picture', 'description']
    template_name = 'hero-creation-form.html'
    success_message = 'Obrigado por criar o(a) herói/heroína %(name)s. Lembre-se: o maior superpoder é a colaboração.'

    def get_success_url(self) -> str:
        return reverse('hero_listing')
