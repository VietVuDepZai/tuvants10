
from django.core.management.base import BaseCommand
import json
from backend.models import Subject

class Command(BaseCommand):
    help = 'Import schools from a JSON file'

    def handle(self, *args, **kwargs):
        # Load JSON data from a file with UTF-8 encoding
        schools_data = ["Anh", "Địa", "Toán", "Tin", "Văn", "KHTN", "Sử", "Pháp", "Nhật", "Trung"]

        # Iterate over the JSON objects and create database entries
        for post_data in schools_data:
            try:

                post = Subject.objects.create(
                    name=post_data,
                )
                post.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error saving post: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported schools'))

    def convert_to_number(self, value):
        """Convert a value to a number. Return None if conversion fails."""
        try:
            return float(value) if value else 0
        except ValueError:
            return None

    def convert_to_boolean(self, value):
        """Convert a value to a boolean. Assumes 'true', 'false', 1, 0 as valid inputs."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            value = value.strip().lower()
            if value in ['true', '1']:
                return True
            elif value in ['false', '0']:
                return False
        return False
