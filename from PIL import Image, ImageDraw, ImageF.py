from PIL import Image, ImageDraw, ImageFilter
import os

W = H = 1080
bg = (7, 20, 44)
white = (248, 248, 248, 255)
blue = (26, 173, 235, 255)

img = Image.new('RGBA', (W, H), bg + (255,))
d = ImageDraw.Draw(img)
cx = cy = W // 2

layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(layer)
ld.ellipse((130, 130, 950, 950), outline=(255, 255, 255, 20), width=2)
layer = layer.filter(ImageFilter.GaussianBlur(25))
img = Image.alpha_composite(img, layer)
d = ImageDraw.Draw(img)

r = 300
th = 14
for start, end in [(132, 176), (4, 86), (94, 126), (184, 266), (274, 356)]:
    d.arc((cx-r, cy-r, cx+r, cy+r), start=start, end=end, fill=white, width=th)

points = [
    [(540, 70), (520, 170), (560, 170)],
    [(1010, 540), (910, 520), (910, 560)],
    [(540, 1010), (520, 910), (560, 910)],
    [(70, 540), (170, 520), (170, 560)],
]
for p in points:
    d.polygon(p, fill=white)

left = [(340, 720), (340, 340), (442, 340), (542, 440), (542, 520), (442, 420), (442, 720)]
right = [(740, 720), (740, 340), (638, 340), (538, 440), (538, 520), (638, 420), (638, 720)]
d.polygon(left, fill=white)
d.polygon(right, fill=white)

cut1 = [(440, 720), (440, 470), (490, 420), (490, 720)]
cut2 = [(642, 720), (642, 470), (592, 420), (592, 720)]
d.polygon(cut1, fill=bg)
d.polygon(cut2, fill=bg)

needle = [(360, 790), (815, 335), (785, 305), (330, 760)]
d.polygon(needle, fill=blue)

hub_r = 30
d.ellipse((cx-hub_r, cy-hub_r, cx+hub_r, cy+hub_r), fill=bg, outline=blue, width=10)

os.makedirs('output', exist_ok=True)
img.save('output/logo_recreation_code.png')