from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.conf import settings
from RentEaseApp.models import LandlordUser, TenantUser, Offer
import random
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'Creates example data: multiple landlord and tenant users, offers, and saves credentials to a text file'

    def handle(self, *args, **options):
        # Store credentials for text file
        credentials = []
        credentials.append("=" * 60)
        credentials.append("RENTEASE - EXAMPLE DATA CREDENTIALS")
        credentials.append("=" * 60)
        credentials.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        credentials.append("")
        
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
        status_options = ['Available', 'Under negotiation', 'Reserved', 'Unavailable', 'Unactive']
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

        # Create landlord users
        landlord_data = [
            {'name': 'John', 'surname': 'Smith', 'email': 'john.smith@example.com', 'password': 'landlord123'},
            {'name': 'Maria', 'surname': 'Kowalski', 'email': 'maria.kowalski@example.com', 'password': 'landlord456'},
            {'name': 'Peter', 'surname': 'Johnson', 'email': 'peter.johnson@example.com', 'password': 'landlord789'},
            {'name': 'Anna', 'surname': 'Nowak', 'email': 'anna.nowak@example.com', 'password': 'landlord321'},
            {'name': 'Robert', 'surname': 'Williams', 'email': 'robert.williams@example.com', 'password': 'landlord654'},
        ]

        landlords = []
        credentials.append("LANDLORD USERS")
        credentials.append("-" * 60)
        
        for landlord_info in landlord_data:
            try:
                landlord = LandlordUser.objects.get(email=landlord_info['email'])
                self.stdout.write(self.style.WARNING(f'Landlord already exists: {landlord.email}'))
            except LandlordUser.DoesNotExist:
                landlord = LandlordUser.objects.create(
                    name=landlord_info['name'],
                    surname=landlord_info['surname'],
                    email=landlord_info['email'],
                    password=make_password(landlord_info['password'])
                )
                self.stdout.write(self.style.SUCCESS(f'Created landlord: {landlord.name} {landlord.surname} ({landlord.email})'))
            
            landlords.append(landlord)
            credentials.append(f"Email: {landlord_info['email']}")
            credentials.append(f"Password: {landlord_info['password']}")
            credentials.append(f"Name: {landlord_info['name']} {landlord_info['surname']}")
            credentials.append("")
        
        credentials.append("")
        credentials.append("TENANT USERS")
        credentials.append("-" * 60)
        
        # Create tenant users
        tenant_data = [
            {'name': 'Michael', 'surname': 'Brown', 'email': 'michael.brown@example.com', 'password': 'tenant123'},
            {'name': 'Sarah', 'surname': 'Davis', 'email': 'sarah.davis@example.com', 'password': 'tenant456'},
            {'name': 'David', 'surname': 'Wilson', 'email': 'david.wilson@example.com', 'password': 'tenant789'},
            {'name': 'Emma', 'surname': 'Miller', 'email': 'emma.miller@example.com', 'password': 'tenant321'},
            {'name': 'James', 'surname': 'Taylor', 'email': 'james.taylor@example.com', 'password': 'tenant654'},
            {'name': 'Olivia', 'surname': 'Anderson', 'email': 'olivia.anderson@example.com', 'password': 'tenant987'},
        ]

        tenants = []
        for tenant_info in tenant_data:
            try:
                tenant = TenantUser.objects.get(email=tenant_info['email'])
                self.stdout.write(self.style.WARNING(f'Tenant already exists: {tenant.email}'))
            except TenantUser.DoesNotExist:
                tenant = TenantUser.objects.create(
                    name=tenant_info['name'],
                    surname=tenant_info['surname'],
                    email=tenant_info['email'],
                    password=make_password(tenant_info['password'])
                )
                self.stdout.write(self.style.SUCCESS(f'Created tenant: {tenant.name} {tenant.surname} ({tenant.email})'))
            
            tenants.append(tenant)
            credentials.append(f"Email: {tenant_info['email']}")
            credentials.append(f"Password: {tenant_info['password']}")
            credentials.append(f"Name: {tenant_info['name']} {tenant_info['surname']}")
            credentials.append("")
        
        credentials.append("")
        credentials.append("=" * 60)
        credentials.append("END OF CREDENTIALS")
        credentials.append("=" * 60)
        
        # Save credentials to file (in the RentEase project root directory)
        # Use Django's BASE_DIR which points to the RentEase directory
        credentials_file_path = os.path.join(settings.BASE_DIR, 'example_users_credentials.txt')
        with open(credentials_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(credentials))
        
        self.stdout.write(self.style.SUCCESS(f'\nCredentials saved to: {credentials_file_path}'))
        
        # Create offers for landlords
        self.stdout.write(self.style.SUCCESS('\nCreating offers...'))
        created_offers_count = 0
        
        for i, landlord in enumerate(landlords):
            # Each landlord gets 3-5 offers
            num_offers = random.randint(3, 5)
            
            for j in range(num_offers):
                offer_idx = created_offers_count % len(descriptions)
                sale_or_rent = random.choice(['Sale', 'Rent'])
                base_price = random.randint(1500, 5000) if sale_or_rent == 'Rent' else random.randint(300000, 800000)
                area = random.randint(25, 120)
                rooms = random.choice([1, 2, 3, 4, 5])
                floor_num = random.choice(['Ground', '1', '2', '3', '4', '5', '6', '7', '8'])
                year = random.randint(1950, 2023)
                
                offer = Offer.objects.create(
                    title=f"Apartment {created_offers_count+1} - {random.choice(['Modern', 'Cozy', 'Spacious', 'Luxury', 'Charming', 'Bright', 'Renovated'])} {rooms}-Room",
                    body=descriptions[offer_idx],
                    user=landlord,
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
                created_offers_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created offer {created_offers_count}: {offer.title} (by {landlord.name} {landlord.surname})'))
        
        self.stdout.write(self.style.SUCCESS(f'\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS(f'Successfully created:'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(landlords)} landlord users'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(tenants)} tenant users'))
        self.stdout.write(self.style.SUCCESS(f'  - {created_offers_count} offers'))
        self.stdout.write(self.style.SUCCESS(f'  - Credentials saved to: {credentials_file_path}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

