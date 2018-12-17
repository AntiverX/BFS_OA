from django.core.management.base import BaseCommand, CommandError
from main_site.models import BFS_OA_Config
from user_info.models import User


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    def handle(self, *args, **options):
        new_config = BFS_OA_Config(
            semester_start_time="2018-08-20"
        )
        admin = User.objects.create_user(
            username="Antiver",
            current_user = "Antiver",
            password="wang@85#2",
            real_name="王帅鹏",
            student_id="3120180863"
        )
        new_config.save()
        admin.save()