from django.test import TestCase, Client
from django.urls import reverse

from model_mommy import mommy


class BattleListViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_performance(self):
        mommy.make('battles.Battle')
        mommy.make('battles.Battle')

        url = reverse('battles:battle_list')

        with self.assertNumQueries(1):
            response = self.client.get(url)

        self.assertEqual(response.context['object_list'].count(), 2)

        mommy.make('battles.Battle')
        mommy.make('battles.Battle')

        with self.assertNumQueries(1):
            response = self.client.get(url)

        self.assertEqual(response.context['object_list'].count(), 4)

    def test_battle_list(self):
        battle1 = mommy.make('battles.Battle')
        battle2 = mommy.make('battles.Battle')

        url = reverse('battles:battle_list')
        response = self.client.get(url)

        self.assertContains(response, battle1.id, status_code=200)
        self.assertContains(response, battle2.id, status_code=200)


class BattleDetailViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_battle_detail(self):
        battle = mommy.make('battles.Battle')

        url = reverse('battles:battle_detail', args=[battle.id])
        response = self.client.get(url)

        self.assertContains(response, battle.id, status_code=200)


class BattleCreateViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_battle_create(self):
        mommy.make('users.User')
        data = {
            'creator': 'creator@test.com',
            'opponent': 'opponent@test.com'
        }
        url = reverse('battles:battle_create')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
