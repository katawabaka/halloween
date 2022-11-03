# Importing library
import qrcode
import json

from PIL import Image


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    """
    Функция для обрезки изображения по центру.
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

# Data to be encoded
bilety = json.load(open("text.txt"))

for i in list(bilety.keys()):
    '''data = 'https://t.me/spookyshot_bot?start={}'.format(i)
    img = qrcode.make(data)
    img.save('qrs/MyQRCode{}.png'.format(bilety[i]['bilet']))'''
    Logo_link = 'g4g.png'
    logo = Image.open(Logo_link)
    basewidth = 150
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    QRcode.add_data('https://t.me/spookyshot_bot?start={}'.format(i))
    QRcode.make()
    QRcolor = 'black'
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    QRimg.save('qrs/MyQRCode{}.jpg'.format(bilety[i]['bilet']))
    QRimg = crop_center(QRimg, 490, 490)
    from PIL import Image, ImageDraw, ImageFont


    def create_image(size, bgColor, message, font, fontColor):
        W, H = size
        image = Image.new('RGB', size, bgColor)
        draw = ImageDraw.Draw(image)
        _, _, w, h = draw.textbbox((0, 0), message, font=font)
        draw.text(((W - w) / 2, (H - h) / 2-20), message, font=font, fill=fontColor)
        return image


    myFont = ImageFont.truetype('shrift.ttf', 90)
    myMessage = '{}'.format(bilety[i]['bilet'])
    myImage = create_image((490, 70), 'white', myMessage, myFont, 'black')
    myImage.save('hello_world.jpg', "JPEG")

    new_image = Image.new('RGB', (QRimg.size[0], QRimg.size[1]+70), (250, 250, 250))

    # вставляем наши изображения

    new_image.paste(QRimg, (0, 0))
    new_image.paste(myImage, (0, QRimg.size[1]))

    # сохраняем новое объединенное изображение в нужном формате

    new_image.save('qrs/MyQRCode{}.jpg'.format(bilety[i]['bilet']), "JPEG")
