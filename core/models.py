from django.db import models

# Modelos ORM do projeto Heropedia


class Hero(models.Model):
    """A representação ORM de um herói."""
    name = models.CharField(verbose_name='Nome', max_length=100)
    picture = models.ImageField('Imagem',
                                upload_to='hero_pictures',
                                blank=True,
                                null=True)
    description = models.TextField('Descrição', max_length=240)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Herói'
