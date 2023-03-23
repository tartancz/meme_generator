import io

import pytest
from PIL import Image
from django.core.files.base import File

from memes.utils import Memer


@pytest.fixture()
def memer():
    image = Image.new("RGB", (500, 400), color="white")
    img_io = io.BytesIO()
    image.save(img_io, format="png")
    file = File(img_io, "test.png")
    return Memer(file)


@pytest.fixture()
def memer_factory():
    def wrapped_func(size: tuple[int, int], font_size=32, image_color="white"):
        image = Image.new("RGB", size, color=image_color)
        img_io = io.BytesIO()
        image.save(img_io, format="png")
        file = File(img_io, "test.png")
        return Memer(file, font_size)
    return wrapped_func