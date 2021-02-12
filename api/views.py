from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import DestroyModelMixin, ListModelMixin
from rest_framework.generics import UpdateAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from core.models import *

# Views e viewsets da API REST


class HeroModelViewSet(ModelViewSet):
    """A viewset com rotas pertinentes à gestão
    do modelo ORM `Hero`.
    """
    serializer_class = HeroSerializer
    queryset = Hero.objects.all()
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']


class HeroPictureUpdateAPIView(UpdateAPIView):
    """Uma view para alterar (ou inserir, quando não houver)
    a imagem (campo `picture`) de um objeto do modelo `Hero`.

    Esta view cuida apenas do campo `picture` devido à natureza
    de arquivo daquele campo, onde aparenta ser mais conveniente
    que ele tenha uma view própria.
    """
    parser_classes = [MultiPartParser, FormParser]
    allowed_methods = ['PATCH']
    queryset = Hero.objects.all()
    serializer_class = HeroPictureSerializer


class FavoriteHeroesViewSet(ListModelMixin,
                            DestroyModelMixin,
                            GenericViewSet):
    """A viewset com as rotas pertinentes ao relacionamento
    de favorito entre `User` e `Hero`.
    """
    serializer_class = FavoriteHeroesPerUserModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'hero'
    filter_backends = [OrderingFilter]
    ordering_fields = ['hero__id']
    ordering = ['hero__name']

    def get_queryset(self):
        """Seleciona para exibição apenas os resultados que
        pertencem ao usuário da requisição.
        """
        queryset = FavoriteHeroesPerUser.objects.filter(
            user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        hero_id = request.data.get('hero', None)

        if hero_id and type(hero_id) == int and hero_id > 0:
            try:
                hero = Hero.objects.get(id=hero_id)
            except Hero.DoesNotExist:
                return Response(status=HTTP_404_NOT_FOUND,
                                data={
                                    'detail': "Não encontrado"
                                })

            fav_hero = FavoriteHeroesPerUser.objects.get_or_create(
                user=request.user,
                hero=hero
            )
            serializer = self.get_serializer(fav_hero[0])
            return Response(status=HTTP_201_CREATED,
                            data=serializer.data)
        else:
            return Response(status=HTTP_400_BAD_REQUEST, data={
                "detail": "O campo \"hero\" precisa ser informado com um número inteiro positivo."
            })
