from django.test import TestCase

# Create your tests here.
class smokeTest(TestCase):
    def test_smoke(self):
        self.assertEqual(1, 1)
