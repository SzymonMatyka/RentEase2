from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from RentEaseApp.models import LandlordUser, Offer
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Creates 20 example offers for user with email la@gmail.com'

    def handle(self, *args, **options):
        # Get or create the user
        email = 'la@gmail.com'
        try:
            user = LandlordUser.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f'Found existing user: {user.name} {user.surname}'))
        except LandlordUser.DoesNotExist:
            user = LandlordUser.objects.create(
                name='Example',
                surname='Landlord',
                email=email,
                password=make_password('password123')
            )
            self.stdout.write(self.style.SUCCESS(f'Created new user: {user.name} {user.surname}'))

        # Sample data for variety
        locations = [
            'Warsaw, Śródmieście, Nowy Świat',
            'Kraków, Stare Miasto, Rynek Główny',
            'Gdańsk, Śródmieście, Długi Targ',
            'Wrocław, Stare Miasto, Rynek',
            'Poznań, Stare Miasto, Stary Rynek',
            'Łódź, Śródmieście, Piotrkowska',
            'Katowice, Centrum, Mariacka',
            'Lublin, Stare Miasto, Krakowskie Przedmieście',
            'Szczecin, Centrum, Wały Chrobrego',
            'Bydgoszcz, Śródmieście, Długi Rynek',
        ]

        building_types = ['Apartment building', 'Tenement house', 'Townhouse', 'Detached house']
        furnished_options = ['Yes', 'No', 'Partially']
        condition_options = ['New', 'Renovated', 'Good', 'Needs renovation']
        outdoor_options = ['Balcony', 'Terrace', 'Garden', 'None']
        heating_options = ['Central', 'Gas', 'Electric', 'Underfloor', 'None']
        parking_options = ['Yes', 'No', 'Garage', 'Street']
        status_options = ['Available', 'Under negotiation', 'Reserved', 'Unactive']
        yes_no = ['Yes', 'No']

        descriptions = [
            "Beautiful apartment in the heart of the city. Recently renovated with modern amenities. Perfect for professionals or small families. Close to public transport and shopping centers.",
            "Spacious apartment with stunning views. Features large windows, modern kitchen, and comfortable living space. Located in a quiet neighborhood with excellent access to schools and parks.",
            "Charming apartment in historic building. High ceilings, original features preserved. Close to city center with all amenities nearby. Perfect for those who appreciate character.",
            "Modern apartment with contemporary design. Fully equipped kitchen, comfortable bedrooms, and bright living area. Building includes elevator and parking space.",
            "Cozy apartment ideal for students or young professionals. Well-maintained building with friendly neighbors. Great location near university and public transport.",
            "Luxury apartment with premium finishes. Features include marble floors, designer kitchen, and spacious balcony. Building has concierge and security.",
            "Family-friendly apartment with multiple bedrooms. Safe neighborhood with playgrounds nearby. Good schools in the area. Perfect for families with children.",
            "Studio apartment perfect for single person or couple. Efficient use of space with modern appliances. Located in vibrant area with many restaurants and cafes.",
            "Penthouse apartment with panoramic city views. Large terrace, premium materials throughout. Exclusive building with top amenities.",
            "Ground floor apartment with private garden access. Ideal for those who prefer not to use stairs. Quiet location with easy access to main roads.",
            "Renovated apartment with original charm. Beautiful hardwood floors, modern bathroom, and updated kitchen. Great investment opportunity.",
            "Bright and airy apartment with lots of natural light. South-facing windows, modern design, and energy-efficient features. Eco-friendly building.",
            "Apartment in new development. Modern construction with latest technology. Smart home features included. Brand new building with warranty.",
            "Traditional apartment with modern updates. Mix of classic and contemporary design. Located in prestigious area with excellent reputation.",
            "Compact apartment with smart storage solutions. Well-designed layout maximizes space. Perfect for minimalists or those who travel frequently.",
            "Apartment with home office space. Separate room ideal for remote work. High-speed internet ready. Quiet environment for productivity.",
            "Pet-friendly apartment with easy access to parks. Building allows pets. Large windows and good ventilation. Great for pet owners.",
            "Apartment near business district. Short commute to major companies. Modern amenities and professional atmosphere. Ideal for business professionals.",
            "Apartment with storage room included. Extra space for belongings. Building has bike storage and package room. Convenient for active lifestyle.",
            "Affordable apartment in good condition. Well-maintained building with responsive management. Great value for money. Suitable for first-time renters.",
        ]

        # Create 20 offers
        created_count = 0
        for i in range(20):
            # Vary the data for each offer
            sale_or_rent = random.choice(['Sale', 'Rent'])
            base_price = random.randint(1500, 5000) if sale_or_rent == 'Rent' else random.randint(300000, 800000)
            area = random.randint(25, 120)
            rooms = random.choice([1, 2, 3, 4, 5])
            floor_num = random.choice(['Ground', '1', '2', '3', '4', '5', '6', '7', '8'])
            year = random.randint(1950, 2023)
            
            offer = Offer.objects.create(
                title=f"Apartment {i+1} - {random.choice(['Modern', 'Cozy', 'Spacious', 'Luxury', 'Charming', 'Bright', 'Renovated'])} {rooms}-Room",
                body=descriptions[i],
                user=user,
                status=random.choice(status_options),
                sale_or_rent=sale_or_rent,
                location=random.choice(locations),
                price=base_price,
                area=area,
                floor=floor_num,
                furnished=random.choice(furnished_options),
                number_of_rooms=rooms,
                year_built=year,
                condition=random.choice(condition_options),
                basement=random.choice(yes_no),
                balcony_terrace_garden=random.choice(outdoor_options),
                elevator=random.choice(yes_no) if floor_num not in ['Ground', '1', '2'] else 'No',
                heating=random.choice(heating_options),
                admin_fees=random.randint(200, 800) if sale_or_rent == 'Rent' else None,
                internet_fiber=random.choice(yes_no),
                deposit=random.randint(2000, 5000) if sale_or_rent == 'Rent' else None,
                minimum_rental_period=random.choice([6, 12, 24]) if sale_or_rent == 'Rent' else None,
                pets_allowed=random.choice(yes_no),
                additional_utilities=random.choice([
                    "Included in rent",
                    "Electricity: ~200 zł/month, Water: ~100 zł/month",
                    "All utilities included",
                    "Separate billing for utilities",
                    "Utilities: ~300 zł/month"
                ]),
                parking=random.choice(parking_options),
                building_type=random.choice(building_types),
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created offer {created_count}/20: {offer.title}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} offers for {user.email}'))

