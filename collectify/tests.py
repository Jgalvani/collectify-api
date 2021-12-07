from django.urls import reverse
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
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

    # CREATE
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

        self.assertEqual(car_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get().name, 'Tesla_test')
        self.assertEqual(Car.objects.get().colors.count(), 3)
        for created_color, car_color in zip(created_colors, Car.objects.get().colors.all()):
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
        car_id = create_response.data['id']
        car_detail_endpoint = reverse('car-detail', args=[car_id])
        retrieve_response = self.client.get(car_detail_endpoint, format='json')

        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(retrieve_response.data, dict)
        self.assertEqual(retrieve_response.data['name'], data['name'])
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
        car_id = create_response.data['id']
        car_detail_endpoint = reverse('car-detail', args=[car_id])
        retrieve_response = self.client.get(car_detail_endpoint, format='json')

        # Preparing to compare the color created and the color of the car.
        car_color_name = retrieve_response.data['colors'][0]['name']
        created_color_name = color_data['name']

        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(retrieve_response.data, dict)
        self.assertEqual(retrieve_response.data['name'], data['name'])
        self.assertEqual(car_color_name, created_color_name)

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
        car_id = create_response.data['id']
        car_detail_endpoint = reverse('car-detail', args=[car_id])
        retrieve_response = self.client.get(car_detail_endpoint, format='json')

        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(retrieve_response.data, dict)
        self.assertEqual(retrieve_response.data['name'], data['name'])
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

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(list_response.data, list)
        self.assertEqual(len(list_response.data), 3)
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

        # Retrieve the car.
        car_id = create_response.data['id']
        car_detail_endpoint = reverse('car-detail', args=[car_id])
        retrieve_response = self.client.get(car_detail_endpoint, format='json')

        # Change the name of the car.
        retrieve_response.data['name'] = 'BMW_test'
        update_response = self.client.put(car_detail_endpoint, retrieve_response.data, format='json')

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(update_response.data, dict)
        self.assertEqual(update_response.data['name'], retrieve_response.data['name'])
        self.assertNotEqual(update_response.data['name'], data['name'])
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

        # Retrieve the car.
        car_id = create_response.data['id']
        car_detail_endpoint = reverse('car-detail', args=[car_id])
        retrieve_response = self.client.get(car_detail_endpoint, format='json')

        # Delete the colors of the car.
        retrieve_colors = retrieve_response.data['colors']
        retrieve_response.data['colors'] = []
        delete_colors_response = self.client.put(car_detail_endpoint, retrieve_response.data, format='json')

        self.assertEqual(delete_colors_response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(delete_colors_response.data, dict)
        self.assertEqual(delete_colors_response.data['name'], retrieve_response.data['name'])
        self.assertEqual(delete_colors_response.data['name'], data['name'])
        self.assertEqual(delete_colors_response.data['colors'], [])
        self.assertNotEqual(delete_colors_response.data['colors'], retrieve_colors)

        # Add new colors to the car.
        delete_colors_response.data['colors'] = created_colors[1:3]
        add_colors_response = self.client.put(car_detail_endpoint, delete_colors_response.data, format='json')

        self.assertEqual(add_colors_response.data['colors'], created_colors[1:3])
        self.assertNotEqual(add_colors_response.data['colors'], [])

    # DELETE
    def test_delete_car(self):
        # Create a car.
        data = {'name': 'Tesla_test', 'colors': []}
        create_response = self.client.post(self.car_list_endpoint, data, format='json')

        self.assertEqual(Car.objects.count(), 1)

        # Delete a car.
        car_id = Car.objects.get().id
        car_detail_endpoint = reverse('car-detail', args=[car_id])
        delete_response = self.client.delete(car_detail_endpoint, format='json')

        self.assertEqual(Car.objects.count(), 0)
