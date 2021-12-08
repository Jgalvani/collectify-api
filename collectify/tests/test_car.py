from django.urls import reverse
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Car, Color


class CarTest(APITestCase):

    def setUp(self):
        '''
        Prepare variables needed by every test.
        '''
        # Authenticate.
        self.user = AuthUser.objects.create_superuser('test_user', '', 'test_password')
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Create links.
        self.car_list_endpoint = reverse('car-list')
        self.color_list_endpoint = reverse('color-list')

    # CREATE
    def test_create_car_without_color(self):
        """
        Create a car without color.
        """
        # Create a car.
        data = {'name': 'Tesla_test', 'colors': []}
        response = self.client.post(self.car_list_endpoint, data, format='json')

        # Response status code should be 201.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # There should be 1 car in the database.
        self.assertEqual(Car.objects.count(), 1)
        # Car from database should be "Tesla_test".
        self.assertEqual(Car.objects.first().name, 'Tesla_test')
        # Car should not have any color in the database.
        self.assertEqual(Car.objects.first().colors.count(), 0)
        # Attribute colors from car should be an empty list.
        self.assertEqual(list(Car.objects.first().colors.all()), [])


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

        # Response status code should be 201.
        self.assertEqual(car_response.status_code, status.HTTP_201_CREATED)
        # There should be 1 car in the database.
        self.assertEqual(Car.objects.count(), 1)
        # Car from database should be "Tesla_test".
        self.assertEqual(Car.objects.first().name, 'Tesla_test')
        # Car should have 1 color in the database.
        self.assertEqual(Car.objects.first().colors.count(), 1)
        # Color from car should be bleu_test.
        self.assertEqual(Car.objects.first().colors.first().name, 'bleu_test')

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

        # Response status code should be 201.
        self.assertEqual(car_response.status_code, status.HTTP_201_CREATED)
        # There should be 1 car in the database.
        self.assertEqual(Car.objects.count(), 1)
        # Car from database should be "Tesla_test".
        self.assertEqual(Car.objects.first().name, 'Tesla_test')
        # Car should have 3 colors in the database.
        self.assertEqual(Car.objects.first().colors.count(), 3)
        # Colors from car should be the same as created colors.
        for created_color, car_color in zip(created_colors, Car.objects.first().colors.all()):
            self.assertEqual(created_color['name'], car_color.name)

    # RETRIEVE
    def test_retrieve_car_without_color(self):
        """
        Retrieve a car without color.
        """
        # Create a car.
        data = {'name': 'Tesla_test', 'colors': []}
        create_response = self.client.post(self.car_list_endpoint, data, format='json')

        # Retrieve the car.
        car_detail_endpoint = reverse('car-detail', args=[create_response.data['id']])
        retrieve_response = self.client.get(car_detail_endpoint, format='json')

        # Response status code should be 200.
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        # Response data should be a dictionnary.
        self.assertIsInstance(retrieve_response.data, dict)
        # Car from response should be "Tesla_test".
        self.assertEqual(retrieve_response.data['name'], 'Tesla_test')
        # Attribute colors from car should be an empty list.
        self.assertEqual(retrieve_response.data['colors'], [])

    def test_retrieve_car_with_one_color(self):
        """
        Retrieve a car with one color.
        """
        # Create a color.
        color_data = {'name': 'bleu_test'}
        color_response = self.client.post(self.color_list_endpoint, color_data, format='json')

        # Create a car.
        data = {'name': 'Tesla_test', 'colors': [color_data]}
        create_response = self.client.post(self.car_list_endpoint, data, format='json')

        # Retrieve the car.
        car_detail_endpoint = reverse('car-detail', args=[create_response.data['id']])
        retrieve_response = self.client.get(car_detail_endpoint, format='json')

        # Response status code should be 200.
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        # Response data should be a dictionnary.
        self.assertIsInstance(retrieve_response.data, dict)
        # Car from response should be "Tesla_test".
        self.assertEqual(retrieve_response.data['name'], 'Tesla_test')
        # Color from car should be bleu_test.
        self.assertEqual(retrieve_response.data['colors'][0]['name'], 'bleu_test')

    def test_retrieve_car_with_colors(self):
        """
        Retrieve a car with multiple colors.
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
        data = {'name': 'Tesla_test', 'colors': colors_data}
        create_response = self.client.post(self.car_list_endpoint, data, format='json')

        # Retrieve the car.
        car_detail_endpoint = reverse('car-detail', args=[create_response.data['id']])
        retrieve_response = self.client.get(car_detail_endpoint, format='json')

        # Response status code should be 200.
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        # Response data should be a dictionnary.
        self.assertIsInstance(retrieve_response.data, dict)
        # Car from response should be "Tesla_test".
        self.assertEqual(retrieve_response.data['name'], 'Tesla_test')
        # Colors from car should be the same as created colors.
        for created_color, car_color in zip(created_colors, retrieve_response.data['colors']):
            self.assertEqual(created_color, car_color)

    # LIST
    def test_list_cars(self):
        """
        List cars.
        """
        # Create colors.
        colors_data = [
            {'name': 'bleu_test'},
            {'name': 'vert_test'},
            {'name': 'rouge_test'}
        ]
        created_colors = []
        for color_data in colors_data:
            created_colors.append(self.client.post(self.color_list_endpoint, color_data, format='json').data)

        # Create cars.
        cars_data = [
            {'name': 'Tesla_test', 'colors': []},
            {'name': 'BMW_test', 'colors': [created_colors[0]]},
            {'name': 'Mercedes_test', 'colors': created_colors}
        ]
        created_cars = []
        for car_data in cars_data:
            created_cars.append(self.client.post(self.car_list_endpoint, car_data, format='json').data)

        # List cars.
        list_response = self.client.get(self.car_list_endpoint, format='json')

        # Response status code should be 200.
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        # Response data should be a list.
        self.assertIsInstance(list_response.data, list)
        # There should be 3 cars in response.
        self.assertEqual(len(list_response.data), 3)
        # Cars from response should be the same as created cars.
        for created_car, car in zip(created_cars, list_response.data):
            self.assertEqual(created_car['name'], car['name'])
            self.assertEqual(created_car['colors'], car['colors'])


    # UPDATE
    def test_update_car_name(self):
        """
        Update a car name.
        """
        colors_data = [
            {'name': 'bleu_test'},
            {'name': 'vert_test'},
            {'name': 'rouge_test'}
        ]
        created_colors = []
        for color_data in colors_data:
            created_colors.append(self.client.post(self.color_list_endpoint, color_data, format='json').data)

        # Create a car.
        data = {'name': 'Tesla_test', 'colors': colors_data}
        create_response = self.client.post(self.car_list_endpoint, data, format='json')

        # Change the name of the car.
        updated_car = create_response.data
        updated_car['name'] = 'BMW_test'
        car_detail_endpoint = reverse('car-detail', args=[updated_car['id']])
        update_response = self.client.put(car_detail_endpoint, updated_car, format='json')

        # Response status code should be 200.
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        # Response data should be a dictionnary.
        self.assertIsInstance(update_response.data, dict)
        # Car from update response should be "BMW_test".
        self.assertEqual(update_response.data['name'], 'BMW_test')
        # Car from update response should not be "Tesla_test".
        self.assertNotEqual(update_response.data['name'], 'Tesla_test')
        # Colors from update response should be the same as created colors.
        self.assertEqual(update_response.data['colors'], created_colors)

    def test_update_car_colors(self):
        """
        Update car colors.
        """
        # Create colors.
        colors_data = [
            {'name': 'bleu_test'},
            {'name': 'vert_test'},
            {'name': 'rouge_test'}
        ]
        created_colors = []
        for color_data in colors_data:
            created_colors.append(self.client.post(self.color_list_endpoint, color_data, format='json').data)

        # Create a car.
        data = {'name': 'Tesla_test', 'colors': colors_data}
        create_response = self.client.post(self.car_list_endpoint, data, format='json')

        # Delete the colors of the car.
        updated_car = create_response.data
        updated_car['colors'] = []
        car_detail_endpoint = reverse('car-detail', args=[updated_car['id']])
        delete_colors_response = self.client.put(car_detail_endpoint, updated_car, format='json')

        # Response status code should be 200.
        self.assertEqual(delete_colors_response.status_code, status.HTTP_200_OK)
        # Response data should be a dictionnary.
        self.assertIsInstance(delete_colors_response.data, dict)
        # Car from update response should be "Tesla_test".
        self.assertEqual(delete_colors_response.data['name'], 'Tesla_test')
        # Colors from car should not be the same as created colors.
        self.assertNotEqual(delete_colors_response.data['colors'], created_colors)
        # The attribute colors from car should be an empty list.
        self.assertEqual(delete_colors_response.data['colors'], [])

        # Add new colors to the car.
        partial_created_colors = created_colors[1:3]
        delete_colors_response.data['colors'] = partial_created_colors
        car_detail_endpoint = reverse('car-detail', args=[delete_colors_response.data['id']])
        add_colors_response = self.client.put(car_detail_endpoint, delete_colors_response.data, format='json')

        # Colors from car should be the same as partial created colors.
        self.assertEqual(add_colors_response.data['colors'], partial_created_colors)
        # The attribute colors from car should not be an empty list.
        self.assertNotEqual(add_colors_response.data['colors'], [])

    # DELETE
    def test_delete_car(self):
        # Create a car.
        data = {'name': 'Tesla_test', 'colors': []}
        create_response = self.client.post(self.car_list_endpoint, data, format='json')

        # There should be 1 car in the database.
        self.assertEqual(Car.objects.count(), 1)

        # Delete a car.
        car_detail_endpoint = reverse('car-detail', args=[Car.objects.first().id])
        delete_response = self.client.delete(car_detail_endpoint, format='json')

        # There should not be any car in the database.
        self.assertEqual(Car.objects.count(), 0)
