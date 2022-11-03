from PIL import Image, ImageDraw, ImageFont


def create_image(size, bgColor, message, font, fontColor):
    W, H = size
    image = Image.new('RGB', size, bgColor)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), message, font=font, fill=fontColor)
    return image


myFont = ImageFont.truetype('shrift.ttf', 64)
myMessage = 'Hello World'
myImage = create_image((430, 100), 'white', myMessage, myFont, 'black')
myImage.save('hello_world.png', "png")
