from django.test import Client, TestCase


class WebpageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_webpage(self):
        self.client.get('/datamodel/')
