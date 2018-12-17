from django.test import TestCase
from django.test import Client


class RegiserTestCase(TestCase):
    c = Client()

    def setUp(self):
        data = {
            'username': "Antiver",
            'password': "wang@85#2",
            'real_name': "王帅鹏",
            "student_id": "3120180863"
        }
        register_response = self.c.post('/login', data=data)
        self.assertEqual(200, register_response.status_code)
        login_response = self.c.post("/login", data={'username': "Antiver", 'password': "wang@85#2"})
        print(login_response)
        self.assertEqual(200, login_response.status_code)

    def test_register(self):
        response = self.c.get("/get_current_week")
        print(response.status_code)
