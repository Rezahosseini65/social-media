from django.test import TestCase

from social_media.auths.users.models import CustomUser


class CustomUserTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@gmail.com',
            password='test@1234',
            is_active=True,
            is_staff=False
        )

    def test_user_model(self):
        self.assertEqual(self.user.email, 'test@gmail.com')
        self.assertTrue(self.user.check_password('test@1234'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
