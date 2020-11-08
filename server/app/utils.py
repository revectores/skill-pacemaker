import string
import random
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from flask_mail import Message
from app import mail
import re
from functools import reduce


def new_verify_code():
    def draw_lines(draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    width, height = 120, 50
    img = Image.new('RGB', (width, height), 'white')
    font = ImageFont.truetype('./app/static/font/auth.ttf', 40)
    # font = ImageFont.load_default()
    draw = ImageDraw.Draw(img)
    for item in range(4):
        draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                  text=code[item],
                  fill=(random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)),
                  font=font)
    draw_lines(draw, 2, width, height)
    img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
    return img, code


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def is_valid_email(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False


def test_recommend(node):
    return node + 1
    

def get_nodes_coordinates(ids, links):
    depth = {id_: 0 for id_ in ids}
    seq = {id_: 0 for id_ in ids}

    for _ in range(len(ids)):
        for link in links:
            if depth[link[1]] < depth[link[0]] + 1:
                depth[link[1]] = depth[link[0]] + 1

    depth_cur = {}
    for id_ in ids:
        if depth[id_] not in depth_cur:
            depth_cur[depth[id_]] = 0

        seq[id_] = depth_cur[depth[id_]]
        depth_cur[depth[id_]] += 1

    nodes_coordinates = {id_: (seq[id_], depth[id_]) for id_ in depth.keys()}
    return nodes_coordinates
