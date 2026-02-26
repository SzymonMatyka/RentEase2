from django import forms
from .models import LandlordUser, TenantUser, Offer
from django.contrib.auth.hashers import make_password, check_password


class ContractPlaceholderForm(forms.Form):
    """
    Form that defines all available contract placeholder fields.
    This serves as the single source of truth for contract variables.
    Fields are organized by category for UI rendering.
    """

    tenant_name = forms.CharField(label='Tenant Name', required=False)
    tenant_surname = forms.CharField(label='Tenant Surname', required=False)
    tenant_full_name = forms.CharField(label='Full Name', required=False)
    tenant_pesel = forms.CharField(label='PESEL', required=False)
    tenant_id_card = forms.CharField(label='ID Card Number', required=False)
    tenant_address = forms.CharField(label='Address', required=False)
    tenant_phone = forms.CharField(label='Phone', required=False)
    tenant_email = forms.CharField(label='Email', required=False)
    tenant_bank_account = forms.CharField(label='Bank Account', required=False)
    landlord_name = forms.CharField(label='Landlord Name', required=False)
    landlord_surname = forms.CharField(label='Landlord Surname', required=False)
    landlord_full_name = forms.CharField(label='Full Name', required=False)
    landlord_pesel = forms.CharField(label='PESEL', required=False)
    landlord_id_card = forms.CharField(label='ID Card Number', required=False)
    landlord_address = forms.CharField(label='Address', required=False)
    landlord_phone = forms.CharField(label='Phone', required=False)
    landlord_email = forms.CharField(label='Email', required=False)
    landlord_bank_account = forms.CharField(label='Bank Account', required=False)
    property_title = forms.CharField(label='Property Title', required=False)
    property_location = forms.CharField(label='Location', required=False)
    property_price = forms.CharField(label='Price', required=False)
    property_area = forms.CharField(label='Area', required=False)
    property_rooms = forms.CharField(label='Rooms', required=False)
    property_floor = forms.CharField(label='Floor', required=False)
    property_description = forms.CharField(label='Description', required=False)
    
    @classmethod
    def get_field_groups(cls):
        """
        Returns field groups organized by category for UI rendering.
        Each group contains (category_name, fields_list).
        """
        return [
            ('tenant', [
                ('tenant_name', 'Tenant Name'),
                ('tenant_surname', 'Tenant Surname'),
                ('tenant_full_name', 'Full Name'),
                ('tenant_pesel', 'PESEL'),
                ('tenant_id_card', 'ID Card Number'),
                ('tenant_address', 'Address'),
                ('tenant_phone', 'Phone'),
                ('tenant_email', 'Email'),
                ('tenant_bank_account', 'Bank Account'),
            ]),
            ('landlord', [
                ('landlord_name', 'Landlord Name'),
                ('landlord_surname', 'Landlord Surname'),
                ('landlord_full_name', 'Full Name'),
                ('landlord_pesel', 'PESEL'),
                ('landlord_id_card', 'ID Card Number'),
                ('landlord_address', 'Address'),
                ('landlord_phone', 'Phone'),
                ('landlord_email', 'Email'),
                ('landlord_bank_account', 'Bank Account'),
            ]),
            ('property', [
                ('property_title', 'Property Title'),
                ('property_location', 'Location'),
                ('property_price', 'Price'),
                ('property_area', 'Area'),
                ('property_rooms', 'Rooms'),
                ('property_floor', 'Floor'),
                ('property_description', 'Description'),
            ]),
        ]


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs.setdefault('multiple', True)
        self.attrs = attrs

    def value_from_datadict(self, data, files, name):
        try:
            file_list = files.getlist(name)
        except AttributeError:
            file_list = [f for f in [files.get(name)] if f]
        return file_list[0] if file_list else None


class RegisterForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        data = self.cleaned_data
        password_hashed = make_password(data['password'])
        if data['user_type'] == 'landlord':
            return LandlordUser.objects.create(
                name=data['name'],
                surname=data['surname'],
                email=data['email'],
                password=password_hashed,
            )
        else:
            return TenantUser.objects.create(
                name=data['name'],
                surname=data['surname'],
                email=data['email'],
                password=password_hashed,
            )


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileEditForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    surname = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    current_password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep current password")
    new_password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep current password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    surname = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep current password")
    phone_number = forms.CharField(max_length=20, required=False, help_text="Phone number")
    pesel = forms.CharField(max_length=11, required=False, help_text="Personal Identification Number (PESEL) - 11 digits")
    id_card_number = forms.CharField(max_length=50, required=False, help_text="Numer Dowodu Osobistego")
    address_street = forms.CharField(max_length=200, required=False, help_text="Street address")
    address_zip_code = forms.CharField(max_length=10, required=False, help_text="ZIP/Postal code")
    address_city = forms.CharField(max_length=100, required=False, help_text="City")
    bank_account_number = forms.CharField(max_length=50, required=False, help_text="Bank account number")
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.user_type = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['name'].initial = self.user.name
            self.fields['surname'].initial = self.user.surname
            self.fields['email'].initial = self.user.email
            self.fields['phone_number'].initial = self.user.phone_number
            self.fields['pesel'].initial = self.user.pesel
            self.fields['id_card_number'].initial = self.user.id_card_number
            self.fields['address_street'].initial = self.user.address_street
            self.fields['address_zip_code'].initial = self.user.address_zip_code
            self.fields['address_city'].initial = self.user.address_city
            self.fields['bank_account_number'].initial = self.user.bank_account_number
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.user and email != self.user.email:
            if self.user_type == 'landlord':
                if LandlordUser.objects.filter(email=email).exclude(id=self.user.id).exists():
                    raise forms.ValidationError("This email is already registered.")
            elif self.user_type == 'tenant':
                if TenantUser.objects.filter(email=email).exclude(id=self.user.id).exists():
                    raise forms.ValidationError("This email is already registered.")
        return email
    
    def clean_pesel(self):
        pesel = self.cleaned_data.get('pesel')
        if pesel and len(pesel) != 11:
            raise forms.ValidationError("PESEL must be exactly 11 digits.")
        if pesel and not pesel.isdigit():
            raise forms.ValidationError("PESEL must contain only digits.")
        return pesel
    
    def save(self):
        data = self.cleaned_data
        if self.user:
            self.user.name = data['name']
            self.user.surname = data['surname']
            self.user.email = data['email']
            if data['password']:
                from django.contrib.auth.hashers import make_password
                self.user.password = make_password(data['password'])
            self.user.phone_number = data.get('phone_number', '') or None
            self.user.pesel = data.get('pesel', '') or None
            self.user.id_card_number = data.get('id_card_number', '') or None
            self.user.address_street = data.get('address_street', '') or None
            self.user.address_zip_code = data.get('address_zip_code', '') or None
            self.user.address_city = data.get('address_city', '') or None
            self.user.bank_account_number = data.get('bank_account_number', '') or None
            
            self.user.save()
            return self.user
        return None


class OfferForm(forms.ModelForm):
    photos = forms.FileField(
        widget=MultipleFileInput(attrs={
            'class': 'file-input',
            'accept': 'image/*',
        }),
        required=False,
        help_text='Upload one or more images (drag and drop or click to select)'
    )
    
    class Meta:
        model = Offer
        fields = [
            'title', 'body', 'status', 'sale_or_rent', 'location', 'price', 'area',
            'floor', 'furnished', 'number_of_rooms', 'year_built', 'condition',
            'basement', 'balcony_terrace_garden', 'elevator', 'heating', 'admin_fees',
            'internet_fiber', 'deposit', 'minimum_rental_period', 'pets_allowed',
            'additional_utilities', 'parking', 'building_type'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'sale_or_rent': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'floor': forms.TextInput(attrs={'class': 'form-control'}),
            'furnished': forms.Select(attrs={'class': 'form-control'}),
            'number_of_rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'year_built': forms.NumberInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'basement': forms.Select(attrs={'class': 'form-control'}),
            'balcony_terrace_garden': forms.Select(attrs={'class': 'form-control'}),
            'elevator': forms.Select(attrs={'class': 'form-control'}),
            'heating': forms.Select(attrs={'class': 'form-control'}),
            'admin_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'internet_fiber': forms.Select(attrs={'class': 'form-control'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control'}),
            'minimum_rental_period': forms.NumberInput(attrs={'class': 'form-control'}),
            'pets_allowed': forms.Select(attrs={'class': 'form-control'}),
            'additional_utilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parking': forms.Select(attrs={'class': 'form-control'}),
            'building_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'body': 'Description',
            'status': 'Status',
            'sale_or_rent': 'Sale or Rent',
            'location': 'Location (City, District, Neighborhood)',
            'price': 'Price (zł)',
            'area': 'Area (m²)',
            'floor': 'Floor',
            'furnished': 'Furnished',
            'number_of_rooms': 'Number of Rooms',
            'year_built': 'Year Built',
            'condition': 'Condition',
            'basement': 'Basement',
            'balcony_terrace_garden': 'Balcony / Terrace / Garden',
            'elevator': 'Elevator',
            'heating': 'Heating',
            'admin_fees': 'Admin Fees / Maintenance (zł)',
            'internet_fiber': 'Internet / Fiber Availability',
            'deposit': 'Deposit (zł)',
            'minimum_rental_period': 'Minimum Rental Period (months)',
            'pets_allowed': 'Pets Allowed',
            'additional_utilities': 'Additional Utilities (electricity, water, etc.)',
            'parking': 'Parking',
            'building_type': 'Building Type',
        }
        help_texts = {
            'floor': 'Enter floor number or "Ground"',
            'additional_utilities': 'Enter text description or amount',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sale_or_rent'].required = True
        self.fields['location'].required = True
        self.fields['price'].required = True
        self.fields['area'].required = True
    

