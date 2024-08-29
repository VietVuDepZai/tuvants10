
from django.core.management.base import BaseCommand
import json
from backend.models import District

class Command(BaseCommand):
    help = 'Import schools from a JSON file'

    def handle(self, *args, **kwargs):
        # Load JSON data from a file with UTF-8 encoding
        schools_data = [
                1,
                3,
                4,
                5,
                6,
                7,
                8,
                10,
                11,
                12,
                "Bình Thạnh",
                "Gò Vấp",
                "PN",
                "Tân Bình",
                "Thủ Đức",
                "Bình Chánh",
                "Cần Giờ",
                "Củ Chi",
                "Hốc Môn",
                "Nhà Bè",
                "Tân Phú",
                "Bình Tân"
            ]

        # Iterate over the JSON objects and create database entries
        for post_data in schools_data:
            try:

                post = District.objects.create(
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
