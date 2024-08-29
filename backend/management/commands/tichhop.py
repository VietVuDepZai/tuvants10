from django.core.management.base import BaseCommand
import json
from backend.models import THPT

class Command(BaseCommand):
    help = 'Import or update schools from a JSON file'

    def handle(self, *args, **kwargs):
        # Load JSON data from a file with UTF-8 encoding
        try:
            with open('mergedtichhop.json', 'r', encoding='utf-8') as file:
                schools_data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File best.json not found'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error decoding JSON file'))
            return
        except UnicodeDecodeError:
            self.stdout.write(self.style.ERROR('Error decoding file. Ensure the file is UTF-8 encoded.'))
            return

        # Iterate over the JSON objects and update/create database entries
        for post_data in schools_data:
            try:
                # Convert values to appropriate types
                nv1 = self.convert_to_number(post_data.get('nv1'))
                nv2 = self.convert_to_number(post_data.get('nv2'))
                nv3 = self.convert_to_number(post_data.get('nv3'))
                isChuyen = self.convert_to_boolean(post_data.get('isChuyen'))
                dia_chi = post_data.get('dia_chi')
                quan = post_data.get('quan_huyen')
                ghichu = post_data.get('ghichu')
                monchuyen = post_data.get('monchuyen')

                
                # Update the existing instance or create a new one if it doesn't exist
                post, created = THPT.objects.update_or_create(
                    name=post_data.get('ten_truong'),
                    nv1=nv1,
                    nv2=nv2,
                    nv3=nv3,
                    diachi=dia_chi,
                    quan=quan,
                    ghichu=ghichu,
                    isChuyen=isChuyen,
                    monchuyen=monchuyen
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new school: {post.name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated school: {post.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error saving post: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported/updated schools'))

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
