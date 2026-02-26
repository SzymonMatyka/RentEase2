from django.test import TestCase
from .models import LandlordUser, TenantUser
from django.contrib.auth.hashers import make_password, check_password

class UserModelTest(TestCase):
    def setUp(self):
        # Kod wykonywany przed kazdym testem
        password_raw = 'TestPassword123!'
        self.password_hashed = make_password(password_raw)
        self.tenant = TenantUser.objects.create(
            email='anna.najemca@example.com',
            password=self.password_hashed,
            name='Anna',
            surname='Najemca'
        )

    def test_tenant_creation_and_fields(self):
        """Sprawdzenie poprawnosci zmapowanych atrybutow."""
        self.assertEqual(self.tenant.email, 'anna.najemca@example.com')
        self.assertEqual(self.tenant.name, 'Anna')
        
    def test_password_hashing(self):
        """Weryfikacja szyfrowania hasla uzytkownika."""
        self.assertNotEqual(self.tenant.password, 'TestPassword123!')
        self.assertTrue(check_password('TestPassword123!', self.tenant.password))