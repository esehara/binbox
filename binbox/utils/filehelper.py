# -*- coding:utf-8 -*-

import os
import re
import commands
import Image, ImageFont, ImageDraw

STATIC_FILE_THUMB = "/static/thumb/"
STATIC_FILE_PDF = "/static/pdf/"

class FileHelper:

    _here = os.path.dirname(__file__) + "/.."

    def __init__(self, filename, encoding=False):
        if encoding:
            self.filename = filename.decode('utf-8')
        else:
            self.filename = filename

    def __str__(self):
        return self.filename

    def view_name(self):
        return ".".join(self.filename.encode('utf-8').split(".")[0:-1]).decode('utf-8')
    
    def printize(self):
        target_string = self.view_name()
        utf8 = target_string.encode('utf-8')
        split_string = " ".join(utf8.split("_"))
        
        def transrate(source, target_strings):
            for target in target_strings:
                source = " ".join(source.split(target))
            
            source = re.sub(r"(\s+)", " ", source)
            
            return source.split(" ")
        
        TARGET_STRINGS = ["(", ")", "[", "]"]
        split_string = transrate(split_string, TARGET_STRINGS)

        return_string = []
        for st in split_string:
            return_string.append(st.decode('utf-8'))
        return return_string

    def consolize(self, string):
        return "\ ".join(string.split(" "))

    def get_filepath(self):
        return 'binbox:static/pdf/' + self.view_name() + ".pdf"
    
    def link_path(self):
        return 'static/pdf/' + self.view_name() + ".pdf"
    
    def get_thumb(self):
        expect_path = self._here + STATIC_FILE_THUMB + self.view_name() + ".png"
        if os.path.exists(expect_path):
            return [True, 'static/thumb/' + self.view_name() + ".png", self.link_path()]
        else:
            filepath = self._here + STATIC_FILE_PDF + self.filename
            filepath = self.consolize(filepath)
            cons_expect_path = self.consolize(expect_path)
            
            response = commands.getstatusoutput('echo "convert %s[0] -resize 300 %s" | bash' % (
                filepath.encode('utf-8'), cons_expect_path.encode('utf-8')))
            
            if response[0] == 0:
                return [True, 'static/thumb/' + self.view_name() + ".png", self.link_path()]
            else:
                font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/takao/TakaoGothic.ttf",
                    16, encoding='unicode')
                image = Image.new('RGBA',(300,400),(0,0,0,0))
                draw = ImageDraw.Draw(image)
                for num, elem in enumerate(self.printize()):
                    draw.text((16,50 + (num * 24)), elem, font=font, fill='#000000')
                image.save(self._here + "/static/thumb/" + self.view_name() + ".png", "PNG")
                return [True, 'static/thumb/' + self.view_name() + ".png", self.link_path()]
