from django.test import TestCase
from django.utils import timezone
from apps.account.models import Account, UserConfirmation, STUDENT, NEW
from datetime import timedelta


class AccountModelTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create(
            username="testuser",
            full_name="Test User",
            phone_number="+998901234567",
            date_of_birth="1990-01-01",
            user_role=STUDENT
        )

    def test_account_creation(self):
        self.assertEqual(self.user.full_name, "Test User")
        self.assertEqual(self.user.phone_number, "+998901234567")
        self.assertEqual(self.user.user_role, STUDENT)
        self.assertEqual(str(self.user), "Test User")


class UserConfirmationModelTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create(
            username="testuser",
            full_name="Test User",
            phone_number="+998901234567",
            date_of_birth="1990-01-01"
        )
        self.confirmation = UserConfirmation.objects.create(
            user=self.user,
            code="123456",
            auth_status=NEW
        )

    def test_user_confirmation_creation(self):
        self.assertEqual(self.confirmation.user, self.user)
        self.assertEqual(self.confirmation.code, "123456")
        self.assertEqual(self.confirmation.auth_status, NEW)
        self.assertFalse(self.confirmation.is_confirmed)
        self.assertEqual(str(self.confirmation), "Confirmation for +998901234567")

    def test_confirmation_expiration(self):
        self.confirmation.expired_time = timezone.now() - timedelta(minutes=1)
        self.confirmation.save()
        self.assertTrue(self.confirmation.is_expired())