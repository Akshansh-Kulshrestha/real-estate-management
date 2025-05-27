import csv
from django.core.management.base import BaseCommand
from core.models import Amenity

class Command(BaseCommand):
    help = 'Import amenities from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='./core/fixtures/amenities_list.csv')

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[0].strip()
                if name and not Amenity.objects.filter(name=name).exists():
                    Amenity.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f'Added: {name}'))

# python manage.py import_amenities core/fixtures/amenities_list.csv
