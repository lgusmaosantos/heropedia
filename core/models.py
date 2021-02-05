from django.db import models
from django.contrib.auth import get_user_model

# Modelos ORM do projeto Heropedia

# Obtém a classe de usuário em uso pelo projeto
User = get_user_model()

class Hero(models.Model):
    """A representação ORM de um herói."""
    name = models.CharField(verbose_name='Nome',
                            max_length=100,
                            unique=True)
    picture = models.ImageField('Imagem',
                                upload_to='hero_pictures',
                                blank=True,
                                null=True)
    description = models.TextField('Descrição', max_length=240)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Herói'


class FavoriteHeroesPerUser(models.Model):
    """A classe modelo que representa a relação de usuário
    e heróis favoritos.
    """
    hero = models.ForeignKey(Hero, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} likes {self.hero}'

    class Meta:
        verbose_name = 'Herói favorito por usuário'
        verbose_name_plural = 'Heróis favoritos por usuário'
        constraints = [models.UniqueConstraint(
            fields=['hero', 'user'], name='hero_object_unique_for_user'
        )]
