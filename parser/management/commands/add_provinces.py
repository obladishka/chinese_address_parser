from django.core.management import BaseCommand, call_command

from parser.models import Province


class Command(BaseCommand):
    help = "Creates provinces sourcebook."

    def handle(self, *args, **kwargs):
        Province.objects.all().delete()

        call_command("loaddata", "provinces_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Provinces sourcebook creation finished successfully."))
