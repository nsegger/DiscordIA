from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import sys
import os
import subprocess
import base64
from io import BytesIO


class Generator():
    def __init__(self):
        self.img = Image.open("amoedogen/assets/images/1.jpeg")
        self.font = ImageFont.truetype("amoedogen/assets/fonts/Montserrat-Bold.ttf", 60)
        self.draw = ImageDraw.Draw(self.img)
        self.image_name = str(datetime.now().time()).replace(
            ".", "").replace(":", "")
        self.last_position = None
        self.lines = 0
        self.result = None
        try:
            os.makedirs('outputs')
        except OSError:
            pass

        self.quotes = Image.open("amoedogen/assets/images/quotes.png")
        logo = Image.open("amoedogen/assets/images/logo.png")
        w, h = self.get_img().size
        self.img.paste(logo, (int(w / 2) - 120, h - 170))
        self.credits()

    def get_img_name(self):
        return self.image_name

    def get_img(self):
        return self.img

    def set_font(self, font):
        self.font = font

    def get_font(self):
        return self.font

    def get_draw(self):
        return self.draw

    def get_last_position(self):
        return self.last_position

    def set_last_position(self, pos):
        self.last_position = pos

    def draw_rect(self, text, color):
        print("Drawing rectangle")
        colors = {
            "orange": (243, 111, 33),
            "aqua": (0, 84, 101),
            "blue": (0, 42, 112)
        }
        position = self.get_last_position()
        rect_size = self.get_font().getsize(text)
        bound_1 = (position[0] - 5, position[1] + 20)
        bound_2 = (position[0] + rect_size[0],
                   position[1] + rect_size[1] + 5)
        rect_bg = colors[color]
        rect_size = self.get_font().getsize(text)
        self.get_draw().rectangle((bound_1, bound_2), fill=rect_bg)
        self.lines += 1

    def write(self, text, color="blue", rect=True, base_64=False):
        _, h = self.get_img().size
        if (self.lines > 3):
            return
        if "\n" in text:
            texts = text.split('\n')
            for text in texts:
                if len(text) == 0:
                    break
                self.write(text, color, base_64=base_64)
            return
        print("Writing on image: " + text)
        text = text[0:26]
        if self.get_last_position() == None:
            position = (60, h / 2)
            self.set_last_position(position)
        if rect:
            self.draw_rect(text, color)
        self.draw.text(self.get_last_position(), text,
                       (255, 255, 255), font=self.get_font())
        if (self.lines == 1):
            self.img.paste(self.quotes, (15, int(h / 2) - 25), self.quotes)
        #if not base_64:
        #    self.get_img().save("outputs/" + self.get_img_name() + ".png")
        #else:
            buffered = BytesIO()
            self.get_img().save(buffered, format="JPEG")
            self.result = base64.b64encode(buffered.getvalue())
        new_position = (
            self.get_last_position()[0],
            self.get_last_position()[1] +
            self.get_font().getsize(text)[1] - 10)
        self.set_last_position(new_position)

    def credits(self):
        w, h = self.get_img().size
        original_font = self.get_font()
        self.set_font(ImageFont.truetype(
            "amoedogen/assets/fonts/Montserrat-Bold.ttf", 20))
        self.set_last_position((w - 290, h - 35))
        self.write("margato.github.io/amoedo", rect=False)
        self.set_last_position(None)
        self.set_font(original_font)

    def open(self):
        print("Opening file")
        command = {'linux': 'xdg-open',
                   'win32': 'explorer',
                   'darwin': 'open'}[sys.platform]
        path = "outputs/" + self.get_img_name() + ".png"
        path = os.path.abspath(path)
        subprocess.run([command, path])
