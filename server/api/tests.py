from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class VeroCsvFileProcessTest(APITestCase):
    def test_process_csv(self):
        """
        Test if we can process our csv file
        """
        url = reverse('convert')
        f = open("../README.md", 'rb')
        response = self.client.put(url, data={'file':f}, format='multipart')
        f.close()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
