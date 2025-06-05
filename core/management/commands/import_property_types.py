import csv
from django.core.management.base import BaseCommand
from core.models import PropertyType

class Command(BaseCommand):
    help = 'Import property types from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                label = row['label']

                obj, created = PropertyType.objects.get_or_create(name=label)
                if created:
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {count} new property types.'))
