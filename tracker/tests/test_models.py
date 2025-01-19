import django

django.setup()

from django.test import TestCase
from django.core.exceptions import ValidationError
from faker import Faker

from tracker.choices import Roles
from tracker.models import CustomUser

fake = Faker()


class TestCustomUserManager(TestCase):
    def setUp(self):
        """Set up test data."""
        self.email = fake.email()
        self.password = fake.password()
        self.role = Roles.CONTRIBUTOR

    def test_create_user(self):
        """Test creating a regular user."""
        user = CustomUser.objects.create_user(
            email=self.email, password=self.password, role=self.role
        )

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertEqual(user.role, self.role)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = CustomUser.objects.create_superuser(
            email=self.email, password=self.password, role=self.role
        )

        self.assertEqual(superuser.email, self.email)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_admin)
        self.assertEqual(superuser.role, self.role)
        self.assertTrue(superuser.check_password(self.password))
        self.assertTrue(superuser.is_staff)

    def test_create_user_with_invalid_email(self):
        """Test creating a user with invalid email format."""
        invalid_email = "invalid.email@format"

        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(
                email=invalid_email, password=self.password, role=self.role
            )


class TestCustomUser(TestCase):
    def setUp(self):
        """Set up test data."""
        self.email = fake.email()
        self.password = fake.password()
        self.is_active = True
        self.is_admin = True
        self.role = Roles.PROJECT_LEAD

    def test_str_method(self):
        """Test the __str__ method of the CustomUser model."""
        user = CustomUser.objects.create_user(
            email=self.email,
            role=self.role,
            password=self.password,
        )

        self.assertEqual(str(user), self.email)

    def test_has_perm(self):
        """Test the has_perm method of the CustomUser model."""
        user = CustomUser.objects.create_user(
            email=self.email,
            role=self.role,
            password=self.password,
        )

        self.assertTrue(CustomUser.has_perm(user))

    def test_has_module_perms(self):
        """Test the has_module_perms method of the CustomUser model."""
        user = CustomUser.objects.create_user(
            email=self.email,
            role=self.role,
            password=self.password,
        )

        self.assertTrue(CustomUser.has_module_perms(user))

    def test_is_staff(self):
        """Test the is_staff property of the CustomUser model."""
        user = CustomUser.objects.create_superuser(
            email=self.email,
            role=self.role,
            password=self.password,
        )

        self.assertTrue(user.is_staff)

    def test_is_project_lead(self):
        """Test the is_project_lead method of the CustomUser model."""
        user = CustomUser.objects.create_user(
            email=self.email,
            role=self.role,
            password=self.password,
        )

        self.assertTrue(user.is_project_lead)
