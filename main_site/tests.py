from django.test import TestCase
from django.test import Client
from .models import BFS_OA_Config


class RegiserTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        data = {
            'username': "Antiver",
            'password': "wang@85#2",
            'real_name': "王帅鹏",
            "student_id": "3120180863"
        }
        register_response = self.c.post('/register', data=data)

        self.assertEqual(200, register_response.status_code)
        login_response = self.c.post("/login", data={'username': "Antiver", 'password': "wang@85#2"}, follow=True)
        self.assertEqual(200, login_response.status_code)
        BFS_OA_Config.objects.create(semester_start_time="2018-08-20")

    def test_get_current_week(self):
        get_current_week_response = self.c.get("/get_current_week")
        self.assertEqual(200, get_current_week_response.status_code)
