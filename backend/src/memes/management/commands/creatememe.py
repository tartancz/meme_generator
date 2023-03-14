from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from memes.serializers import ImageSerializer


class Command(BaseCommand):
    help = "Register new meme format to database"

    def add_arguments(self, parser):
        parser.add_argument("fullpath", help="full path to meme", type=Path)
        parser.add_argument("name", help="name of meme", type=str)

    def handle(self, *args, **options):
        full_path: Path = options.pop("fullpath")
        name: str = options.pop("name")
        if not full_path.exists():
            raise CommandError(f"path {full_path} is not valid")
        with full_path.open(mode="rb") as f:
            file = File(f, name=full_path.name)
            data = {"high_res": file, "name": name}
            ser = ImageSerializer(data=data)
            if ser.is_valid():
                ser.save()
                self.stdout.write(self.style.SUCCESS(f"Meme with name {name} was successfully created"))
            else:
                for _, field_errors in ser.errors.items():
                    for error in field_errors:
                        self.stdout.write(self.style.ERROR(error))
