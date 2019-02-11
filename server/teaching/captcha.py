# encoding:utf-8
from PIL import Image, ImageDraw, ImageFont
import random
from io import StringIO, BytesIO, FileIO
from math import ceil
import base64
import hashlib

class Captcha(object):

    def __init__(self, request, * args, **kwargs):
        self.count = 4

        # 宽高
        self.width = 150
        self.height = 30

        #取值范围
        self.words = list('abcdefhkmnpuvwxyABCDEFGHKLMNPQRTUVWXY346789')

        # 生成验证码
        self.code = self._set_code()

        #session
        request.session[request.session.session_key] = "".join(self.code)
        self.request = request
        self.key = self.request.session.session_key

    def set_font_size(self):
        """
            将图片高度的80%作为字体大小
        """
        return int(self.height * 0.9)

    def _set_code(self):
        length, code = len(self.words), []
        for i in range(0, 4):
            code.append(self.words[random.randrange(0, length)])

        return code

    def display(self):
        """
            把生成的验证码图片改成数据流返回
        """

        # 字体颜色
        self.font_color = ['black', 'darkblue', 'darkred']

        # 背景颜色，随机生成
        self.background = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))

        #　使用 PIL 创建画布
        im = Image.new('RGB', (self.width, self.height), self.background)

        # 设置字体大小
        self.font_size = self.set_font_size()

        # 实例化一个绘图
        draw = ImageDraw.Draw(im)

        # 在画布绘图,写验证码

        for i in range(random.randrange(0, 4)):
            line_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            xy = (
                random.randrange(0, int(self.width * 0.2)),
                random.randrange(0, self.height),
                random.randrange(int(3 * self.width / 4), self.width),
                random.randrange(0, self.height)
            )
            draw.line(xy, fill=line_color, width=3)
        j = int(self.font_size * 0.4)
        k = int(self.font_size * 0.6)
        x = random.randrange(j, k)  # starts point
        for word in self.code:
            y = random.randrange(1, 3)
            self.font = ImageFont.truetype('arial.ttf', self.font_size)
            draw.text((x, y), word, font=self.font, fill=random.choice(self.font_color))
            x += self.font_size * 1.2
        del x
        del draw


        # 序列化处理
        buffered = BytesIO()
        im.save(buffered, format="JPEG")
        return buffered.getvalue()
