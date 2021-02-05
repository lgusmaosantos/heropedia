from django.db import models
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.contrib.auth import get_user
from .models import Hero, FavoriteHeroesPerUser

# Create your views here.


DEFAULT_PERMISSION_DENIED_MESSAGE = 'Você precisa de alguns poderes para isso. Pouca coisa, é só fazer login.'


class HeroListView(ListView):
    """A view contendo a relação de heróis já cadastrados.
    Em seu template HTML há links para as funcionalidades
    de edição, remoção e cadastro de novos registros.
    """
    model = Hero
    paginate_by = 10
    template_name = 'hero-listing.html'
    ordering = ['name']


class HeroCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """A view onde se dá o registro de um novo herói."""
    model = Hero
    fields = ['name', 'picture', 'description']
    template_name = 'hero-creation-form.html'
    success_message = 'Obrigado por criar o(a) herói/heroína %(name)s. Lembre-se: o maior superpoder é a colaboração.'
    permission_denied_message = DEFAULT_PERMISSION_DENIED_MESSAGE
    
    def get_success_url(self) -> str:
        return reverse('hero_listing')

    def get_login_url(self):
        return reverse('login')


class HeroUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """A view que possibilita a autalização/edição de um herói."""
    model = Hero
    template_name = 'hero-update-form.html'
    fields = ['name', 'picture', 'description']
    success_message = '%(name)s atualizado com sucesso.'
    permission_denied_message = DEFAULT_PERMISSION_DENIED_MESSAGE

    def get_success_url(self) -> str:
        return reverse('hero_listing')

    def get_login_url(self):
        return reverse('login')


class HeroDeleteView(LoginRequiredMixin, DeleteView):
    """A view que possibilita a deleção de um herói."""
    model = Hero
    success_message = 'Registro apagado com sucesso. Esperamos que Thanos não tenha nada a ver com isso.'
    permission_denied_message = DEFAULT_PERMISSION_DENIED_MESSAGE

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

    def get_login_url(self):
        return reverse('login')


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


class FavoriteHeroesListView(LoginRequiredMixin, ListView):
    """A view que lista os heróis favoritos de um usuário."""
    model = Hero
    paginate_by = 10
    template_name = 'favorite-heroes-listing.html'
    ordering = ['name']
    permission_denied_message = DEFAULT_PERMISSION_DENIED_MESSAGE

    def get_queryset(self):
        """Filtra a queryset pelo usuário da sessão."""
        user = get_user(self.request)
        pre_queryset = FavoriteHeroesPerUser.objects.filter(user=user)
        queryset = Hero.objects.filter(
            id__in=pre_queryset.values_list('hero', flat=True))
        return queryset

    def get_login_url(self):
        return reverse('login')


class FavoriteHeroRemovalDeleteView(LoginRequiredMixin, DeleteView):
    """A view que remove um herói da lista de favoritos de um
    usuário.
    """
    allowed_methods = ['POST']
    model = FavoriteHeroesPerUser
    ordering = ['name']
    paginate_by = 10
    success_message = 'Removido(a) dos favoritos com sucesso. Também já estávamos enjoados dele(a).'
    permission_denied_message = DEFAULT_PERMISSION_DENIED_MESSAGE

    def get_object(self, queryset=None):
        user = get_user(self.request)
        hero_id = self.request.POST['hero_id']
        return self.model.objects.get(user=user, hero=hero_id)

    def get_success_url(self):
        return reverse('favorite_heroes')

    def delete(self, request, *args, **kwargs):
        """Um override para incluir uma mensagem de sucesso."""
        messages.success(self.request, self.success_message)
        return super(FavoriteHeroRemovalDeleteView, self).delete(
            request, *args, **kwargs)

    def get_login_url(self):
        return reverse('login')


class FavoriteHeroAddView(LoginRequiredMixin, View):
    """A view que cuida da adição de um herói à lista de favoritos
    de um usuário."""
    allowed_methods = ['POST']
    permission_denied_message = DEFAULT_PERMISSION_DENIED_MESSAGE

    def post(self, request, *args, **kwargs):
        user = request.user
        hero_id = request.POST.get('hero_id', None)

        if hero_id:
            try:
                hero = Hero.objects.get(id=hero_id)
            except Hero.DoesNotExist:
                return Http404()
            
            favorite_hero_user = FavoriteHeroesPerUser.objects.get_or_create(
                user=user,
                hero=hero)
            return redirect('favorite_heroes')

    def get_login_url(self):
        return reverse('login')


class CustomLoginView(LoginView):
    """A view que possibilita login na aplicação."""
    template_name = 'login.html'
    
    def get_success_url(self):
        return reverse('hero_listing')


class CustomLogoutView(LogoutView):
    """A view que possibilita logout da aplicação."""
    next_page = '/'
