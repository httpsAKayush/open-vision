from django.test import TestCase
from .growth_engine import update_skill


class MatchingTest(TestCase):
    def test_skill_capped(self):
        self.assertEqual(update_skill(10, 10), 10)
