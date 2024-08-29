import os
from django.core.management.base import BaseCommand
from backend.models import THPT
from docx import Document
from docx.shared import Inches

class Command(BaseCommand):
    help = 'Update school logos from a Word document'

    def handle(self, *args, **kwargs):
        # Load Word document
        docx_path = 'ts101.docx'
        image_dir = 'static/images/'  # Directory to save extracted images
        os.makedirs(image_dir, exist_ok=True)

        try:
            doc = Document(docx_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading Word document: {e}'))
            return

        # Extract data from the table
        table = doc.tables[0]
        for index, row in enumerate(table.rows):
            school_name = row.cells[0].text.strip()

            # Extract image from the second cell if it exists
            cell = row.cells[1]._element
            blips = cell.findall('.//a:blip', namespaces={'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
            if blips:
                for blip in blips:
                    rId = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                    image_part = doc.part.related_parts[rId]
                    image_extension = image_part.content_type.split('/')[-1]
                    image_name = f"{school_name.replace(' ', '_')}.{image_extension}"
                    image_path = os.path.join(image_dir, image_name)
                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_part.blob)
                    break
            else:
                self.stdout.write(self.style.WARNING(f'No image found for {school_name}'))
                continue

            try:
                # Find the corresponding THPT instance
                school = THPT.objects.get(name=f"Trường {school_name}")
                if school:
                    # Update the 'anh' field
                    with open(image_path, 'rb') as f:
                        school.anh.save(os.path.basename(image_path), f)
                    school.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated logo for {school.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'No matching school found for {school_name}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing row {index}: {e}'))

        self.stdout.write(self.style.SUCCESS('Finished updating school logos'))
