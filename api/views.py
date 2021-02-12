from rest_framework.viewsets import ModelViewSet
from .serializers import HeroSerializer
from core.models import Hero

# Views e viewsets da API REST


class HeroModelViewSet(ModelViewSet):
    """A viewset com rotas pertinentes à gestão
    do modelo ORM `Hero`.
    """
    serializer_class = HeroSerializer
    queryset = Hero.objects.all()
