import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import pre_save
from django.dispatch import receiver

from memes.models import MemeTemplate, Meme


def _resize_image(file, width_image=500, height_image=500, keep_aspect_ratio=True):
    '''
    this will take picture and resize it to wanted resolution with same aspect ratio
    and return object with resized res
    inspiration here: https://stackoverflow.com/questions/71709173/fetch-image-and-crop-before-save-django
    '''
    filename, _ = file.name.split('.')
    image = Image.open(file)
    if keep_aspect_ratio:
        image.thumbnail((width_image, height_image), Image.LANCZOS)
    else:
        image = image.resize((width_image, height_image), Image.LANCZOS)

    output = BytesIO()

    image.save(output, format="png", quality=95)
    resized_image = InMemoryUploadedFile(output, 'ImageField',
                                         f"{filename}.png", 'image/jpeg',
                                         sys.getsizeof(output), None)
    return resized_image


@receiver(pre_save, sender=MemeTemplate)
def change_res_photo_MemeTemplate(sender, instance: MemeTemplate, **kwargs):
    if instance.high_res.width > 500 or instance.high_res.height > 500:
        instance.high_res = _resize_image(instance.high_res.file)
    if not instance.low_res.name:
        instance.low_res = _resize_image(instance.high_res.file, 100, 100, keep_aspect_ratio=False)


@receiver(pre_save, sender=MemeTemplate)
def change_res_photo(sender, instance: MemeTemplate, **kwargs):
    instance.low_res = _resize_image(instance.high_res.file, 100, 100, keep_aspect_ratio=False)