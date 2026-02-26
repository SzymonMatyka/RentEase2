from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from RentEaseApp.models import LandlordUser, Offer, Photo
import base64
import random
import os
import glob
from django.conf import settings

class Command(BaseCommand):
    help = 'Deletes all offers and creates new realistic offers for john.smith@example.com'

    def handle(self, *args, **options):
        offer_count = Offer.objects.count()
        Offer.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Deleted {offer_count} existing offers'))
        email = 'john.smith@example.com'
        try:
            landlord = LandlordUser.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f'Found existing landlord: {landlord.name} {landlord.surname}'))
        except LandlordUser.DoesNotExist:
            landlord = LandlordUser.objects.create(
                name='John',
                surname='Smith',
                email=email,
                password=make_password('landlord123')
            )
            self.stdout.write(self.style.SUCCESS(f'Created new landlord: {landlord.name} {landlord.surname}'))
        media_path = os.path.join(settings.MEDIA_ROOT, 'offers_photos')
        photo_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            photo_files.extend(glob.glob(os.path.join(media_path, ext)))
        
        photo_files = sorted(photo_files)
        self.stdout.write(self.style.SUCCESS(f'Found {len(photo_files)} photos'))
        max_offers = len(photo_files) // 2
        num_offers = max_offers
        self.stdout.write(self.style.SUCCESS(f'Will create {num_offers} offers'))
        polish_locations = [
            'Warsaw, Śródmieście, Nowy Świat',
            'Warsaw, Mokotów, Puławska',
            'Warsaw, Żoliborz, Krasińskiego',
            'Kraków, Stare Miasto, Rynek Główny',
            'Kraków, Kazimierz, Krakowska',
            'Kraków, Podgórze, Kalwaryjska',
            'Gdańsk, Śródmieście, Długi Targ',
            'Gdańsk, Oliwa, Grunwaldzka',
            'Wrocław, Stare Miasto, Rynek',
            'Wrocław, Krzyki, Legnicka',
            'Poznań, Stare Miasto, Stary Rynek',
            'Poznań, Jeżyce, Dąbrowskiego',
            'Łódź, Śródmieście, Piotrkowska',
        ]
        descriptions = [
            "Piękne mieszkanie w samym sercu miasta. Niedawno wyremontowane z nowoczesnymi udogodnieniami. Idealne dla profesjonalistów lub małych rodzin. Blisko transportu publicznego i centrów handlowych.",
            "Przestronne mieszkanie z oszałamiającym widokiem. Duże okna, nowoczesna kuchnia i wygodna przestrzeń życiowa. Położone w spokojnej dzielnicy z doskonałym dostępem do szkół i parków.",
            "Urokliwe mieszkanie w zabytkowym budynku. Wysokie sufity, zachowane oryginalne elementy. Blisko centrum miasta ze wszystkimi udogodnieniami w pobliżu. Idealne dla tych, którzy doceniają charakter.",
            "Nowoczesne mieszkanie w stylu współczesnym. W pełni wyposażona kuchnia, wygodne sypialnie i jasna przestrzeń dzienna. Budynek z windą i miejscem parkingowym.",
            "Przytulne mieszkanie idealne dla studentów lub młodych profesjonalistów. Dobrze utrzymany budynek z przyjaznymi sąsiadami. Doskonała lokalizacja przy uniwersytecie i transporcie publicznym.",
            "Luksusowe mieszkanie z wysokiej klasy wykończeniami. Marmurowe podłogi, designerska kuchnia i przestronny balkon. Budynek z portiernią i ochroną.",
            "Mieszkanie przyjazne rodzinom z wieloma sypialniami. Bezpieczna dzielnica z placami zabaw w pobliżu. Dobre szkoły w okolicy. Idealne dla rodzin z dziećmi.",
            "Kawalerka idealna dla jednej osoby lub pary. Efektywne wykorzystanie przestrzeni z nowoczesnymi urządzeniami. Położone w tętniącej życiem okolicy z wieloma restauracjami i kawiarniami.",
            "Mieszkanie na parterze z dostępem do prywatnego ogrodu. Idealne dla tych, którzy wolą nie używać schodów. Spokojna lokalizacja z łatwym dostępem do głównych dróg.",
            "Wyremontowane mieszkanie z oryginalnym urokiem. Piękne drewniane podłogi, nowoczesna łazienka i zaktualizowana kuchnia. Świetna okazja inwestycyjna.",
            "Jasne i przestronne mieszkanie z dużą ilością naturalnego światła. Okna skierowane na południe, nowoczesny design i energooszczędne funkcje. Ekologiczny budynek.",
            "Mieszkanie w nowej inwestycji. Nowoczesna konstrukcja z najnowszą technologią. Funkcje inteligentnego domu w zestawie. Nowy budynek z gwarancją.",
            "Tradycyjne mieszkanie z nowoczesnymi aktualizacjami. Mieszanka klasycznego i współczesnego designu. Położone w prestiżowej okolicy z doskonałą reputacją.",
        ]
        apartment_types = [
            ('Modern', 'Nowoczesne'),
            ('Cozy', 'Przytulne'),
            ('Spacious', 'Przestronne'),
            ('Luxury', 'Luksusowe'),
            ('Charming', 'Urokliwe'),
            ('Bright', 'Jasne'),
            ('Renovated', 'Wyremontowane'),
            ('Historic', 'Zabytkowe'),
            ('Contemporary', 'Współczesne'),
            ('Elegant', 'Eleganckie'),
            ('Comfortable', 'Komfortowe'),
            ('Stylish', 'Stylowe'),
            ('Premium', 'Premium'),
        ]

        building_types = ['Apartment building', 'Tenement house', 'Townhouse', 'Detached house']
        furnished_options = ['Yes', 'No', 'Partially']
        condition_options = ['New', 'Renovated', 'Good', 'Needs renovation']
        outdoor_options = ['Balcony', 'Terrace', 'Garden', 'None']
        heating_options = ['Central', 'Gas', 'Electric', 'Underfloor', 'None']
        parking_options = ['Yes', 'No', 'Garage', 'Street']
        yes_no = ['Yes', 'No']
        photo_index = 0
        created_count = 0

        for i in range(num_offers):
            sale_or_rent = random.choice(['Sale', 'Rent'])
            if sale_or_rent == 'Rent':
                base_price = random.randint(1500, 6000)
            else:
                area = random.randint(30, 120)
                price_per_sqm = random.randint(4000, 12000)
                base_price = area * price_per_sqm
            rooms = random.choice([1, 2, 3, 4, 5])
            if rooms == 1:
                area = random.randint(25, 45)
            elif rooms == 2:
                area = random.randint(40, 65)
            elif rooms == 3:
                area = random.randint(55, 85)
            elif rooms == 4:
                area = random.randint(75, 110)
            else:
                area = random.randint(100, 150)
            
            floor_num = random.choice(['Ground', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
            year = random.randint(1950, 2023)
            
            apt_type_en, apt_type_pl = random.choice(apartment_types)
            location = random.choice(polish_locations)
            offer = Offer.objects.create(
                title=f"Mieszkanie {i+1} - {apt_type_pl} {rooms}-pokojowe",
                body=descriptions[i % len(descriptions)],
                user=landlord,
                status='Available',
                sale_or_rent=sale_or_rent,
                location=location,
                price=base_price,
                area=area,
                floor=floor_num,
                furnished=random.choice(furnished_options),
                number_of_rooms=rooms,
                year_built=year,
                condition=random.choice(condition_options),
                basement=random.choice(yes_no),
                balcony_terrace_garden=random.choice(outdoor_options),
                elevator='Yes' if floor_num not in ['Ground', '1', '2'] and random.random() > 0.3 else 'No',
                heating=random.choice(heating_options),
                admin_fees=random.randint(200, 800) if sale_or_rent == 'Rent' else None,
                internet_fiber=random.choice(yes_no),
                deposit=random.randint(2000, 5000) if sale_or_rent == 'Rent' else None,
                minimum_rental_period=random.choice([6, 12, 24]) if sale_or_rent == 'Rent' else None,
                pets_allowed=random.choice(yes_no),
                additional_utilities=random.choice([
                    "Wliczone w czynsz",
                    "Prąd: ~200 zł/miesiąc, Woda: ~100 zł/miesiąc",
                    "Wszystkie media wliczone",
                    "Osobne rozliczenie za media",
                    "Media: ~300 zł/miesiąc"
                ]),
                parking=random.choice(parking_options),
                building_type=random.choice(building_types),
            )
            for j in range(2):
                if photo_index < len(photo_files):
                    photo_path = photo_files[photo_index]
                    with open(photo_path, 'rb') as f:
                        photo_data = base64.b64encode(f.read()).decode('utf-8')
                    ext = os.path.splitext(photo_path)[1].lower()
                    content_types = {
                        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                        '.png': 'image/png', '.gif': 'image/gif',
                        '.webp': 'image/webp',
                    }
                    content_type = content_types.get(ext, 'image/jpeg')
                    Photo.objects.create(
                        offer=offer,
                        photo_data=photo_data,
                        content_type=content_type
                    )
                    photo_index += 1

            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created offer {created_count}/{num_offers}: {offer.title} ({location})'))

        self.stdout.write(self.style.SUCCESS(f'\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} offers for {landlord.email}'))
        self.stdout.write(self.style.SUCCESS(f'Used {photo_index} photos (2 per offer)'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
