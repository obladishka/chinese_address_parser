from parser.models import AddressObject, Province, SpecialWord

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Creates sourcebooks needed."

    def handle(self, *args, **kwargs):
        Province.objects.all().delete()
        SpecialWord.objects.all().delete()
        AddressObject.objects.all().delete()

        call_command("loaddata", "provinces_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Provinces sourcebook creation finished successfully."))

        call_command("loaddata", "special_words_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Special words sourcebook creation finished successfully."))

        call_command("loaddata", "address_objects.json", format="json")
        self.stdout.write(self.style.SUCCESS("Address objects sourcebook creation finished successfully."))
