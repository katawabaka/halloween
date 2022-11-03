from PIL import Image, ImageDraw

lst = []
for i in range(200):
    lst.append(str(i+1))
print(len(lst))
c = 0
d = 1
nom = 1
for k in range(5):
    collage = Image.new("RGBA", (2940, 3920), color=(255, 255, 255, 255))
    for i in range(0, 2940, 490):
        for j in range(0, 3920, 560):
            file = "qrs/" + 'MyQRCode' + lst[c] + ".jpg"
            photo = Image.open(file).convert("RGBA")
            photo = photo.resize((490, 560))
            print(c)
            if c <199:
                c += 1
                collage.paste(photo, (i, j))
    collage.save('grids/grid_{}.png'.format(k))
collage.show()