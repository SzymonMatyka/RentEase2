from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from RentEaseApp.models import LandlordUser, TenantUser, Offer
from datetime import datetime


class Command(BaseCommand):
    help = 'Creates 1 tenant, 1 landlord with all info filled, and 5 offers'

    def handle(self, *args, **options):
        # Create Landlord with all info filled
        landlord, created = LandlordUser.objects.get_or_create(
            email='demo.landlord@rentease.com',
            defaults={
                'name': 'Jan',
                'surname': 'Kowalski',
                'password': make_password('landlord123'),
                'phone_number': '+48 123 456 789',
                'pesel': '85010112345',
                'id_card_number': 'ABC123456',
                'address_city': 'Warsaw',
                'address_street': 'ul. Nowy Świat 15',
                'address_zip_code': '00-001',
                'bank_account_number': 'PL61109010140000071219812874'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created landlord: {landlord.name} {landlord.surname}'))
        else:
            # Update existing landlord with all info
            landlord.phone_number = '+48 123 456 789'
            landlord.pesel = '85010112345'
            landlord.id_card_number = 'ABC123456'
            landlord.address_city = 'Warsaw'
            landlord.address_street = 'ul. Nowy Świat 15'
            landlord.address_zip_code = '00-001'
            landlord.bank_account_number = 'PL61109010140000071219812874'
            landlord.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Updated landlord: {landlord.name} {landlord.surname}'))

        # Create Tenant with all info filled
        tenant, created = TenantUser.objects.get_or_create(
            email='demo.tenant@rentease.com',
            defaults={
                'name': 'Anna',
                'surname': 'Nowak',
                'password': make_password('tenant123'),
                'phone_number': '+48 987 654 321',
                'pesel': '92020267890',
                'id_card_number': 'XYZ987654',
                'address_city': 'Krakow',
                'address_street': 'ul. Floriańska 10',
                'address_zip_code': '31-019',
                'bank_account_number': 'PL27114020040000300201355387'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created tenant: {tenant.name} {tenant.surname}'))
        else:
            # Update existing tenant with all info
            tenant.phone_number = '+48 987 654 321'
            tenant.pesel = '92020267890'
            tenant.id_card_number = 'XYZ987654'
            tenant.address_city = 'Krakow'
            tenant.address_street = 'ul. Floriańska 10'
            tenant.address_zip_code = '31-019'
            tenant.bank_account_number = 'PL27114020040000300201355387'
            tenant.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Updated tenant: {tenant.name} {tenant.surname}'))

        # Create 5 Offers
        offers_data = [
            {
                'title': 'Modern 2-Room Apartment in Warsaw Center',
                'body': 'Beautiful, fully renovated 2-room apartment in the heart of Warsaw. Located on the 5th floor with elevator access. The apartment features modern finishes, large windows, and a spacious balcony with city views. Perfect for professionals or couples. Close to public transport, shopping centers, and restaurants.',
                'location': 'Warsaw, Śródmieście',
                'price': 3500,
                'area': 45,
                'number_of_rooms': 2,
                'floor': '5',
                'sale_or_rent': 'Rent',
                'furnished': 'Yes',
                'condition': 'Renovated',
                'building_type': 'Apartment building',
                'balcony_terrace_garden': 'Balcony',
                'parking': 'Garage',
                'heating': 'Central',
                'elevator': 'Yes',
                'basement': 'Yes',
                'pets_allowed': 'Yes',
                'internet_fiber': 'Yes',
                'square_footage': '45 m²',
                'additional_utilities': 'Water, electricity, heating, internet',
                'admin_fees': 200,
                'deposit': 7000,
                'minimum_rental_period': 12,
                'year_built': 2015
            },
            {
                'title': 'Cozy 1-Room Studio Near University',
                'body': 'Compact and well-designed studio apartment perfect for students or young professionals. Recently renovated with modern kitchen and bathroom. Located in a quiet neighborhood, just 10 minutes walk from the university. Public transport nearby. Ideal for single person.',
                'location': 'Warsaw, Mokotów',
                'price': 2200,
                'area': 28,
                'number_of_rooms': 1,
                'floor': '2',
                'sale_or_rent': 'Rent',
                'furnished': 'Partially',
                'condition': 'Good',
                'building_type': 'Tenement house',
                'balcony_terrace_garden': 'None',
                'parking': 'Street',
                'heating': 'Central',
                'elevator': 'No',
                'basement': 'No',
                'pets_allowed': 'No',
                'internet_fiber': 'Yes',
                'square_footage': '28 m²',
                'additional_utilities': 'Water, electricity, heating',
                'admin_fees': 150,
                'deposit': 4400,
                'minimum_rental_period': 6,
                'year_built': 1985
            },
            {
                'title': 'Luxury 3-Room Apartment with Terrace',
                'body': 'Spacious 3-room apartment in a prestigious location. Features include: large living room with access to private terrace, modern kitchen with island, two bedrooms, and two bathrooms. High-quality finishes throughout. Building includes concierge, gym, and underground parking. Perfect for families.',
                'location': 'Warsaw, Żoliborz',
                'price': 6500,
                'area': 95,
                'number_of_rooms': 3,
                'floor': '8',
                'sale_or_rent': 'Rent',
                'furnished': 'Yes',
                'condition': 'New',
                'building_type': 'Apartment building',
                'balcony_terrace_garden': 'Terrace',
                'parking': 'Garage',
                'heating': 'Underfloor',
                'elevator': 'Yes',
                'basement': 'Yes',
                'pets_allowed': 'Yes',
                'internet_fiber': 'Yes',
                'square_footage': '95 m²',
                'additional_utilities': 'All utilities included',
                'admin_fees': 500,
                'deposit': 13000,
                'minimum_rental_period': 24,
                'year_built': 2020
            },
            {
                'title': 'Charming 2-Room in Historic Building',
                'body': 'Unique 2-room apartment in a beautifully restored historic tenement house. Features original architectural details, high ceilings, and hardwood floors. Located in a vibrant neighborhood with cafes, restaurants, and cultural attractions. Close to public transport.',
                'location': 'Warsaw, Praga',
                'price': 2800,
                'area': 52,
                'number_of_rooms': 2,
                'floor': '3',
                'sale_or_rent': 'Rent',
                'furnished': 'No',
                'condition': 'Renovated',
                'building_type': 'Tenement house',
                'balcony_terrace_garden': 'Balcony',
                'parking': 'No',
                'heating': 'Gas',
                'elevator': 'No',
                'basement': 'Yes',
                'pets_allowed': 'Yes',
                'internet_fiber': 'Yes',
                'square_footage': '52 m²',
                'additional_utilities': 'Water, electricity, gas',
                'admin_fees': 180,
                'deposit': 5600,
                'minimum_rental_period': 12,
                'year_built': 1920
            },
            {
                'title': 'Modern 4-Room Family Apartment',
                'body': 'Large 4-room apartment perfect for families. Features include: spacious living room, modern kitchen, three bedrooms, two bathrooms, and a large balcony. Located in a family-friendly neighborhood with schools, parks, and shopping centers nearby. Building has playground and parking.',
                'location': 'Warsaw, Włochy',
                'price': 4800,
                'area': 120,
                'number_of_rooms': 4,
                'floor': '4',
                'sale_or_rent': 'Rent',
                'furnished': 'Partially',
                'condition': 'Good',
                'building_type': 'Apartment building',
                'balcony_terrace_garden': 'Balcony',
                'parking': 'Yes',
                'heating': 'Central',
                'elevator': 'Yes',
                'basement': 'Yes',
                'pets_allowed': 'Yes',
                'internet_fiber': 'Yes',
                'square_footage': '120 m²',
                'additional_utilities': 'Water, electricity, heating',
                'admin_fees': 300,
                'deposit': 9600,
                'minimum_rental_period': 12,
                'year_built': 2010
            }
        ]

        created_count = 0
        for offer_data in offers_data:
            offer, created = Offer.objects.get_or_create(
                title=offer_data['title'],
                user=landlord,
                defaults=offer_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created offer: {offer.title}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully created/updated:'))
        self.stdout.write(self.style.SUCCESS(f'  - 1 Landlord: {landlord.name} {landlord.surname} ({landlord.email})'))
        self.stdout.write(self.style.SUCCESS(f'  - 1 Tenant: {tenant.name} {tenant.surname} ({tenant.email})'))
        self.stdout.write(self.style.SUCCESS(f'  - {created_count} Offers'))
        self.stdout.write(self.style.SUCCESS(f'\nCredentials:'))
        self.stdout.write(self.style.WARNING(f'  Landlord - Email: {landlord.email}, Password: landlord123'))
        self.stdout.write(self.style.WARNING(f'  Tenant - Email: {tenant.email}, Password: tenant123'))

