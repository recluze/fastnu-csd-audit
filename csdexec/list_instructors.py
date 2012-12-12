# myproject/myapp/management/commands/my_command.py

from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        t=Template("My name is {myname}.")
        c=Context({"myname":"John"})
        f = open('write_test.txt', 'w')
        f.write(t.render(c))
        f.close
