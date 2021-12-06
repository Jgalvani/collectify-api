from django.urls import reverse
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase, APITestCase, RequestsClient
from rest_framework import status

from .models import Car, Color, User

# Create your tests here.
class CarTest(APITestCase):

    def setUp(self):
        '''
        Prepare variables needed by every test.
        '''
        self.user = AuthUser.objects.create_superuser('test_user', '', 'test_password')
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.car_list_endpoint = reverse('car-list')
        self.color_list_endpoint = reverse('color-list')

    def test_create_car_without_color(self):
        """
        Create a car without color.
        """
        # Create a car.
        data = {'name': 'Tesla_test', 'colors': []}
        response = self.client.post(self.car_list_endpoint, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get().name, 'Tesla_test')
        self.assertEqual(Car.objects.get().colors.count(), 0)
        self.assertEqual(list(Car.objects.get().colors.all()), [])


    def test_create_car_with_one_color(self):
        """
        Create a car with one color.
        """
        # Create a color.
        color_data = {'name': 'bleu_test'}
        color_response = self.client.post(self.color_list_endpoint, color_data, format='json')

        # Create a car.
        car_data = {'name': 'Tesla_test', 'colors': [color_response.data]}
        car_response = self.client.post(self.car_list_endpoint, car_data, format='json')

        # Preparing to compare the color created and the color of the car.
        car_color_name = Car.objects.get().colors.get().name
        created_color_name = color_data['name']

        self.assertEqual(car_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get().name, 'Tesla_test')
        self.assertEqual(Car.objects.get().colors.count(), 1)
        self.assertEqual(car_color_name, created_color_name)

    def test_create_car_with_colors(self):
        """
        Create a car with multiple colors.
        """

        # Create multiple colors.
        colors_data = [
            {'name': 'bleu_test'},
            {'name': 'vert_test'},
            {'name': 'rouge_test'}
        ]
        created_colors = []
        for color_data in colors_data:
            created_colors.append(self.client.post(self.color_list_endpoint, color_data, format='json').data)

        # Create a car.
        car_data = {'name': 'Tesla_test', 'colors': created_colors}
        car_response = self.client.post(self.car_list_endpoint, car_data, format='json')

        # Preparing to compare the colors created and the colors of the car.
        car_colors_names = [color.name for color in Car.objects.get().colors.all()]
        created_colors_names = [color['name'] for color in created_colors]

        self.assertEqual(car_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get().name, 'Tesla_test')
        self.assertEqual(Car.objects.get().colors.count(), 3)
        self.assertEqual(car_colors_names, created_colors_names)
