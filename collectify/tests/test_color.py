from django.urls import reverse
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Color

class ColorTest(APITestCase):

    def setUp(self):
        '''
        Prepare variables needed by every test.
        '''
        # Authenticate.
        self.authUser = AuthUser.objects.create_superuser('test_user', '', 'test_password')
        self.token = Token.objects.create(user=self.authUser)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create color link.
        self.color_list_endpoint = reverse('color-list')

    # CREATE
    def test_create_color(self):
        """
        Create a color.
        """
        # Create a color.
        data = {'name': 'bleu_test'}
        response = self.client.post(self.color_list_endpoint, data, format='json')

        # Response status code should be 201.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # There should be 1 color in the database.
        self.assertEqual(Color.objects.count(), 1)
        # Color name from database should be "bleu_test".
        self.assertEqual(Color.objects.first().name, 'bleu_test')

    # RETRIEVE
    def test_retrieve_color(self):
        """
        Retrieve a color.
        """
        # Create a color.
        data = {'name': 'bleu_test'}
        create_response = self.client.post(self.color_list_endpoint, data, format='json')

        # Retrieve the color.
        color_detail_endpoint = reverse('color-detail', args=[create_response.data['id']])
        retrieve_response = self.client.get(color_detail_endpoint, format='json')

        # Response status code should be 200.
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        # Response data should be a dictionnary.
        self.assertIsInstance(retrieve_response.data, dict)
        # Color name from response should be "bleu_test".
        self.assertEqual(retrieve_response.data['name'], 'bleu_test')

    # LIST
    def test_list_colors(self):
        """
        List colors.
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

        # List colors.
        list_response = self.client.get(self.color_list_endpoint, format='json')

        # Response status code should be 200.
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        # Response data should be a list.
        self.assertIsInstance(list_response.data, list)
        # There should be 3 colors in response.
        self.assertEqual(len(list_response.data), 3)
        # Colors from response should be the same as created colors.
        self.assertEqual(created_colors, list_response.data)

    # UPDATE
    def test_update_color(self):
        """
        Update a color.
        """
        # Create a color.
        data = {'name': 'bleu_test'}
        create_response = self.client.post(self.color_list_endpoint, data, format='json')

        # Change the name of the color.
        updated_color = create_response.data
        updated_color['name'] = 'rouge_test'
        color_detail_endpoint = reverse('color-detail', args=[updated_color['id']])
        update_response = self.client.put(color_detail_endpoint, updated_color, format='json')

        # Response status code should be 200.
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        # Response data should be a dictionnary.
        self.assertIsInstance(update_response.data, dict)
        # Color name from response should not be "bleu_test".
        self.assertNotEqual(update_response.data['name'], "bleu_test")
        # Color name from response should be "rouge_test".
        self.assertEqual(update_response.data['name'], 'rouge_test')

    # DELETE
    def test_delete_color(self):
        # Create a color.
        data = {'name': 'bleu_test'}
        create_response = self.client.post(self.color_list_endpoint, data, format='json')

        # There should be 1 color in the database.
        self.assertEqual(Color.objects.count(), 1)

        # Delete a color.
        color_detail_endpoint = reverse('color-detail', args=[Color.objects.first().id])
        delete_response = self.client.delete(color_detail_endpoint, format='json')

        # There should not be any color in the database.
        self.assertEqual(Color.objects.count(), 0)

