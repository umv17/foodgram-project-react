import json

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('recipes/data/tags.json', 'rb') as f:
            data = json.load(f)
            for i in data:
                tags = Tag()
                tags.name = i['name']
                tags.color = i['color']
                tags.slug = i['slug']
                tags.save()
