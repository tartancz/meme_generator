from pathlib import Path

from PIL import ImageDraw, Image, ImageFont
import io


class Memer:
    def __init__(self, file, font_size: int = 32):
        self.file = file
        self.font = self._create_font(size=font_size)
        self.image = None
        self.draw = None

    def __enter__(self):
        self.image = Image.open(self.file)
        self.draw = ImageDraw.Draw(self.image)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.image.close()
        self.image = None
        self.draw = None

    def _create_font(self, font_path: str | Path | None = None, size: int = 32) -> ImageFont.truetype:
        if font_path is None:
            font_path = Path("memes/fonts/Roboto.ttf")
        if isinstance(font_path, str):
            font_path = Path(font_path)
        if not font_path.is_file():
            raise FileNotFoundError(f"{font_path} do not exist")
        font = ImageFont.truetype(str(font_path), size=size)
        return font

    def calculate_text_center(self, text: str) -> float:
        '''
        calculate starting width of text to be centered
        '''
        _, _, w, _ = self.draw.textbbox((0, 0), text, font=self.font)
        return (self.image.width - w) / 2

    def calculate_height_of_text(self, text: str) -> int:
        _, _, _, h = self.draw.textbbox((0, 0), text, font=self.font)
        return h

    def text_wrap(self, text: str, max_width: int | None, spacing: int = 20) -> str:
        '''
        inspiration: https://tutorials.botsfloor.com/putting-text-on-images-using-python-part-2-cfc173c04874
        get text and it will return formatted text with newlines characters that can fit into image
        '''
        if max_width is None:
            max_width = self.image.width
        max_width -= spacing * 2
        multiline_text = ''
        if self.font.getsize(text)[0] <= max_width:
            return text
        else:
            words = text.split(' ')
            line = ''
            for i, word in enumerate(words):
                if not self.font.getsize(line + words[i])[0] <= max_width:
                    multiline_text += line + "\n"
                    line = ''
                line += word + " "
            multiline_text += line
            print(multiline_text)
        return multiline_text

    def generate_meme(self, bottom_text: str, top_text: str):
        if top_text:
            self.write_centered(top_text, 10)
        if bottom_text:
            y = self.image.height - self.calculate_height_of_text(bottom_text) - 10
            self.write_centered(bottom_text, y)

    def write_centered(self, text: str, y: int):
        text = self.text_wrap(text, self.image.width)
        x = self.calculate_text_center(text)
        self.draw.text((x, y), text, font=self.font, align="center")

    def get_image(self):
        '''
        will return image in array of bytes
        :return:
        '''
        img_io = io.BytesIO()
        self.image.save(img_io, format="PNG")
        return img_io.getvalue()