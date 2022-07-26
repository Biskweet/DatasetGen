for i in range(img.width):
    for j in range(img.height):
            if img.getpixel((i, j))[0] > thr:
                    img.putpixel((i, j), (255, 255, 255))
            else:
                    img.putpixel((i, j), (0, 0, 0))


# ============

import os
for i in range(1,5):
    with open(f"labels/{i}.txt", "r") as f:
            description = [[float(y) for y in x.split(" ")] for x in f.read().split("\n")]
    original = Image.open(f"images/{i}.jpg")
    for elem in description:
            x = int(elem[1] * original.width)
            y = int(elem[2] * original.height)
            w = int(elem[3] * original.width)
            h = int(elem[4] * original.height)
            cropped = original.crop((x - (w//2), y - (h//2), x + (w//2), y + (h//2)))
            cropped.save(f"{int(elem[0])}/{len(os.listdir(str(int(elem[0]))))}.jpg")