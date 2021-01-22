import os
import glob
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import click
import os

def signature(way,word):
    font = ImageFont.truetype('fonts/ddg.ttf', size=100)
    filename=way.split('/')[1]
    im = Image.open(way)
    draw_text = ImageDraw.Draw(im)
    name = os.path.basename(filename)
    index = name.index('.')
    size = draw_text.textsize('~'+' '+word, font=font)
    draw_text.text(
        (im.width-(size[0]+7), im.height-(size[1]+7)),
        '~'+' '+word,
        font=font,
        fill=('white')
        )
    filepath = 'output_images'+'/'+name 
    im.save(filepath)
    return filepath

signature('source_images/images.jpg', 'Emir')