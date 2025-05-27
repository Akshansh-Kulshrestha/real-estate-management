import csv
from django.core.management.base import BaseCommand
from core.models import Location  # adjust if your model is elsewhere

class Command(BaseCommand):
    help = 'Import Indian city/location data from CSV'

    def handle(self, *args, **kwargs):
        with open('core/fixtures/Cities_in_India_with_pincodes.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                state = row['State'].strip()
                city = row['District'].strip()
                area = row['Location'].strip()
                pincode = row['Pincode'].strip()

                if state and city and area and pincode:
                    Location.objects.get_or_create(
                        country='India',
                        state=state,
                        city=city,
                        area=area,
                        pincode=pincode
                    )
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'Imported {count} locations successfully.'))
