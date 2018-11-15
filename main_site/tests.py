from django.test import TestCase
import os
from .models import FileRecord

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your tests here.
class uploader_test(TestCase):
    def test_upload_1(self):
        FileRecord.objects.create(time="2018-10-10 10:10", title="你好", name="你")

    def test_upload_2(self):
        pass
