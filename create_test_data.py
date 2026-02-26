#!/usr/bin/env python3
"""
Script to create test data: 1 tenant, 1 landlord, and 5 offers
"""
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RentEase.settings')
django.setup()

from RentEaseApp.models import LandlordUser, TenantUser, Offer
from django.contrib.auth.hashers import make_password

def create_test_data():
    landlord, created = LandlordUser.objects.get_or_create(
        email='test.landlord@example.com',
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
            'bank_account_number': 'PL61 1090 1014 0000 7121 9812 2876'
        }
    )
    
    if created:
        print(f"✅ Created landlord: {landlord.name} {landlord.surname} ({landlord.email})")
    else:
        print(f"ℹ️  Landlord already exists: {landlord.name} {landlord.surname} ({landlord.email})")

    tenant, created = TenantUser.objects.get_or_create(
        email='test.tenant@example.com',
        defaults={
            'name': 'Anna',
            'surname': 'Nowak',
            'password': make_password('tenant123'),
            'phone_number': '+48 987 654 321',
            'pesel': '92020298765',
            'id_card_number': 'XYZ987654',
            'address_city': 'Krakow',
            'address_street': 'ul. Floriańska 20',
            'address_zip_code': '31-019',
            'bank_account_number': 'PL12 3456 7890 1234 5678 9012 3456'
        }
    )
    
    if created:
        print(f"✅ Created tenant: {tenant.name} {tenant.surname} ({tenant.email})")
    else:
        print(f"ℹ️  Tenant already exists: {tenant.name} {tenant.surname} ({tenant.email})")

    offers_data = [
        {
            'title': 'Modern 2-Bedroom Apartment in Warsaw Center',
            'body': 'Beautiful, fully furnished apartment in the heart of Warsaw. Perfect for professionals. Features modern kitchen, spacious living room, and two comfortable bedrooms. Close to public transport and shopping centers.',
            'location': 'Warsaw, Śródmieście',
            'price': 3500,
            'area': 65,
            'number_of_rooms': 2,
            'floor': '5th floor',
            'sale_or_rent': 'Rent',
            'furnished': 'Yes',
            'condition': 'Renovated',
            'building_type': 'Apartment building',
            'heating': 'Central',
            'parking': 'Garage',
            'balcony_terrace_garden': 'Balcony',
            'elevator': 'Yes',
            'basement': 'Yes',
            'internet_fiber': 'Yes',
            'pets_allowed': 'Yes',
            'minimum_rental_period': 12,
            'deposit': 3500,
            'admin_fees': 200,
            'square_footage': '65 m²',
            'additional_utilities': 'Water, heating included',
            'year_built': 2015,
        },
        {
            'title': 'Cozy Studio Apartment Near University',
            'body': 'Compact and well-designed studio apartment ideal for students or young professionals. Recently renovated with modern amenities. Quiet neighborhood, close to university campus.',
            'location': 'Krakow, Stare Miasto',
            'price': 2200,
            'area': 35,
            'number_of_rooms': 1,
            'floor': '2nd floor',
            'sale_or_rent': 'Rent',
            'furnished': 'Partially',
            'condition': 'Good',
            'building_type': 'Tenement house',
            'heating': 'Central',
            'parking': 'Street',
            'balcony_terrace_garden': 'None',
            'elevator': 'No',
            'basement': 'No',
            'internet_fiber': 'Yes',
            'pets_allowed': 'No',
            'minimum_rental_period': 6,
            'deposit': 2200,
            'admin_fees': 150,
            'square_footage': '35 m²',
            'additional_utilities': 'All utilities included',
            'year_built': 1985,
        },
        {
            'title': 'Luxury 3-Bedroom Apartment with Terrace',
            'body': 'Spacious luxury apartment with stunning city views. Features high-end finishes, modern appliances, and a private terrace. Perfect for families. Located in prestigious neighborhood.',
            'location': 'Warsaw, Mokotów',
            'price': 6500,
            'area': 120,
            'number_of_rooms': 3,
            'floor': '12th floor',
            'sale_or_rent': 'Rent',
            'furnished': 'Yes',
            'condition': 'New',
            'building_type': 'Apartment building',
            'heating': 'Underfloor',
            'parking': 'Garage',
            'balcony_terrace_garden': 'Terrace',
            'elevator': 'Yes',
            'basement': 'Yes',
            'internet_fiber': 'Yes',
            'pets_allowed': 'Yes',
            'minimum_rental_period': 24,
            'deposit': 6500,
            'admin_fees': 500,
            'square_footage': '120 m²',
            'additional_utilities': 'All utilities included',
            'year_built': 2020,
        },
        {
            'title': 'Charming 1-Bedroom in Historic Building',
            'body': 'Beautifully restored apartment in a historic tenement building. Features original architectural details combined with modern amenities. Quiet street, close to parks and cafes.',
            'location': 'Gdansk, Old Town',
            'price': 2800,
            'area': 45,
            'number_of_rooms': 1,
            'floor': '3rd floor',
            'sale_or_rent': 'Rent',
            'furnished': 'No',
            'condition': 'Renovated',
            'building_type': 'Tenement house',
            'heating': 'Central',
            'parking': 'No',
            'balcony_terrace_garden': 'None',
            'elevator': 'No',
            'basement': 'Yes',
            'internet_fiber': 'Yes',
            'pets_allowed': 'No',
            'minimum_rental_period': 12,
            'deposit': 2800,
            'admin_fees': 180,
            'square_footage': '45 m²',
            'additional_utilities': 'Water included',
            'year_built': 1920,
        },
        {
            'title': 'Family-Friendly 4-Bedroom House with Garden',
            'body': 'Spacious family house with large garden, perfect for families with children. Features modern kitchen, multiple bathrooms, and plenty of storage space. Quiet residential area.',
            'location': 'Wroclaw, Krzyki',
            'price': 5500,
            'area': 150,
            'number_of_rooms': 4,
            'floor': 'Ground floor',
            'sale_or_rent': 'Rent',
            'furnished': 'Partially',
            'condition': 'Good',
            'building_type': 'Detached house',
            'heating': 'Gas',
            'parking': 'Yes',
            'balcony_terrace_garden': 'Garden',
            'elevator': 'No',
            'basement': 'Yes',
            'internet_fiber': 'Yes',
            'pets_allowed': 'Yes',
            'minimum_rental_period': 24,
            'deposit': 5500,
            'admin_fees': 300,
            'square_footage': '150 m²',
            'additional_utilities': 'All utilities included',
            'year_built': 2010,
        },
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
            print(f"✅ Created offer: {offer.title}")
        else:
            print(f"ℹ️  Offer already exists: {offer.title}")
    
    print(f"\n📊 Summary:")
    print(f"   - Landlord: {landlord.name} {landlord.surname}")
    print(f"   - Tenant: {tenant.name} {tenant.surname}")
    print(f"   - Offers created: {created_count}/5")
    print(f"\n🔑 Login Credentials:")
    print(f"   Landlord: {landlord.email} / landlord123")
    print(f"   Tenant: {tenant.email} / tenant123")

if __name__ == '__main__':
    create_test_data()


