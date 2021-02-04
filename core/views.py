from django.db import models
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.contrib.auth import get_user
from .models import Hero, FavoriteHeroesPerUser

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


class HeroUpdateView(SuccessMessageMixin, UpdateView):
    """A view que possibilita a autalização/edição de um herói."""
    model = Hero
    template_name = 'hero-update-form.html'
    fields = ['name', 'picture', 'description']
    success_message = '%(name)s atualizado com sucesso.'

    def get_success_url(self) -> str:
        return reverse('hero_listing')


class HeroDeleteView(DeleteView):
    """A view que possibilita a deleção de um herói."""
    model = Hero
    success_message = 'Registro apagado com sucesso. Esperamos que Thanos não tenha nada a ver com isso.'

    def get_success_url(self) -> str:
        return reverse('hero_listing')

    def delete(self, request, *args, **kwargs):
        """Um override do método `delete` da view para
        a inclusão da mensagem de confirmação da exclusão.
        É necessário pois uma `message` está normalmente
        atrelada a um `form_valid`, que não existe em
        `DeleteView`.

        Mais detalhes na issue do projeto Django, em:
        https://code.djangoproject.com/ticket/21936
        """
        messages.success(self.request, self.success_message)
        return super(HeroDeleteView, self).delete(request, *args, **kwargs)


class SearchListView(ListView):
    """A view que processa a busca de heróis por nome."""
    model = Hero
    paginate_by = 10
    template_name = 'hero-listing.html'
    ordering = ['name']

    def get_queryset(self):
        """Sobrescreve `get_queryset` para filtragem pelo termo
        de busca.
        """
        search_term = self.request.GET['search_term']
        queryset = self.model.objects.filter(
            name__icontains=search_term)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['origin_view'] = 'search'
        context['search_term'] = self.request.GET['search_term']
        return context


class FavoriteHeroesListView(ListView):
    """A view que lista os heróis favoritos de um usuário."""
    model = Hero
    paginate_by = 10
    template_name = 'favorite-heroes-listing.html'
    ordering = ['name']

    def get_queryset(self):
        """Filtra a queryset pelo usuário da sessão."""
        user = get_user(self.request)
        pre_queryset = FavoriteHeroesPerUser.objects.filter(user=user)
        queryset = Hero.objects.filter(
            id__in=pre_queryset.values_list('hero', flat=True))
        return queryset
