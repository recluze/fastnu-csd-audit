from django.core.management.base import BaseCommand, CommandError
from cscm.models import Instructor

class Command(BaseCommand):
    def handle(self, *args, **options):
        # self.stdout.write('Successfully closed poll')
        i = Instructor.objects.all()[0] 
        icon = i.course_set.all()[0]
        self.stdout.write(str(icon.course_name))
        self.stdout.write('\n')
