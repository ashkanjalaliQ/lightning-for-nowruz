import argparse
from models import PostalCard
from config import IMAGE_TEXT, REWARD


arg_parser = argparse.ArgumentParser(description="Generate a postal card")
arg_parser.add_argument("-n", "--name", help="name of the person", default="")
arg_parser.add_argument("-t", "--theme", help="theme of the card, dark or light", default="light")
args = arg_parser.parse_args()

postal_card = PostalCard(name=args.name, theme=args.theme)
lnurl = postal_card.create_lnurl(reward=REWARD)
postal_card.generate_qrcode(lnurl=lnurl)
postal_card.add_logo_into_qrcode()
template = postal_card.add_qrcode_to_template(qrcode_image=postal_card.qrcode_image)
postal_card.add_text_into_template(text=IMAGE_TEXT.format(args.name), template=template)
postal_card.save_image(image_object=template, file_name="postalcard")
print("postal card is generated successfully!")



