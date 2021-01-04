from django.test import TestCase
from django.urls import reverse

from model_mommy import mommy

from battles.forms import BattleForm


class BattleCreateFormTests(TestCase):

    def test_create_battle(self):
        current_user = mommy.make('users.User')
        opponent = mommy.make('users.User', email='opponent@test.com')

        data = {
            'opponent': opponent.id
        }

        form = BattleForm(data=data, user=current_user)
        self.assertTrue(form.is_valid())

        battle = form.save()
        self.assertEqual(battle.creator, current_user)
        self.assertEqual(battle.opponent, opponent)

    def test_cannot_create_battle_with_creator_as_opponent(self):
        current_user = mommy.make('users.User')

        data = {
            'opponent': current_user.id
        }

        form = BattleForm(data=data, user=current_user)

        self.assertFalse(form.is_valid())

    def test_cannot_force_a_creator_user(self):
        current_user = mommy.make('users.User')
        fake_creator_user = mommy.make('users.User')
        opponent = mommy.make('users.User')

        data = {
            'creator': fake_creator_user.id,
            'opponent': opponent.id
        }

        form = BattleForm(data=data, user=current_user)
        self.assertTrue(form.is_valid())

        battle = form.save()
        self.assertEqual(battle.creator, current_user)
