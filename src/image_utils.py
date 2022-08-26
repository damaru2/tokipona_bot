#!/usr/bin/env python
# coding: utf-8
# 
# adapted from https://gist.github.com/josephkern/69591e9bc1d2e07a46d35d2a3ab66542
# 
# Copyright 2011 Álvaro Justen [alvarojusten at gmail dot com]
# License: GPL <http://www.gnu.org/copyleft/gpl.html>

from PIL import Image, ImageDraw, ImageFont
import io

font_cache = {}


class ImageText(object):
    def __init__(self, width, size, font_file, mode='RGBA', background=(0, 0, 0, 255),
                 foreground = (255, 255, 251, 255), padding=10, padding_bottom=None, padding_top=None, padding_left=None, padding_right=None):
        self.mode = mode
        self.padding_top = padding_top or padding
        self.padding_bottom = padding_bottom or padding
        self.padding_left = padding_left or padding
        self.padding_right = padding_right or padding
        self.width = width
        self.text_width = width - self.padding_left - self.padding_right
        self.background = background
        self.foreground = foreground
        font_id = "{}#{}".format(font_file, size)
        if font_id in font_cache:
            self.font = font_cache[font_id]
        else:
            self.font = ImageFont.truetype(font_file, size)
            font_cache[font_id] = self.font

    def save(self, img, filename_or_format=None, binary=False):
        if binary:
            output = io.BytesIO()
            img.save(output, format=filename_or_format)
            return output.getvalue()
        else:
            img.save(filename_or_format or self.filename)
            return filename_or_format

    def render(self, text, filename_or_format, binary=False):
        lines = self.wrap_text(text)
        wrapped = '\n'.join(lines)
        
        text_size = self.font.getsize_multiline(wrapped)
        height = text_size[1] + self.padding_top + self.padding_bottom
        width = self.padding_left + self.padding_right + (text_size[0] if len(lines) == 1 else max(self.text_width, text_size[0]))

        img = Image.new(self.mode, (width, height), color=self.background)
        draw = ImageDraw.Draw(img)

        draw.multiline_text((self.padding_left, self.padding_top), wrapped, font=self.font, fill=self.foreground)
        return self.save(img, filename_or_format, binary)

    def get_text_size(self, text):
        return self.font.getsize(text)

    def wrap_text(self, text):
        hard_lines = text.split('\n')
        lines = []
        for hard_line in hard_lines:
            line = []
            words = hard_line.split()
            for word in words:
                new_line = ' '.join(line + [word])
                size = self.get_text_size(new_line)
                text_height = size[1]
                if size[0] <= self.text_width:
                    line.append(word)
                else:
                    word_size = self.get_text_size(word)
                    if word_size[0] > self.text_width:
                        lines.append(line)
                        lines.append([word])
                        line = []
                    else:
                        lines.append(line)
                        line = [word]
            if line:
                lines.append(line)
        lines = [' '.join(line) for line in lines if line]
        return lines
