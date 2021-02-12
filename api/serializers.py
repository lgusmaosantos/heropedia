from django.db import models
from django.db.models import fields
from rest_framework.decorators import permission_classes
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from core.models import Hero, FavoriteHeroesPerUser

# Serializers do projeto Heropedia


class HeroSerializer(ModelSerializer):
    """Um serializer para o modelo ORM Hero.
    O campo `picture` não será abordado aqui,
    mas em um serializer específico para imagens.
    """
    
    class Meta:
        model = Hero
        fields = ['id', 'name', 'picture', 'description']
        read_only_fields = ['picture']


class HeroPictureSerializer(ModelSerializer):
    """Um serializer para o modelo ORM Hero que aborda
    somente o campo `picture`.
    
    Isso é para que haja uma
    view específica para o upload ou edição da imagem
    de um herói.
    """

    class Meta:
        model = Hero
        fields = ['picture']


class FavoriteHeroesPerUserModelSerializer(ModelSerializer):
    """Um serializer para a tabela com o relacionamento de
    favorito entre `User` e `Hero`.
    """

    class Meta:
        model = FavoriteHeroesPerUser
        fields = ['hero']
        depth = 1
