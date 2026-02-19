from django.test import TestCase
from .difficulty_engine import score_issue_difficulty


class IssueTest(TestCase):
    def test_good_first_issue(self):
        self.assertEqual(score_issue_difficulty({'labels':['good-first-issue']}), 2.0)
