# Generated by Django 3.1.6 on 2021-02-04 06:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_remove_hero_favorited_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteHeroesPerUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.hero')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
