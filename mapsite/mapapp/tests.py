from django.test import TestCase, override_settings
from django.urls import reverse

from . import models


def create_address(full_address, lat=10.0, lon=20.0):
    """
    Creates an address with the given `full_address`.
    """
    return models.Address.objects.create(
        full_address=full_address, lat=lat, lon=lon)


@override_settings(ENABLE_GOOGLE_FUSION=False)
class IndexViewTests(TestCase):
    def test_index_view_with_no_addresses(self):
        """
        If no addresses exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No address are available.")

    def test_index_view_with_a_past_address(self):
        """
        Existing addresses should be displayed on the index page.
        """
        create_address(full_address="Test Str.12")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


@override_settings(ENABLE_GOOGLE_FUSION=False)
class PostAddressViewTests(TestCase):
    def test_post_address_view_with_correct_input(self):
        """
        Create a new address using the POST view.
        """
        payload = {'full_address': 'Test Str. 14', 'lat': 10.01, 'lon': 20.03}
        response = self.client.post(
            reverse('post_address'), payload,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, payload['full_address'])

    def test_post_address_view_with_incorrect_input(self):
        """
        Fail to create a new address using the POST view.
        """
        payload = {'full_address': 'Test Str. 15', 'lat': 'bad', 'lon': 20.03}
        response = self.client.post(
            reverse('post_address'), payload,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)

    def test_post_address_view_with_incorrect_method(self):
        """
        Fail to create a new address using the POST view.
        """
        payload = {'test': 'test'}
        response = self.client.put(
            reverse('post_address'), payload,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 405)
