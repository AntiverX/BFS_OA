from django.test import TestCase
from django.test import Client


class RegiserTestCase(TestCase):
    c = Client()

    def setUp(self):
        pass

    def test_register(self):
        data = {
            'username': "Antiver",
            'password': "wang@85#2",
            'real_name': "王帅鹏",
            "student_id": "3120180863"
        }
        response = self.c.post("/register", data=data)
        print(response.status_code)
