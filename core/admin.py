from django.contrib import admin
from .models import Hero

# Register your models here.


@admin.register(Hero)
class HeroModelAdmin(admin.ModelAdmin):
    pass
