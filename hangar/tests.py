from django.test import TestCase, Client
from django.urls import reverse

from hangar.forms import RacketSearchForm
from hangar.models import Racket


class ModelsTestCase(TestCase):
    def test_racket_str(self):
        Racket = Racket.objects.create(
            name="hello",
            speed=900,
            destination="mars"
        )
        self.assertEqual(str(Racket), "hello")


class RacketListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('hangar:Racket-list')
        for i in range(15):
            Racket.objects.create(
                name=f'Racket {i + 1}',
                speed=i,
                destination=f"mars{i}"
            )

    def test_racket_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
