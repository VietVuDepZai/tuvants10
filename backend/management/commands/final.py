import os
import cloudinary
import cloudinary.uploader
from django.core.management.base import BaseCommand
from backend.models import THPT

# Configure Cloudinary
cloudinary.config(
    cloud_name="dyiesiahu",
    api_key="193699843749843",       # Replace with your Cloudinary API key
    api_secret="lv0RbiRsVz6SWKtHsB5MdJKfFzQ"  # Replace with your Cloudinary API secret
)

class Command(BaseCommand):
    help = 'Upload school logos to Cloudinary and update the database'

    def handle(self, *args, **kwargs):
        # Define the directory where your images are stored
        image_dir = 'static/images/'

        # Get all files in the directory
        for filename in os.listdir(image_dir):
            if filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.jpg'):
                # Remove file extension and special characters to match with school name
                school_name = os.path.splitext(filename)[0]
                school_name = school_name.replace('_', ' ').replace('-', ' ').strip()
                print(school_name)
                try:
                     # Find all schools with the given name
                    schools = THPT.objects.filter(name=f"Trường {school_name}")

                    if schools.exists():
                        for school in schools:
                            print(school.name)
                            # Upload the image to Cloudinary
                            image_path = os.path.join(image_dir, filename)
                            upload_result = cloudinary.uploader.upload(image_path, folder="media/")

                            # Update the 'anh' field with the Cloudinary URL
                            school.anh = upload_result.get('public_id')
                            school.save()
                            self.stdout.write(self.style.SUCCESS(f'Updated logo for {school.name}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'No school found with the name "Trường {school_name}"'))
                except: 
                    print("lệ")
        self.stdout.write(self.style.SUCCESS('Finished uploading and updating school logos'))