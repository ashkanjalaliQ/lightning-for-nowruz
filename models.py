from config import URL, LNBITS_ADMIN_KEY, LNBITS_BASE_URL, LNURL_TITLE, TEMPLATES, LOGO, LOGO_SIZE
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from exceptions import RequestError
import requests, qrcode, os, json
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

class LNurl:
    def __init__(self, name) -> None:
        self.name = name
    
    def get_lnbits_lnurl(self, reward: int) -> str:
        """
        Create a lnurl with the given name and reward.
        """
        data = {
            "title": LNURL_TITLE.format("عزیز" if self.name == "" else self.name),
            "min_withdrawable": reward,
            "max_withdrawable": reward,
            "uses": 1,
            "wait_time": 1,
            "is_unique": True
        }
        response = requests.post(LNBITS_BASE_URL + URL["create_lnurl"]["lnbits"], json=data, headers={"X-Api-Key": LNBITS_ADMIN_KEY})
        try:
            return response.json()["lnurl"]
        except:
            raise RequestError("There is a problem in creating a lnurl.")

    def create_lnurl(self, reward: int) -> str:
        """
        Create a lnurl with the given reward and provider.
        """
        """
        provider is a string that will be used to identify the provider of the lnurl.
        for example: "lnbits" or "lntxbot"
        """
        if reward <= 0:
            raise ValueError("The reward must be greater than 0.")

        return self.get_lnbits_lnurl(reward)


class PostalCard(LNurl):
    def __init__(self, name="", theme="light") -> None:
        super().__init__(name)
        self.name = name
        self.theme = theme
        self.qrcode_image = None
    
    def generate_qrcode(self, lnurl: str) -> None:
        qr = qrcode.QRCode()
        qr.add_data(lnurl)
        self.qrcode_image = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    
    def add_qrcode_to_template(self, qrcode_image):
        template = Image.open(TEMPLATES[self.theme])
        qrcode_image = qrcode_image.resize((1350, 1350))
        qrcode_image = qrcode_image.crop((90, 90, qrcode_image.height-90, qrcode_image.height-90))
        template.paste(qrcode_image, (535, 360))
        return template

    def add_text_into_template(self, text: str, template):
        if os.name == "nt":
            text = arabic_reshaper.reshape(text)
            text = get_display(text)
        
        text_image = Image.new("RGBA", (2000, 2000), (255, 255, 255, 0))
        font = ImageFont.truetype("fonts/Vazirmatn-Bold.ttf", size=100)
        draw = ImageDraw.Draw(text_image)

        if self.theme == "light":
            text_color = (0, 0, 0, 255)
        else:
            text_color = (255, 255, 255, 255)

        draw.text((550, 1750), text, font=font, fill=text_color)
        template.paste(text_image, (0, 0), text_image)
        return template
        
    def add_logo_into_qrcode(self) -> None:
        image = Image.open(LOGO)
        self.qrcode_image = self.qrcode_image.convert("RGB")
        image = image.resize(LOGO_SIZE)
        pos = ((self.qrcode_image.size[0] - image.size[0]) // 2, (self.qrcode_image.size[1] - image.size[1]) // 2)
        self.qrcode_image.paste(image, pos)

    def save_image(self, image_object, file_name: str) -> None:
        image_object.save(f"{file_name}.png")