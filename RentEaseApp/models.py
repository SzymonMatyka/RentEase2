from django.db import models


class LandlordUser(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Phone number")
    pesel = models.CharField(max_length=11, blank=True, null=True, help_text="Personal Identification Number (PESEL)")
    id_card_number = models.CharField(max_length=50, blank=True, null=True, help_text="Numer Dowodu Osobistego")
    address_city = models.CharField(max_length=100, blank=True, null=True, help_text="City")
    address_street = models.CharField(max_length=200, blank=True, null=True, help_text="Street address")
    address_zip_code = models.CharField(max_length=10, blank=True, null=True, help_text="ZIP/Postal code")
    bank_account_number = models.CharField(max_length=50, blank=True, null=True, help_text="Bank account number for rent payments")

    def __str__(self):
        return f"{self.name} {self.surname}"
    
    def get_full_address(self):
        """Return formatted full address"""
        parts = []
        if self.address_street:
            parts.append(self.address_street)
        if self.address_zip_code:
            parts.append(self.address_zip_code)
        if self.address_city:
            parts.append(self.address_city)
        return ", ".join(parts) if parts else ""


class TenantUser(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Phone number")
    pesel = models.CharField(max_length=11, blank=True, null=True, help_text="Personal Identification Number (PESEL)")
    id_card_number = models.CharField(max_length=50, blank=True, null=True, help_text="Numer Dowodu Osobistego")
    address_city = models.CharField(max_length=100, blank=True, null=True, help_text="City")
    address_street = models.CharField(max_length=200, blank=True, null=True, help_text="Street address")
    address_zip_code = models.CharField(max_length=10, blank=True, null=True, help_text="ZIP/Postal code")
    bank_account_number = models.CharField(max_length=50, blank=True, null=True, help_text="Bank account number for deposit return")

    def __str__(self):
        return f"{self.name} {self.surname}"
    
    def get_full_address(self):
        """Return formatted full address"""
        parts = []
        if self.address_street:
            parts.append(self.address_street)
        if self.address_zip_code:
            parts.append(self.address_zip_code)
        if self.address_city:
            parts.append(self.address_city)
        return ", ".join(parts) if parts else ""


class Offer(models.Model):
    SALE_OR_RENT_CHOICES = [
        ('Sale', 'Sale'),
        ('Rent', 'Rent'),
    ]

    FURNISHED_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Partially', 'Partially'),
    ]

    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Renovated', 'Renovated'),
        ('Good', 'Good'),
        ('Needs renovation', 'Needs renovation'),
    ]

    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    OUTDOOR_SPACE_CHOICES = [
        ('Balcony', 'Balcony'),
        ('Terrace', 'Terrace'),
        ('Garden', 'Garden'),
        ('None', 'None'),
    ]

    HEATING_CHOICES = [
        ('Central', 'Central'),
        ('Gas', 'Gas'),
        ('Electric', 'Electric'),
        ('Underfloor', 'Underfloor'),
        ('None', 'None'),
    ]

    PARKING_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Garage', 'Garage'),
        ('Street', 'Street'),
    ]

    BUILDING_TYPE_CHOICES = [
        ('Apartment building', 'Apartment building'),
        ('Tenement house', 'Tenement house'),
        ('Townhouse', 'Townhouse'),
        ('Detached house', 'Detached house'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Under negotiation', 'Under negotiation'),
        ('Reserved', 'Reserved'),
        ('Unavailable', 'Unavailable'),
        ('Unactive', 'Unactive'),
    ]

    title = models.CharField(max_length=255)
    body = models.TextField(help_text="Content of the post")
    user = models.ForeignKey(
        LandlordUser,
        on_delete=models.CASCADE,
        related_name="offers"
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)

    sale_or_rent = models.CharField(max_length=10, choices=SALE_OR_RENT_CHOICES, default='Rent', blank=True)
    location = models.CharField(max_length=255, blank=True, help_text="City, District, Neighborhood")
    price = models.IntegerField(blank=True, null=True, help_text="Price in currency units")
    area = models.IntegerField(blank=True, null=True, help_text="Area in m²")
    floor = models.CharField(max_length=50, blank=True, help_text="Floor number or 'Ground'")
    furnished = models.CharField(max_length=20, choices=FURNISHED_CHOICES, blank=True)
    number_of_rooms = models.IntegerField(blank=True, null=True)
    year_built = models.IntegerField(blank=True, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True)
    basement = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True)
    balcony_terrace_garden = models.CharField(max_length=20, choices=OUTDOOR_SPACE_CHOICES, blank=True)
    elevator = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True)
    heating = models.CharField(max_length=20, choices=HEATING_CHOICES, blank=True)
    admin_fees = models.IntegerField(blank=True, null=True, help_text="Admin fees / Maintenance in currency units")
    internet_fiber = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True)
    deposit = models.IntegerField(blank=True, null=True, help_text="Deposit in currency units")
    minimum_rental_period = models.IntegerField(blank=True, null=True, help_text="Minimum rental period in months")
    pets_allowed = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=True)
    additional_utilities = models.TextField(blank=True, help_text="Additional utilities (electricity, water, etc.) - text or amount")
    parking = models.CharField(max_length=20, choices=PARKING_CHOICES, blank=True)
    building_type = models.CharField(max_length=50, choices=BUILDING_TYPE_CHOICES, blank=True)
    square_footage = models.TextField(default="", blank=True)
    assigned_user = models.ForeignKey(
        TenantUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_offers",
        help_text="Tenant who rented/bought this offer"
    )

    def __str__(self):
        return self.title


