from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Deletes a specified superuser."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="the email related to the superuser you want deleted.")

    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f"Successfully deleted user."))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"user does not exist."))