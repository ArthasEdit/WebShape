from django.core.management.base import BaseCommand
from core.models import VocabularyWord
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Update user field for all VocabularyWord records'

    def handle(self, *args, **options):
        # Perform the update
        VocabularyWord.objects.update(user=User.objects.get(username='arthasedit'))

        self.stdout.write(self.style.SUCCESS('Successfully updated user field for all VocabularyWord records.'))