class Photo(models.Model):
    """Photo stored as base64 string in database (no filesystem storage)."""
    photo_data = models.TextField(help_text="Base64-encoded image data")
    content_type = models.CharField(
        max_length=50,
        default="image/jpeg",
        help_text="MIME type (e.g. image/jpeg, image/png)"
    )
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    @property
    def data_uri(self):
        """Return data URI for use in <img src='...'>."""
        if self.photo_data and self.content_type:
            return f"data:{self.content_type};base64,{self.photo_data}"
        return None

    def __str__(self):
        return f"Photo for {self.offer.title}"


class Conversation(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="conversations"
    )
    landlord = models.ForeignKey(
        LandlordUser,
        on_delete=models.CASCADE,
        related_name="conversations_as_landlord"
    )
    tenant = models.ForeignKey(
        TenantUser,
        on_delete=models.CASCADE,
        related_name="conversations_as_tenant"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['offer', 'landlord', 'tenant']

    def __str__(self):
        return f"Conversation for {self.offer.title} - {self.landlord.name} & {self.tenant.name}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender_id = models.IntegerField(help_text="ID of sender (LandlordUser or TenantUser)")
    sender_type = models.CharField(
        max_length=10,
        choices=[('landlord', 'Landlord'), ('tenant', 'Tenant')],
        help_text="Type of sender"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_by_landlord = models.BooleanField(default=False)
    read_by_tenant = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender_type} in conversation {self.conversation.id}"
    
    def mark_as_read(self, user_type):
        """Mark message as read by landlord or tenant"""
        if user_type == 'landlord':
            self.read_by_landlord = True
        elif user_type == 'tenant':
            self.read_by_tenant = True
        self.save()


class Favorite(models.Model):
    """Model to track favorite offers for tenants"""
    tenant = models.ForeignKey(
        TenantUser,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['tenant', 'offer']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tenant.name} favorited {self.offer.title}"


class ContractTemplate(models.Model):
    """Model to store contract templates (assigned to one or many offers)"""
    landlord = models.ForeignKey(
        LandlordUser,
        on_delete=models.CASCADE,
        related_name="contract_templates"
    )
    template_content = models.TextField(help_text="Contract template with placeholders")
    template_structure = models.JSONField(null=True, blank=True, help_text="Structured template data with blocks")
    offers = models.ManyToManyField(
        Offer,
        related_name="contract_templates",
        help_text="Offers this template is assigned to"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        offer_count = self.offers.count()
        return f"Contract Template ({offer_count} offer{'s' if offer_count != 1 else ''})"


class Contract(models.Model):
    """Model to store generated contract instances (for specific tenant-offer pairs)"""
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="contracts"
    )
    tenant = models.ForeignKey(
        TenantUser,
        on_delete=models.CASCADE,
        related_name="contracts"
    )
    landlord = models.ForeignKey(
        LandlordUser,
        on_delete=models.CASCADE,
        related_name="contracts"
    )
    template = models.ForeignKey(
        ContractTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_contracts"
    )
    final_content = models.TextField(blank=True, help_text="Final contract with all placeholders replaced")
    created_at = models.DateTimeField(auto_now_add=True)
    signed_by_tenant = models.BooleanField(default=False)
    signed_by_landlord = models.BooleanField(default=False)
    signed_by_tenant_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when tenant signed")
    signed_by_landlord_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when landlord signed")
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['offer', 'tenant']
    
    def __str__(self):
        return f"Contract for {self.offer.title} - {self.tenant.name}"
