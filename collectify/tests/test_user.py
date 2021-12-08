import datetime

from django.urls import reverse
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Car, Color, User

# Create your tests here.
class UserTest(APITestCase):

    def assertCreateUser(self, response):
        # Response status code should be 201.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # There should be 1 user in the database.
        self.assertEqual(User.objects.count(), 1)
        # Database user firstname should be "Henry_test".
        self.assertEqual(User.objects.first().firstname, 'Henry_test')
        # Database user lastname should be "Dupont_test".
        self.assertEqual(User.objects.first().lastname, 'Dupont_test')
        # Database user date of birth should be "2010-01-25".
        self.assertEqual(User.objects.first().date_of_birth, datetime.date(1990, 1, 25))

    def setUp(self):
        '''
        Prepare variables needed by every test.
        '''
        # Authenticate.
        self.authUser = AuthUser.objects.create_superuser('test_user', '', 'test_password')
        self.token = Token.objects.create(user=self.authUser)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.required_data = {
            'firstname': 'Henry_test',
            'lastname': 'Dupont_test',
            'date_of_birth': '1990-01-25',
        }

        # Create links.
        self.user_list_endpoint = reverse('user-list')
        self.car_list_endpoint = reverse('car-list')
        self.color_list_endpoint = reverse('color-list')

    # CREATE
    def test_create_user_without_licence_and_without_car(self):
        """
        Create a user without a driver licence and without a car.
        """
        # Create a user.
        data = self.required_data
        data['has_driver_licence'] = False
        response = self.client.post(self.user_list_endpoint, data, format='json')

        self.assertCreateUser(response)
        # Database user should not have a driver licence.
        self.assertEqual(User.objects.first().has_driver_licence, False)
        # Database user should not have a car.
        self.assertEqual(User.objects.first().car_id, None)
        # Database user should not have a color.
        self.assertEqual(User.objects.first().color_id, None)

    def test_create_user_with_licence_and_witouht_car(self):
        """
        Create a user with a driver licence and without a car.
        """
        # Create a user.
        data = self.required_data
        data['has_driver_licence'] = True
        response = self.client.post(self.user_list_endpoint, data, format='json')

        self.assertCreateUser(response)
        # Database user should have a driver licence.
        self.assertEqual(User.objects.first().has_driver_licence, True)
        # Database user should not have a car.
        self.assertEqual(User.objects.first().car_id, None)
        # Database user should not have a color.
        self.assertEqual(User.objects.first().color_id, None)

    def test_create_user_with_licence_and_car_without_color(self):
        """
        Create a user with a driver licence and a car without color.
        """

        # Create a car.
        data = {'name': 'Tesla_test', 'colors': []}
        self.client.post(self.car_list_endpoint, data, format='json')

        # Create a user.
        data = self.required_data
        data['has_driver_licence'] = True
        data['car_id'] = Car.objects.first().id
        response = self.client.post(self.user_list_endpoint, data, format='json')

        self.assertCreateUser(response)
        # Database user should not have a driver licence.
        self.assertEqual(User.objects.first().has_driver_licence, True)
        # Database user should have a car.
        self.assertNotEqual(User.objects.first().car_id, None)
        self.assertEqual(User.objects.first().car_id, Car.objects.first().id)
        # Database user should not have a color
        self.assertEqual(User.objects.first().color_id, None)

    def test_create_user_with_licence_and_car_with_color(self):
        """
        Create a user with a driver licence and a car with a color.
        """
        # Create a color.
        color_data = {'name': 'bleu_test'}
        color_response = self.client.post(self.color_list_endpoint, color_data, format='json')

        # Create a car.
        data = {'name': 'Tesla_test', 'colors': [color_response.data]}
        self.client.post(self.car_list_endpoint, data, format='json')

        # Create a user.
        data = self.required_data
        data['has_driver_licence'] = True
        data['car_id'] = Car.objects.first().id
        data['color_id'] = Color.objects.first().id
        response = self.client.post(self.user_list_endpoint, data, format='json')

        self.assertCreateUser(response)
        # Database user should not have a driver licence.
        self.assertEqual(User.objects.first().has_driver_licence, True)
        # Database user should have a car.
        self.assertNotEqual(User.objects.first().car_id, None)
        self.assertEqual(User.objects.first().car_id, Car.objects.first().id)
        # Database user should have a color
        self.assertNotEqual(User.objects.first().color_id, None)
        self.assertEqual(User.objects.first().color_id, Color.objects.first().id)

    def test_create_user_with_licence_and_car_with_not_related_color(self):
        """
        Create a user with a driver licence and a car
        with a color not related to it.
        """
        # Create a color.
        colors_data = [
            {'name': 'bleu_test'},
            {'name': 'rouge_test'}
        ]
        created_colors = []
        for color_data in colors_data:
            created_colors.append(self.client.post(self.color_list_endpoint, color_data, format='json'))

        # Create a car.
        data = {'name': 'Tesla_test', 'colors': [created_colors[0].data]}
        self.client.post(self.car_list_endpoint, data, format='json')

        # Define color ids
        related_color_id = created_colors[0].data['id']
        not_related_color_id = created_colors[1].data['id']

        # Create a user.
        data = self.required_data
        data['has_driver_licence'] = True
        data['car_id'] = Car.objects.first().id
        data['color_id'] = not_related_color_id
        response = self.client.post(self.user_list_endpoint, data, format='json')

        self.assertCreateUser(response)
        # Database user should not have a driver licence.
        self.assertEqual(User.objects.first().has_driver_licence, True)
        # Database user should have a car.
        self.assertNotEqual(User.objects.first().car_id, None)
        self.assertEqual(User.objects.first().car_id, Car.objects.first().id)
        # Database user should not have a color
        self.assertNotEqual(User.objects.first().color_id, not_related_color_id)
        self.assertNotEqual(User.objects.first().color_id, related_color_id)
        self.assertEqual(User.objects.first().color_id, None)
