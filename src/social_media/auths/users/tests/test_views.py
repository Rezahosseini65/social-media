from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from social_media.auths.users.models import CustomUser


class UserTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('register')
        self.data_user = {
            'email':'test1@gmail.com',
            'password':'test1234',
            'confirm_password':'test1234'
        }

    def test_register_user(self):
        response = self.client.post(self.url, self.data_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access' in response.data['tokens'])
        self.assertTrue('refresh' in response.data['tokens'])
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'test1@gmail.com')

    def test_register_user_password_mismatch(self):
        self.data_user['confirm_password'] = 'wrongPassword'
        response = self.client.post(self.url, self.data_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_register_user_email_exists(self):
        CustomUser.objects.create_user(email='test1@gmail.com', password='test1234')
        response = self.client.post(self.url, self.data_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 1)