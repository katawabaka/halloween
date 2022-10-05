from PIL import Image, ImageDraw

collage = Image.new("RGBA", (5000, 5000), color=(255, 255, 255, 255))
lst = []
for i in range(100):
    lst.append(str(i+1))
print(len(lst))
c = 0
for i in range(0, 5000, 500):
    for j in range(0, 5000, 500):
        print(c)
        file = "qrs/" + 'MyQRCode' + lst[c] + ".png"
        photo = Image.open(file).convert("RGBA")
        photo = photo.resize((500, 500))
        collage.paste(photo, (i, j))
        c += 1
collage.show()