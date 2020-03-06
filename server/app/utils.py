import string
import random
from PIL import Image, ImageFont, ImageDraw, ImageFilter

def new_verify_code():
    def draw_lines(draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    code = ''.join(random.sample(string.ascii_letters+string.digits, 4))
    width, height = 120, 50
    img = Image.new('RGB',(width, height),'white')
    font = ImageFont.truetype('../res/font/auth.ttf', 40)
    draw = ImageDraw.Draw(img)
    for item in range(4):
        draw.text((5+random.randint(-3,3)+23*item, 5+random.randint(-3,3)),
                  text=code[item], 
                  fill=(random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)),
                  font=font )
    draw_lines(draw, 2, width, height)
    img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
    return img, code