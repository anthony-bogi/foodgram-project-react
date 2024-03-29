import csv
import os

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    """Импортирует данные об ингредиентах из *.csv-файла."""

    def handle(self, *args, **options):
        file_name = 'ingredients.csv'
        file_path = os.path.join(
            os.path.dirname(__file__),
            *([os.pardir] * 1), 'data',
            file_name
        )
        if Ingredient.objects.exists():
            self.stderr.write('Данные об ингредиентах уже загружены.')
            return

        self.stdout.write(
            f'Загружаем данные об ингредиентах из {file_name}...'
        )
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                _, _ = Ingredient.objects.update_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
        self.stdout.write('Загрузка завершена!')
