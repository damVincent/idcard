from typing import Optional
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
import qrcode

def generate_id_card(first_name: str, middle_name: Optional[str], last_name: str, institution: str, expire_date: datetime, student_id: str, logo_path: str, photo_path: str) -> Image.Image:
    # Creating Image object
    image1 = Image.new('RGB', (500, 700), (255, 255, 255))  # creating a plain image
    font = ImageFont.truetype('arial.ttf', size=20)  # you can use other fonts (calibre for example), but make sure you have it installed on your pc
    write = ImageDraw.Draw(image1)

    # Adding Institution logo
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
    image1.paste(logo_image, (10, 10))

    # Adding Institution name
    color = 'rgb(64,64,64)'
    write.text((120, 45), institution, fill=color, font=ImageFont.truetype('arial.ttf', size=35))

    # Adding Photo
    pic1 = Image.open(photo_path)
    pic1 = pic1.resize((200, 230), Image.ANTIALIAS)
    pic = ImageOps.expand(pic1, border=4, fill='gray')
    image1.paste(pic, (150, 130))

    # Adding Name
    color = 'rgb(0,0,0)'
    full_name = f"{first_name} {middle_name} {last_name}" if middle_name else f"{first_name} {last_name}"
    write.text((50, 400), full_name, fill=color, font=font)

    # Adding ID
    write.text((50, 440), f"ID: {student_id}", fill=color, font=font)

    # Adding Expiration Date
    expire_date_str = expire_date.strftime("%Y-%m-%d")
    write.text((50, 480), f"Expires: {expire_date_str}", fill=color, font=font)

    # Adding QR Code
    qr_string = f"{full_name}\n{expire_date_str}\n{institution}\n{student_id}"
    qrc = qrcode.make(qr_string)  # generating qrcode with details like name, contact number and address
    qrcod = qrc.resize((100, 100), Image.ANTIALIAS)
    image1.paste(qrcod, (380, 610))

    return image1
