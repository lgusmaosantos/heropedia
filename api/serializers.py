from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from core.models import Hero

# Serializers do projeto Heropedia


class HeroSerializer(ModelSerializer):
    """Um serializer para o modelo ORM Hero.
    O campo `picture` não será abordado aqui,
    mas em um serializer específico para imagens.
    """
    
    class Meta:
        model = Hero
        fields = ['id', 'name', 'description']
