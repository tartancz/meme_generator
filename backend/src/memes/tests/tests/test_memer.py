import io
from pathlib import Path

import pytest
from PIL import Image, ImageDraw
from django.core.files.base import ContentFile

from memes.utils import Memer


def test_check_if_ifs_opened(memer):
    with pytest.raises(ValueError):
        memer._check_if_its_opened()


def test_not_valid_path(memer):
    with pytest.raises(FileNotFoundError):
        memer._create_font("/bad_path/bad.ttf")


def test_memer_enter_and_exit_method(memer):
    with memer:
        assert memer.image is not None
        assert memer.draw is not None
    assert memer.image is None
    assert memer.draw is None


def test_memer_open_and_close_manually(memer):
    # opening image
    memer.open()
    assert memer.image is not None
    assert memer.draw is not None
    # closing image
    memer.close()
    assert memer.image is None
    assert memer.draw is None


def test_calculate_text_center(memer_factory):
    # this test depends on size of image
    memer = memer_factory((500, 400))
    with memer:
        assert memer.calculate_text_center("") == memer.image.width / 2
        text = "Hello, world!"
        _, _, w, _ = memer.draw.textbbox((0, 0), text, font=memer.font)
        assert memer.calculate_text_center("Hello, world!") == (memer.image.width - w) / 2
        # hard coded value
        assert memer.calculate_text_center("Hello, world!") == 161.5


def test_calculate_height(memer_factory):
    memer = memer_factory((500, 400), 10)
    with memer:
        assert memer.calculate_height_of_text("") == 0
        assert memer.calculate_height_of_text("Hello world!") == 10
        assert memer.calculate_height_of_text("Hello \n world!") == 24
        assert memer.calculate_height_of_text("Hello world") == memer.draw.textbbox((0, 0), "Hello world",
                                                                                    font=memer.font)[3]
    memer = memer_factory((500, 400), 32)
    with memer:
        assert memer.calculate_height_of_text("") == 0
        assert memer.calculate_height_of_text("Hello world!") == 30
        assert memer.calculate_height_of_text("Hello \n world!") == 64
        assert memer.calculate_height_of_text("Hello world") == memer.draw.textbbox((0, 0), "Hello world",
                                                                                    font=memer.font)[3]


def test_text_wrap(memer):
    with memer:
        text = "This is a long text that needs to be wrapped."
        wrapped_text = memer.text_wrap(text, max_width=100, spacing=0)
        assert wrapped_text == 'This is \na long \ntext \nthat \nneeds \nto be \nwrapped.'
        wrapped_text = memer.text_wrap(text, max_width=500)
        assert wrapped_text == 'This is a long text that needs to \nbe wrapped.'
        wrapped_text = memer.text_wrap(text, max_width=1000)
        assert wrapped_text == text
        wrapped_text = memer.text_wrap(text, spacing=250)
        assert wrapped_text == 'This \nis \na \nlong \ntext \nthat \nneeds \nto \nbe \nwrapped.'


def test_get_image(memer):
    with memer:
        width = memer.image.width
        height = memer.image.height
        image_io = memer.get_image()
    image = Image.open(ContentFile(image_io, "test.png"))
    image_width = image.width
    image_height = image.height
    image.close()
    assert image.format.lower() == "png"
    assert image_width == width
    assert image_height == height


def test_write_image(memer_factory):
    memer = memer_factory((400, 400), font_size=32, image_color="black")
    with memer:
        memer.generate_meme("Hello world!", "Hello world!")
        assert memer.image.getpixel((200, 10)) == (0, 0, 0)  # non text
        assert memer.image.getpixel((200, 390)) == (0, 0, 0)  # non text
        assert memer.image.getpixel((200, 250)) == (0, 0, 0)  # non text
        assert memer.image.getpixel((120, 20)) == (255, 255, 255)  # text
        assert memer.image.getpixel((120, 380)) == (255, 255, 255)  # text
