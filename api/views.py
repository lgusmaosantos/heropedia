from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from .serializers import HeroSerializer, HeroPictureSerializer
from core.models import Hero

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
