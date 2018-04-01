from PIL import Image
from io import BytesIO
from os import path
import os
import requests


class ParseImage(object):
    def __init__(self, img_src, author_name, user_agent):
        self.img_src = img_src
        self.author_name = author_name
        self.user_agent = user_agent

    def save_image(self):
        dir_name = self.author_name
        self.init_path()
        try:
            resp = requests.get(self.img_src, headers={"User-agent":self.user_agent})
            image = Image.open(BytesIO(resp.content))
            file_name = self.img_src.split('/')[-1]
            image.save(dir_name + "/" + file_name.encode())
        except Exception as e:
            print "the image src %s could not find the image, and the err msg is %s"%(self.img_src,e.message)

    def init_path(self):
        if not path.exists(self.author_name):
            os.mkdir(self.author_name)



