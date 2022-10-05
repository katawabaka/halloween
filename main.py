# Importing library
import qrcode
import json

from PIL import Image

# Data to be encoded
bilety = json.load(open("text.txt"))

for i in list(bilety.keys()):
    '''data = 'https://t.me/file_id_finder_bot?start={}'.format(i)
    img = qrcode.make(data)
    img.save('qrs/MyQRCode{}.png'.format(bilety[i]['bilet']))'''
    Logo_link = 'g4g.jpg'
    logo = Image.open(Logo_link)
    basewidth = 250
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    QRcode.add_data('https://t.me/file_id_finder_bot?start={}'.format(i))
    QRcode.make()
    QRcolor = 'white'
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="black").convert('RGB')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    QRimg.save('qrs/MyQRCode{}.png'.format(bilety[i]['bilet']))

